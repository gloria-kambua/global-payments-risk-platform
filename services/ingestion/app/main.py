import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

import requests
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

WORLD_BANK_BASE = "https://api.worldbank.org/v2"
DEFAULT_INDICATORS = [
    # Account ownership (% ages 15+)
    "FX.OWN.TOTL.ZS",
    # Used digital payments (% ages 15+)
    "FX.OWN.TOTL.DT.ZS",
    # Mobile money account (% ages 15+)
    "FX.OWN.TOTL.MM.ZS",
    # Bank branches per 100,000 adults
    "FB.CBK.BRCH.P5",
]

def db_dsn() -> str:
    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "payments_risk")
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    return f"host={host} port={port} dbname={db} user={user} password={password}"

def read_sql(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def ensure_schema(conn: psycopg.Connection) -> None:
    sql_path = os.path.join(os.path.dirname(__file__), "..", "sql", "001_init_schema.sql")
    sql_path = os.path.abspath(sql_path)
    with conn.cursor() as cur:
        cur.execute(read_sql(sql_path))
    conn.commit()

def start_run(conn: psycopg.Connection, source_key: str, source_name: str, source_url: str) -> str:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            INSERT INTO de_ingestion_runs (source_key, source_name, source_url, status)
            VALUES (%s, %s, %s, 'started')
            RETURNING run_id::text
            """,
            (source_key, source_name, source_url),
        )
        run_id = cur.fetchone()["run_id"]
    conn.commit()
    return run_id

def finish_run(conn: psycopg.Connection, run_id: str, status: str, records: int = 0, error: str | None = None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE de_ingestion_runs
            SET status=%s, finished_at=now(), records_fetched=%s, error_message=%s
            WHERE run_id=%s::uuid
            """,
            (status, records, error, run_id),
        )
    conn.commit()

def get_source_id(conn: psycopg.Connection, source_key: str) -> int:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT source_id FROM sources WHERE source_key=%s", (source_key,))
        row = cur.fetchone()
        if not row:
            raise RuntimeError(f"source_key not found in sources table: {source_key}")
        return int(row["source_id"])

def world_bank_fetch_indicator(indicator: str, per_page: int = 20000) -> List[Dict[str, Any]]:
    # World Bank returns JSON array: [metadata, data]
    url = f"{WORLD_BANK_BASE}/country/all/indicator/{indicator}"
    params = {"format": "json", "per_page": per_page}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    payload = r.json()
    if not isinstance(payload, list) or len(payload) < 2:
        return []
    data = payload[1] or []
    # Keep only rows with essential fields
    return [d for d in data if d and d.get("country") and d.get("date")]

def upsert_indicator_dim(conn: psycopg.Connection, indicator_code: str, indicator_name: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dim_indicator (indicator_code, indicator_name, indicator_source)
            VALUES (%s, %s, 'world_bank')
            ON CONFLICT (indicator_code) DO UPDATE
            SET indicator_name = EXCLUDED.indicator_name
            """,
            (indicator_code, indicator_name),
        )
    conn.commit()

def upsert_country_dim(conn: psycopg.Connection, iso3: str, country_name: str, iso2: str | None = None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dim_country (iso2, iso3, country_name)
            VALUES (%s, %s, %s)
            ON CONFLICT (iso3) DO UPDATE
            SET country_name = EXCLUDED.country_name,
                iso2 = COALESCE(dim_country.iso2, EXCLUDED.iso2)
            """,
            (iso2, iso3, country_name),
        )
    conn.commit()

def insert_raw_event(conn: psycopg.Connection, run_id: str, source_id: int, entity_key: str, record_key: str, payload: Dict[str, Any]) -> None:
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    payload_hash = sha256_text(text)
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO raw_events (run_id, source_id, entity_key, record_key, payload, payload_hash)
            VALUES (%s::uuid, %s, %s, %s, %s::jsonb, %s)
            ON CONFLICT (source_id, payload_hash) DO NOTHING
            """,
            (run_id, source_id, entity_key, record_key, text, payload_hash),
        )

def upsert_fact_indicator(conn: psycopg.Connection, run_id: str, source_id: int, iso3: str, indicator_code: str, year: int, value: Any) -> None:
    # value can be None
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO fact_country_indicator (run_id, source_id, iso3, indicator_code, year, value)
            VALUES (%s::uuid, %s, %s, %s, %s, %s)
            ON CONFLICT (source_id, iso3, indicator_code, year) DO UPDATE
            SET value = EXCLUDED.value,
                run_id = EXCLUDED.run_id
            """,
            (run_id, source_id, iso3, indicator_code, year, value),
        )

def normalize_world_bank_record(d: Dict[str, Any]) -> Tuple[str, str, str, int, Any]:
    """
    Returns: (iso3, country_name, indicator_code, year, value)
    """
    iso3 = (d.get("countryiso3code") or "").strip()
    country_name = (d.get("country", {}) or {}).get("value") or ""
    indicator_code = (d.get("indicator", {}) or {}).get("id") or ""
    year = int(d.get("date"))
    value = d.get("value")
    return iso3, country_name, indicator_code, year, value

def main() -> None:
    indicators = os.getenv("WORLD_BANK_INDICATORS", ",".join(DEFAULT_INDICATORS)).split(",")
    indicators = [i.strip() for i in indicators if i.strip()]

    source_key = "world_bank"
    source_name = "World Bank Open Data API"
    source_url = WORLD_BANK_BASE

    with psycopg.connect(db_dsn()) as conn:
        ensure_schema(conn)

        run_id = start_run(conn, source_key, source_name, source_url)
        source_id = get_source_id(conn, source_key)

        total = 0
        try:
            for ind in indicators:
                rows = world_bank_fetch_indicator(ind)
                # Update indicator dim name once (best effort)
                if rows:
                    indicator_name = (rows[0].get("indicator", {}) or {}).get("value") or ind
                    upsert_indicator_dim(conn, ind, indicator_name)

                for d in rows:
                    iso3, country_name, indicator_code, year, value = normalize_world_bank_record(d)
                    if not iso3 or not indicator_code:
                        continue

                    upsert_country_dim(conn, iso3=iso3, country_name=country_name)

                    record_key = f"{iso3}|{year}|{indicator_code}"
                    insert_raw_event(conn, run_id, source_id, entity_key=indicator_code, record_key=record_key, payload=d)
                    upsert_fact_indicator(conn, run_id, source_id, iso3, indicator_code, year, value)
                    total += 1

                conn.commit()

            finish_run(conn, run_id, "succeeded", records=total)
            print(f"✅ World Bank ingestion succeeded. records={total} run_id={run_id}")

        except Exception as e:
            conn.rollback()
            finish_run(conn, run_id, "failed", records=total, error=str(e))
            raise

if __name__ == "__main__":
    main()
