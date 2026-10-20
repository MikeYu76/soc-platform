# SOC Platform Architecture

## Architectural shape

The code separates HTTP handling, use-case orchestration, domain behavior, and persistence adapters. Dependencies point inward: routes call application services; services use domain components and repository/Unit of Work abstractions; SQLite and PostgreSQL implement persistence at the edge.

```mermaid
flowchart TB
    UI[React SOC console] -->|HTTP + bearer token| API[FastAPI routes]
    API --> APP[Application services and DTOs]
    APP --> DOMAIN[Domain models, rules, and engines]
    APP --> PORTS[Repository and Unit of Work interfaces]
    PORTS --> SQLITE[SQLite adapter]
    PORTS --> POSTGRES[PostgreSQL adapter]
    API --> AUTH[JWT authentication and role checks]
    AUTH --> APP
    COMPOSE[Docker Compose] -. runs .-> UI
    COMPOSE -. runs .-> API
    COMPOSE -. runs .-> POSTGRES
    COMPOSE -. includes .-> OS[OpenSearch + Dashboards]
```

Processed normalized events are sent to OpenSearch after the relational Unit of Work commits. The relational database remains the source of truth for operational entities; OpenSearch is an auxiliary event-search index. If indexing fails, the API logs the failure and returns the successfully committed processing result. This best-effort path does not include a durable retry queue.

## Event processing sequence

```mermaid
sequenceDiagram
    actor Analyst
    participant API as FastAPI
    participant UseCase as ProcessSecurityEventService
    participant Detect as Detection engine
    participant Enrich as Enrichment engine
    participant Correlate as Correlation engine
    participant Alert as Alert + processors
    participant Case as Case factory + processors
    participant UoW as Unit of Work / repositories
    participant Search as OpenSearch indexer
    Analyst->>API: POST /events (bearer token)
    API->>UseCase: validated event request
    UseCase->>Detect: evaluate event
    Detect-->>UseCase: detections
    UseCase->>Enrich: add context
    Enrich-->>UseCase: enriched detections
    UseCase->>Correlate: evaluate related activity
    Correlate-->>UseCase: correlations
    UseCase->>Alert: create and process alerts
    Alert-->>UseCase: alerts
    UseCase->>Case: create/process investigation cases
    Case-->>UseCase: cases
    UseCase->>UoW: persist results and commit
    UoW-->>UseCase: relational commit succeeds
    UseCase->>Search: index normalized event (best-effort)
    Search-->>UseCase: indexed or logged failure
    UseCase-->>API: response DTO
    API-->>Analyst: JSON response
```

## Case activity sequence

```mermaid
sequenceDiagram
    actor Analyst
    participant API as Cases route
    participant Service as Case application service
    participant UoW as Unit of Work
    participant Repo as Case repository
    Analyst->>API: POST comment/evidence or PATCH workflow field
    API->>API: validate bearer token and role
    API->>Service: request DTO
    Service->>UoW: open transaction
    Service->>Repo: load case and apply domain operation
    Repo-->>Service: updated case with timeline entry
    Service->>UoW: commit
    Service-->>API: response DTO
    API-->>Analyst: JSON response
    Analyst->>API: GET /cases/{id}/timeline
    API->>Service: timeline query
    Service->>Repo: retrieve case history
    Repo-->>API: ordered timeline response
```

## Event pipeline responsibilities

1. **Normalization:** maps supported raw input into the common event model.
2. **Detection:** individual rules identify suspicious events.
3. **Enrichment:** adds available context to detections.
4. **Correlation:** evaluates groups of activity for broader patterns.
5. **Alert generation and processing:** converts findings into alerts, then applies configured processors.
6. **Case creation and processing:** creates investigations and applies case assignment/SLA/escalation processors.
7. **Persistence:** repositories store entities within a Unit of Work transaction.
8. **API response:** application DTOs expose results without returning database records.

## Package map

- `api/`: FastAPI application, route handlers, authentication dependencies, and exception handling.
- `application/`: use cases, request/response DTOs, settings, and composition root.
- `common/`, `alert/`, `case/`, `detection/`, `correlation/`, `enrichment/`, `risk/`: shared and domain behavior.
- `normalization/`: source-specific event parsing and normalization.
- `repositories/`: persistence contracts and query objects.
- `infrastructure/sqlite/`, `infrastructure/postgres/`: concrete persistence adapters.
- `frontend/`: React-based operator console.
- `tests/`: unit, persistence, and API integration coverage.

## Runtime selection

`SOC_DATABASE_BACKEND` accepts `sqlite` or `postgresql`. The default is SQLite. Compose sets PostgreSQL and supplies its service hostname. The composition root selects the matching connection factory and Unit of Work. When `SOC_OPENSEARCH_ENABLED=true`, it also creates an OpenSearch client and injects an event indexer into the processing service. PostgreSQL schema setup is currently managed by the application adapter; a separate migration framework is not configured.
