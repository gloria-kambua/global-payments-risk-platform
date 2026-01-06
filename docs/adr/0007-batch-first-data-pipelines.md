# ADR 0007: Batch-First Data Pipelines

## Status
Accepted

## Context
Initial data sources for the platform are public and semi-public datasets published periodically rather than continuous event streams.

Early system goals prioritize correctness, debuggability, and iteration speed over real-time processing.

## Decision
The platform adopts a batch-first ingestion approach for all initial data pipelines.

## Consequences
- Lower operational complexity in early stages
- Easier debugging and reprocessing of failed runs
- Clear upgrade path to streaming architectures when required
- Not suitable for real-time detection in the current phase
