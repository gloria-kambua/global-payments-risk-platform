# ADR 0011: Analytics-Friendly Schema Design

## Status
Accepted

## Context
The platform supports analytical queries, aggregations, and feature extraction for ML.

Schemas optimized purely for transactional access would limit analytical usability.

## Decision
Database schemas are designed with analytics use cases in mind, including:
- Explicit fact and dimension tables
- Time-based columns suitable for filtering and partitioning
- Minimal reliance on semi-structured JSON fields

## Consequences
- Improved query performance and readability
- Easier integration with BI and ML tooling
- Requires more upfront modeling effort
