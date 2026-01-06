# ADR 0012: Orchestration-Ready Pipeline Design

## Status
Accepted

## Context
As the platform grows, pipelines may require scheduling, dependency management, and monitoring.

Introducing orchestration too early adds operational overhead.

## Decision
Pipelines are implemented as discrete, dependency-aware steps designed to be orchestrated later by tools such as Airflow or Prefect.

## Consequences
- Pipelines remain simple in early phases
- Smooth migration to full orchestration later
- Requires discipline in pipeline boundaries and interfaces
