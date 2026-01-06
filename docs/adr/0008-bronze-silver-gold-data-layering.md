# ADR 0008: Bronze / Silver / Gold Data Layering

## Status
Accepted

## Context
Raw datasets vary significantly in structure, quality, and completeness.
Downstream use cases (analytics, ML, decisioning) require stable, well-defined data contracts.

## Decision
Data is organized into explicit processing layers:

- Bronze: Raw, immutable ingested data
- Silver: Normalized, domain-aligned tables
- Gold: Aggregated, analytics-ready views

## Consequences
- Clear separation of concerns between ingestion and consumption
- Safe evolution of normalization logic
- Simplified debugging and reprocessing
- Slight increase in storage and processing overhead
