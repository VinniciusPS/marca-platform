[English](README.md) | [Português](README.pt-BR.md)

# Marca Platform

Integrated management platform for clinic/service operations, combining appointment scheduling, payment processing, and operational analytics.

## Overview

Marca Platform is a domain-oriented system that enables businesses to manage:

- **Service Reservations** — Scheduling, availability, and confirmation of appointments/services
- **Payment Processing** — Authorization, transaction processing, and reconciliation
- **Operational Analytics** — Business metrics, market trends, and strategic decisions

The system is organized as a microservices architecture with clear separation of concerns, asynchronous communication, and an isolated analytics data layer.

## Getting Started

### For developers new to the project

1. Start with architectural documentation:
   - [`docs/architecture/context.md`](docs/architecture/context.md) — Understand the overall context
   - [`docs/architecture/containers.md`](docs/architecture/containers.md) — See the main components

2. Review diagrams to visualize flows:
   - [`docs/diagrams/context.md`](docs/diagrams/context.md) — Context diagram
   - [`docs/diagrams/flow-booking-payments.md`](docs/diagrams/flow-booking-payments.md) — Main flow

3. Understand architectural decisions:
   - [`docs/decisions/adr-002-bff-pattern.md`](docs/decisions/adr-002-bff-pattern.md) — Why BFF?
   - [`docs/decisions/adr-001-separate-booking-and-payments-apis.md`](docs/decisions/adr-001-separate-booking-and-payments-apis.md) — Why separate APIs?

4. Review current implementation state:
   - [`docs/deployment/current.md`](docs/deployment/current.md) — What is implemented

5. See live application at:
   - Link: https://marca-platform.vercel.app/

## Repository Structure

```
.
├── docs/                          # Architectural documentation
│   ├── README.md                  # Documentation reading guide
│   ├── architecture/              # Conceptual definitions (C4 Model)
│   ├── decisions/                 # Architectural decisions (ADR)
│   ├── deployment/                # Current implementation state
│   ├── diagrams/                  # Diagrams as code (Mermaid)
│   ├── issues/                    # Planning and evolution state
│   └── requirements/              # Functional and non-functional specs
│
├── services/                      # Backend services
│   ├── api/
│   │   ├── booking/               # Reservations API
│   │   ├── payments/              # Payments API
│   │   └── analytics/             # Analytics API
│   └── bff/                       # Backend-for-Frontend
│
├── view/                          # Frontend Web
│   └── src/                       # React/Vite/Tailwind
│
├── etl/                           # Data orchestration and transformation
│   ├── airflow/                   # Extraction DAGs
│   └── dbt/                       # Transformation models
│
├── database/                      # Schemas and migrations
│   └── migrations/                # Flyway migrations
│
├── deploy/                        # Deployment configurations
│   ├── dev/                       # Development environment
│   └── prd/                       # Production environment
│
└── scripts/                       # Utilities and automation
```

## Architecture

### Conceptual Model

The platform follows the **C4 Model** for architecture documentation:

- **Context** — Actors, external systems, and boundaries
- **Containers** — Executable components (services, databases, frontends)
- **Components** — Internal decomposition of containers
- **Code** — Implementation

Detailed documentation: [`docs/README.md`](docs/README.md)

### Architectural Patterns

#### Backend-for-Frontend (BFF)
The BFF orchestrates calls to domain services, providing an interface optimized for the frontend.

- **Decision**: [`adr-002-bff-pattern.md`](docs/decisions/adr-002-bff-pattern.md)

#### Domain Separation
Reservations and Payments are independent APIs with:
- Own databases
- Decoupled deployment cycles
- Well-defined contracts

- **Decision**: [`adr-001-separate-booking-and-payments-apis.md`](docs/decisions/adr-001-separate-booking-and-payments-apis.md)

#### Asynchronous Communication
Services communicate through an Event Bus to reduce coupling.

- **Decision**: [`adr-003-event-bus-pattern.md`](docs/decisions/adr-003-event-bus-pattern.md)

#### Isolated Analytics
Separate analytics database, fed by ETL, for OLAP and decision-making.

- **Decision**: [`adr-004-analytics-db.md`](docs/decisions/adr-004-analytics-db.md)

## Data

### Primary Database
PostgreSQL with multiple schemas:

- **clinic** — Patients, professionals, schedules
- **operations** — Contracts and operations
- **marketing** — Trend terms and strategy
- **staging** — Raw ETL data
- **silver/gold** — Enriched models for analytics
- **control** — Load audit trail

