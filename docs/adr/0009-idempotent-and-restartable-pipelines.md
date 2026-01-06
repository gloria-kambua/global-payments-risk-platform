# ADR 0009: Idempotent and Restartable Pipelines

## Status
Accepted

## Context
Ingestion pipelines may fail due to transient network issues, malformed data, or upstream changes.

Re-running pipelines must not introduce duplicate records or corrupt downstream tables.

## Decision
All data pipelines are designed to be idempotent and safely restartable.

## Consequences
- Pipelines can be re-run without manual cleanup
- Duplicate ingestion is prevented through keys and metadata
- Simplifies orchestration and operational recovery
- Requires additional bookkeeping (batch IDs, timestamps)
