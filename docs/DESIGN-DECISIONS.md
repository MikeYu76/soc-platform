# Design Decisions and Trade-offs

This document records the current implementation choices and their practical costs. It describes a development/portfolio system, not a production security certification.

## Layered application with domain-focused modules

**Choice:** API handlers delegate to application services; domain rules and processors own security and workflow behavior; persistence is behind repository and Unit of Work contracts.

**Benefit:** Components can be tested independently, and changes to the web framework or database are less likely to leak into domain logic.

**Cost:** There are more interfaces, DTOs, and composition code than in a small single-file application. New features need to be threaded through the service and dependency wiring.

## SQLite locally; PostgreSQL in Compose

**Choice:** SQLite is the zero-setup default for local development and tests. Docker Compose selects PostgreSQL.

**Benefit:** Fast isolated tests and a realistic relational database for the containerized stack.

**Cost:** Both adapters must remain behaviorally aligned. SQLite data is not migrated automatically to PostgreSQL. PostgreSQL migrations are forward-only; rollback scripts and a migration authoring CLI are not provided.

## Synchronous request processing

**Choice:** Event processing and persistence run synchronously in the API request.

**Benefit:** The behavior is straightforward to follow and test, and the caller receives processing results immediately.

**Cost:** Long pipelines consume request worker time; there is no durable queue, retry policy, or independent scaling of ingestion and processing.

## JWT access tokens and role-based checks

**Choice:** Users authenticate with username/password; protected endpoints require bearer tokens and role checks.

**Benefit:** The application demonstrates authentication and authorization boundaries.

**Cost / follow-up:** Token expiration and revocation strategy is limited; changing a user's role may not affect an already-issued token until it expires, depending on the token claims. Use TLS, strong secret management, rate limiting, audit logging, and a reviewed account recovery process before deployment beyond local development. Do not commit `.env` or share credentials.

## In-memory rule and enrichment registration

**Choice:** Rules, enrichers, and processors are registered in the composition root.

**Benefit:** The active pipeline is visible in one place and easy to configure for tests.

**Cost:** Adding plugins dynamically or configuring tenants independently would need additional loading/configuration infrastructure.

## Relational persistence plus an OpenSearch event index

**Choice:** The normalized event and its outbox entry are committed together in the selected relational database. A background worker indexes the event in OpenSearch using its stable ID, then removes the outbox entry. Failed writes remain queued and use capped exponential backoff. OpenSearch indexing is optional outside Compose through `SOC_OPENSEARCH_ENABLED`.

**Benefit:** Operators can search full-text event messages and filter on mapped event fields in OpenSearch Dashboards.

**Cost / follow-up:** The database and search index cannot share one transaction, so search results may lag behind ingestion. Administrators can inspect aggregate queue health at `GET /operations/opensearch-indexing` and scrape aggregate Prometheus metrics at `GET /operations/opensearch-indexing/metrics`. The worker logs sustained-backlog and recovery alerts using configurable queue count and duration thresholds. The alert timer is in memory, so a restart resets the sustained-duration window. There is no dead-letter threshold or per-event retry control. Delivery is at least once: multiple workers may process the same pending row, and indexing by stable ID makes duplicate writes safe. A retry after OpenSearch success and before outbox deletion is also safe. Credentials and disabled certificate verification in Compose are for local development only.

## React console served by Nginx

**Choice:** The frontend is a small React/Vite application built into a static bundle and served by Nginx in Compose.

**Benefit:** Simple local deployment without a separate frontend development runtime.

**Cost:** The API and console are separate services; production concerns such as TLS termination, caching policy, content security policy, and deployment routing need explicit configuration.

## CI quality gates

**Choice:** GitHub Actions runs Ruff, mypy, and pytest with coverage. Mypy currently uses `continue-on-error: true`.

**Benefit:** Type-check feedback is visible while the project adopts strict typing without blocking every change.

**Cost / follow-up:** A green workflow does not guarantee mypy passed when that step is advisory. Local mypy currently passes; consider making it blocking after agreeing on the project's typing policy. Coverage is reported in CI, but no minimum threshold is enforced.

## No external threat-intelligence dependency by default

**Choice:** The core pipeline has local/example context providers and does not require API keys to run.

**Benefit:** Tests and local setup are reproducible and do not disclose external credentials.

**Cost:** Threat intelligence freshness, provider failure handling, quotas, and provenance are not represented as a fully operational integration yet.

## Development deployment only

Docker Compose is intended for local development. It does not provide production-grade TLS, secret rotation, backup/restore procedures, resource sizing, network segmentation, or high availability. The health endpoint is a liveness check and should not be treated as a full dependency readiness signal.
