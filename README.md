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

- Ingest real public payments and risk datasets  
- Normalize and store data using clear domain models  
- Preserve raw source data and lineage  
- Expose clean APIs for downstream consumers  
- Design the system to scale toward streaming, ML, and AI use cases  

---

## Current Features

### Data Ingestion
- Batch ingestion from public sources (CSV, JSON)
- Schema validation and normalization
- Idempotent and retry-safe ingestion logic

### Data Storage
- PostgreSQL as the primary datastore
- Separation of raw and normalized data
- Analytics-friendly schema design

### API Layer
- FastAPI-based service
- Typed request and response models
- Pagination and predictable error handling

### Infrastructure
- Fully dockerized services
- Environment-based configuration
- One-command local setup

---

## Tech Stack

**Languages**
- Python

**Backend & APIs**
- FastAPI  
- Pydantic  

**Data**
- PostgreSQL  

**Infrastructure**
- Docker  
- Docker Compose  

---

## Architecture Overview

```

Public Data Sources
(CSV / JSON)
|
v
Data Engineering Pipelines
(fetch, validate, normalize)
|
v
PostgreSQL

* raw_events
* transactions
* risk_indicators
* sources
  |
  v
  API & Decision Services

```

---

## System Components

The platform is intentionally structured as a set of clear, purpose-driven components.  
Each component exists to solve a specific class of problems and mirrors how real fintech and data platforms are built in production.

**System flow:**

**Data Engineering → Deterministic Decisioning → Predictive Intelligence → Human-Readable Insight**

---

### Data Engineering (Pipelines & Storage)

**Responsibilities**
- Ingest external public datasets (batch-first)
- Handle schema drift, missing fields, and inconsistent formats
- Normalize raw data into analytics-ready tables
- Enforce data quality, freshness, and idempotency
- Preserve source lineage and ingestion metadata

**Key Characteristics**
- Bronze / Silver / Gold style layering  
  - Raw data (immutable)  
  - Normalized domain tables  
  - Aggregated analytical views  
- Fact and dimension modeling  
- Designed for orchestration (Airflow/Prefect-style), even if not deployed yet  

**Primary Outputs**
- `raw_events`
- `transactions`
- `risk_indicators`
- Aggregated country and time-based summaries  

This layer is the backbone of the platform. All downstream components depend on its correctness and reliability.

---

### Java Risk Decision Engine (Deterministic Logic)

**Responsibilities**
- Apply deterministic, explainable risk rules
- Perform policy and threshold evaluation
- Produce stable, auditable risk decisions
- Expose versioned decision APIs

**Why Java**
- Strong typing and explicit contracts
- Predictable runtime behavior
- Well-suited for core financial and risk logic
- Easier to reason about correctness and long-term maintenance

**Primary Outputs**
- Risk scores
- Risk flags
- Decision metadata suitable for auditing and compliance

This component prioritizes correctness and predictability over experimentation.

---

### Machine Learning (Predictive Modeling)

**Responsibilities**
- Learn patterns from historical normalized data
- Predict risk likelihoods and trends
- Generate probabilistic signals that complement deterministic rules

**Scope**
- Feature extraction from curated data tables
- Baseline, explainable models (no deep learning for its own sake)
- Clear evaluation metrics (precision, recall, ROC-AUC)
- Model versioning and reproducibility

**Primary Outputs**
- Predicted risk probabilities
- Model evaluation metrics
- Feature importance or explanations

ML augments decision-making but does not replace deterministic logic.

---

### LLM / AI Layer (Summarization & Insight)

**Responsibilities**
- Convert structured risk data into concise, human-readable summaries
- Generate periodic risk briefs by country, source, or time window
- Assist interpretation without owning decision authority

**Constraints**
- Outputs are grounded strictly in stored data
- No hallucinated or free-form financial decisions
- Guardrails applied to limit scope and tone

**Primary Outputs**
- Weekly or monthly risk summaries
- Explanations of trends and anomalies

This layer improves usability and communication without controlling core logic.

---

## Architecture Decision Records (ADRs)

This project uses Architecture Decision Records (ADRs) to document key technical decisions, their context, and trade-offs.

ADRs make architectural intent explicit and support long-term system evolution.

All ADRs are stored in:

```

docs/adr/

```

Each ADR follows a consistent format:
- Context
- Decision
- Consequences

---

## Data Model (High Level)

| Table             | Description                     |
|-------------------|---------------------------------|
| `sources`         | Dataset metadata and provenance |
| `raw_events`      | Immutable raw ingested records  |
| `transactions`    | Normalized payment data         |
| `risk_indicators` | Risk-related signals            |
| `countries`       | Country reference and ISO codes |

---

## API Examples

- `GET /transactions?country=KE`
- `GET /transactions?from=2024-01-01&to=2024-12-31`
- `GET /risk-summary?country=NG`
- `GET /sources`

API documentation:
```

[http://localhost:8000/docs](http://localhost:8000/docs)

```

---

## Project Structure

```

.
├── services/
│   ├── ingestion/        # Data engineering pipelines
│   ├── api/              # FastAPI service
│   ├── analytics/        # Aggregations and metrics
│   └── risk-engine/      # Java risk decision engine (planned)
├── ml/                   # ML training and inference (planned)
├── data/                 # Reference data and mappings
├── scripts/              # Utilities and maintenance scripts
├── docs/
│   └── adr/              # Architecture Decision Records
├── docker-compose.yml
└── README.md

````

---

## Running the Project Locally

### Prerequisites
- Docker
- Docker Compose

### Start Services
```bash
docker-compose up --build
````

This will start:

* PostgreSQL
* Ingestion service
* API service

---

## What This Project Is Not

* Not a frontend or dashboard project
* Not a tutorial or demo
* Not a CRUD application

This repository focuses on **backend engineering, data engineering, and system design** rather than presentation.

---

## Roadmap

* Streaming ingestion (Kafka-style architecture)
* Data quality checks and anomaly detection
* Java-based risk decision engine
* Feature extraction for ML-based risk scoring
* LLM-powered risk summaries
* BI-friendly exports (Parquet, DuckDB)
* Automated data freshness monitoring

---

## Author

**Gloria Kambua**
Senior Software Engineer – Backend, Data & Distributed Systems
Remote-first | Nairobi (GMT+3)

📧 [kambuasammy96@gmail.com](mailto:kambuasammy96@gmail.com)
🔗 [https://www.linkedin.com/in/kambua-sammy/](https://www.linkedin.com/in/kambua-sammy/)

---

## Notes for Reviewers

This project is intentionally scoped to demonstrate:

* Data engineering foundations
* Clear system boundaries
* Deterministic vs probabilistic decisioning
* Production-minded architecture decisions

It prioritizes correctness, clarity, and extensibility over visual polish.