### Data Pipeline
1. **Extraction** — Airflow extracts data from sources (e.g., Google Trends)
2. **Staging** — Raw data persisted in PostgreSQL
3. **Transformation** — dbt transforms into silver/gold models
4. **Consumption** — Analytics API exposes data via REST

## Main Components

### Frontend (`view/`)
- React + Vite + Tailwind
- Tests with Vitest
- Linting with ESLint

**Status**: Functional

### BFF (`services/bff/`)
- Java + SpringBoot
- Orchestrates domain services

**Status**: Initial structure, implementation in progress

### Reservations API (`services/api/booking/`)
- Python + FastAPI (planned)

**Status**: Architecture structure, no functional implementation

### Payments API (`services/api/payments/`)
- Python + FastAPI (planned)
- External gateway integration

**Status**: Minimal entry point

### Analytics API (`services/api/analytics/`)
- Python + FastAPI + SQLAlchemy
- Access to silver/gold data

**Status**: Functional

### ETL (`etl/`)
- Airflow for orchestration
- dbt for transformation
- Google Trends as data source

**Status**: Functional

## Main Flows

### Reservation and Payment Creation

```
1. Operator creates reservation in frontend
2. BFF receives and forwards to Reservations API
3. Reservations API persists in PENDING_PAYMENT
4. ReservationCreated event published to Event Bus
5. Payments API processes payment with gateway
6. Result published (confirmed or rejected)
7. Reservations API updates reservation status
8. Frontend reflects new state
```

Detailed diagram: [`docs/diagrams/flow-booking-payments.md`](docs/diagrams/flow-booking-payments.md)

### Analytics

```
1. Airflow extracts Google Trends daily
2. Raw data persisted in staging
3. dbt transforms into silver/gold models
4. Analytics API exposes data via REST endpoints
5. Frontend or external tools query the API
```

Detailed diagram: [`docs/diagrams/flow-analytics.md`](docs/diagrams/flow-analytics.md)

## Key Decisions

All relevant architectural decisions are documented as ADRs:

| ADR | Decision | Status |
|-----|----------|--------|
| [001](docs/decisions/adr-001-separate-booking-and-payments-apis.md) | Separation of Reservations and Payments into distinct APIs | Accepted |
| [002](docs/decisions/adr-002-bff-pattern.md) | Adoption of Backend-for-Frontend | Accepted |
| [003](docs/decisions/adr-003-event-bus-pattern.md) | Asynchronous communication via Event Bus | Accepted |
| [004](docs/decisions/adr-004-analytics-db.md) | Separate analytics database | Accepted |

Read full justifications in [`docs/decisions/`](docs/decisions/).

## Current State

Implementation is evolving:

- Functional: Frontend, Analytics API, ETL
- Partial: BFF, Payments API
- Not started: Reservations API, Event Bus

Complete details in [`docs/deployment/current.md`](docs/deployment/current.md) and [`docs/issues/Master-plan.md`](docs/issues/Master-plan.md).

## Next Steps

1. **Implement Reservations API** — Core scheduling functionality
2. **Complete Payments flow** — External gateway integration
3. **Implement Event Bus** — Asynchronous service communication
4. **Add E2E tests** — Validate main flows
5. **Document final deployment** — CI/CD for production

See detailed plan in [`docs/issues/Master-plan.md`](docs/issues/Master-plan.md).

## Documentation

- **[Documentation Guide](docs/README.md)** — How to navigate and evolve documentation
- **[Architecture](docs/architecture/)** — Conceptual model (C4)
- **[Decisions](docs/decisions/)** — ADRs justifying choices
- **[Deployment](docs/deployment/)** — Implementation state and strategy
- **[Diagrams](docs/diagrams/)** — Flows and visual topology
- **[Evolution Issues](docs/issues/)** — Planning and change state

## Governance

This repository follows **Spec-Driven Development (SDD)** methodology with **Harness Engineering** to ensure changes are:

- Explicitly specified
- Traceable to requirements
- Verifiable through tests
- Documented for continuity

See [`AGENTS.md`](AGENTS.md) for operational principles.

## Conventions

- Documentation in Portuguese (pt-BR) and English
- Code in English
- Diagrams as code (Mermaid)
- Decisions formalized as ADRs
- Specifications before implementation

---

**Last updated**: 2026-08-30  
**Status**: Architecture documented, implementation in progress
