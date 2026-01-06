# Global Payments & Risk Intelligence Platform

A production-oriented data platform for ingesting, normalizing, and exposing **real-world payments and financial risk signals** across countries, sources, and time.

This project focuses on the core engineering problems behind fintech and risk systems: reliable ingestion, strong data modeling, and clean APIs.

---

## Problem Statement

Payments and financial risk data exists across many public and semi-public sources, but it is fragmented, inconsistent, and difficult to analyze at scale.

As a result, early indicators of fraud, country exposure, sanctions risk, and operational anomalies are often detected too late.

This platform demonstrates how to transform **messy, real-world data** into **structured, analytics-ready intelligence** using production-grade backend and data engineering practices.

---

## Project Goals

* Ingest real public payments and risk datasets
* Normalize and store data using clear domain models
* Preserve raw source data and lineage
* Expose clean APIs for downstream consumers
* Design the system to scale toward streaming and ML use cases

---

## Current Features

### Data Ingestion

* Batch ingestion from public sources (CSV, JSON)
* Schema validation and normalization
* Idempotent and retry-safe ingestion logic

### Data Storage

* PostgreSQL as the primary datastore
* Separation of raw and normalized data
* Analytics-friendly schema design

### API Layer

* FastAPI-based service
* Typed request and response models
* Pagination and predictable error handling

### Infrastructure

* Fully dockerized services
* Environment-based configuration
* One-command local setup

---

## Tech Stack

**Languages**

* Python

**Backend & APIs**

* FastAPI
* Pydantic

**Data**

* PostgreSQL

**Infrastructure**

* Docker
* Docker Compose

---

## Architecture Overview

```
Public Data Sources
(CSV / JSON)
        |
        v
Ingestion Service
(fetch, validate, normalize)
        |
        v
PostgreSQL
- raw_events
- transactions
- risk_indicators
- sources
        |
        v
API Service (FastAPI)
```

---

## Architecture Decision Records (ADRs)

This project uses Architecture Decision Records (ADRs) to document key technical decisions, their context, and trade-offs.

ADRs make architectural intent explicit and support long-term system evolution.

All ADRs are stored in:

docs/adr/

Each ADR follows a consistent format:

* Context
* Decision
* Consequences

---

## Data Model (High Level)

| Table             | Description                        |
| ----------------- | ---------------------------------- |
| `sources`         | Dataset metadata and provenance    |
| `raw_events`      | Immutable raw ingested records     |
| `transactions`    | Normalized payment data            |
| `risk_indicators` | Risk-related signals               |
| `countries`       | Country reference and ISO mappings |

---

## API Examples

* `GET /transactions?country=KE`
* `GET /transactions?from=2024-01-01&to=2024-12-31`
* `GET /risk-summary?country=NG`
* `GET /sources`

API documentation available at:

```
http://localhost:8000/docs
```

---

## Project Structure

```
.
├── services/
│   ├── ingestion/        # Data ingestion and normalization
│   ├── api/              # FastAPI service
│   └── analytics/        # Aggregations and domain logic
├── data/                 # Reference data and mappings
├── scripts/              # Utilities and maintenance scripts
├── docs/
│   └── adr/              # Architecture Decision Records
├── docker-compose.yml
└── README.md
```

---

## Running the Project Locally

### Prerequisites

* Docker
* Docker Compose

### Start Services

```bash
docker-compose up --build
```

This will start:

* PostgreSQL
* Ingestion service
* API service

---

## What This Project Is Not

* Not a frontend or dashboard project
* Not a tutorial or demo
* Not a CRUD application

This repository focuses on **backend engineering, data modeling, and system design**.

---

## Roadmap

* Streaming ingestion (Kafka-style architecture)
* Data quality checks and anomaly detection
* Feature extraction for ML-based risk scoring
* BI-friendly exports (Parquet, DuckDB)
* Automated data freshness monitoring

---

## Author

**Gloria Kambua**
Senior Software Engineer – Backend & Data Systems
Remote-first | Nairobi (GMT+3)

---

## Notes for Reviewers

This project is intentionally scoped to show:

* How data pipelines are designed
* How ingestion and normalization are handled
* How system decisions are documented and evolved

It prioritizes correctness, clarity, and extensibility over visual polish.

