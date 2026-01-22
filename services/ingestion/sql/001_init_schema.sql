-- Bronze: raw payloads + batch runs
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS de_ingestion_runs (
  run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_key TEXT NOT NULL,                -- e.g. world_bank
  source_name TEXT NOT NULL,               -- human readable
  source_url TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'started',  -- started|succeeded|failed
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  records_fetched INT DEFAULT 0,
  error_message TEXT
);

CREATE TABLE IF NOT EXISTS sources (
  source_id BIGSERIAL PRIMARY KEY,
  source_key TEXT UNIQUE NOT NULL,         -- world_bank, ofac, eu_sanctions
  source_name TEXT NOT NULL,
  base_url TEXT NOT NULL,
  trust_level TEXT NOT NULL DEFAULT 'high',
  update_cadence TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO sources (source_key, source_name, base_url, trust_level, update_cadence)
VALUES
  ('world_bank', 'World Bank Open Data API', 'https://api.worldbank.org/v2/', 'high', 'periodic')
ON CONFLICT (source_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS raw_events (
  raw_event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES de_ingestion_runs(run_id) ON DELETE CASCADE,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  entity_key TEXT,                         -- e.g. indicator code
  record_key TEXT,                         -- e.g. country|year|indicator
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  payload JSONB NOT NULL,
  payload_hash TEXT NOT NULL,              -- dedupe helper
  UNIQUE (source_id, payload_hash)
);

-- Silver: normalized indicators (stable schema across datasets)
CREATE TABLE IF NOT EXISTS dim_country (
  country_id BIGSERIAL PRIMARY KEY,
  iso2 CHAR(2),
  iso3 CHAR(3),
  country_name TEXT NOT NULL,
  UNIQUE (iso3)
);

CREATE TABLE IF NOT EXISTS dim_indicator (
  indicator_id BIGSERIAL PRIMARY KEY,
  indicator_code TEXT UNIQUE NOT NULL,     -- e.g. FX.OWN.TOTL.ZS
  indicator_name TEXT NOT NULL,
  indicator_source TEXT NOT NULL DEFAULT 'world_bank'
);

CREATE TABLE IF NOT EXISTS fact_country_indicator (
  fact_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID NOT NULL REFERENCES de_ingestion_runs(run_id) ON DELETE RESTRICT,
  source_id BIGINT NOT NULL REFERENCES sources(source_id),
  iso3 CHAR(3) NOT NULL,
  indicator_code TEXT NOT NULL,
  year INT NOT NULL,
  value NUMERIC,
  unit TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (source_id, iso3, indicator_code, year)
);

-- Gold: aggregated, analytics-ready view/table
CREATE TABLE IF NOT EXISTS gold_country_risk_profile (
  profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  as_of_date DATE NOT NULL,
  iso3 CHAR(3) NOT NULL,
  payments_access_score NUMERIC,           -- derived score
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (as_of_date, iso3)
);

-- Helpful index for analytics
CREATE INDEX IF NOT EXISTS idx_fact_indicator_country_year
  ON fact_country_indicator (iso3, indicator_code, year);
