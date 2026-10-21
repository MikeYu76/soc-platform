# SOC Platform Developer Handoff

## What this project is

A modular SOC workflow and portfolio project. The repository contains a FastAPI backend, React console, event detection and correlation pipeline, case/alert workflows, SQLite and PostgreSQL adapters, JWT authentication with role checks, Docker Compose configuration, and automated tests.

For the architecture, request flows, API endpoints, and design trade-offs, see:

- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/DESIGN-DECISIONS.md`

## Current status

The implemented roadmap includes event processing, detection and correlation rules, enrichment, alerts, case management (including comments, evidence, priority changes, and timeline entries), JWT login/RBAC, Docker Compose, PostgreSQL persistence with versioned schema migrations, React console, and GitHub Actions quality checks.

At the latest local verification, 222 pytest tests passed; Ruff passed; and mypy reported no issues in 248 source files. The PostgreSQL migration `0001_initial_schema` was verified in the running database. CI now treats mypy failures as workflow failures; confirm the next GitHub Actions run after applying this change.

## Local development

Use Python 3.12. From the project root in PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m uvicorn api.main:app --reload
```

SQLite is the default for a directly launched API. Configure `SOC_JWT_SECRET`, `SOC_BOOTSTRAP_ADMIN_USERNAME`, and `SOC_BOOTSTRAP_ADMIN_PASSWORD` in a private `.env` file for authentication/bootstrap. `.env` is ignored by Git. The bootstrap password must meet the minimum configured by the API.

## Docker development

1. Ensure Docker Desktop is running.
2. Make sure `.env` contains the variables required by `compose.yaml`, including PostgreSQL, bootstrap administrator, JWT, and OpenSearch passwords.
3. Start services with `docker compose up --build -d`.
4. Check service state with `docker compose ps` and API health at `http://localhost:8000/health`.
5. Use `http://localhost:3000` for the console, `http://localhost:8000/docs` for API docs, and `http://localhost:5601` for OpenSearch Dashboards.
6. Stop with `docker compose down`. Avoid `docker compose down -v` unless deleting persistent database/search data is intentional.

The Compose setup uses PostgreSQL and enables durable outbox indexing of processed events to OpenSearch. In OpenSearch Dashboards, create a `security-events` data view using `timestamp` as the time field. Indexing runs asynchronously after database commit; failed writes remain queued and retry with capped exponential backoff.

## Quality checks

```powershell
python -m ruff check .
python -m mypy --ignore-missing-imports --namespace-packages --explicit-package-bases .
python -m pytest -q
```

The GitHub Actions workflow runs Ruff, mypy, and pytest. All three checks must pass for the workflow to succeed.

## Code navigation

- `api/main.py`: application creation, lifespan/bootstrap, router registration, health endpoint.
- `api/routes/`: HTTP endpoints for auth, alerts, cases, and events.
- `api/security.py`: bearer token validation and role dependencies.
- `application/services/`: use cases; services call repositories through a Unit of Work.
- `application/composition/dependencies.py`: configured engines, services, and selected database adapter.
- `detection/rules/`, `correlation/rules/`, `enrichment/`: pipeline capabilities.
- `infrastructure/sqlite/`, `infrastructure/postgres/`: persistence adapters and schemas.
- `frontend/src/`: React console.
- `tests/`: unit, API, and persistence tests.

## Safe contribution workflow

1. Start from an up-to-date `main` branch.
2. Make one cohesive feature or repair.
3. Add or update tests for behavior changes.
4. Run Ruff, mypy, and pytest locally.
5. Update the relevant API/architecture documentation.
6. Inspect `git status` and the diff before committing; keep `.env`, database files, caches, and virtual environments out of commits.
7. Use a clear commit message and push only after the local checks pass.

## Known limitations and next steps

- OpenSearch writes are asynchronous and may lag; the durable outbox retries failures but has no dead-letter threshold.
- OpenSearch outbox status is available to administrators at `GET /operations/opensearch-indexing`; it reports queue counts and age, but does not expose per-event contents or allow manual retry/deletion.
- PostgreSQL schema changes use ordered SQL migrations tracked in `soc_schema_migrations`. Add new immutable version files and append them to the migration registry; there is no automatic downgrade workflow.
- Event processing remains synchronous, while OpenSearch indexing runs asynchronously through a durable relational outbox. There is no dead-letter threshold yet.
- Deployment settings are for local development and need a production security review before external exposure.
- The health endpoint reports API liveness, not readiness of every dependency.

Possible next work: add metrics and alerts for sustained outbox queue growth; then harden deployment configuration.
