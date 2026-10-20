# SOC Platform Developer Handoff

## What this project is

A modular SOC workflow and portfolio project. The repository contains a FastAPI backend, React console, event detection and correlation pipeline, case/alert workflows, SQLite and PostgreSQL adapters, JWT authentication with role checks, Docker Compose configuration, and automated tests.

For the architecture, request flows, API endpoints, and design trade-offs, see:

- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/DESIGN-DECISIONS.md`

## Current status

The implemented roadmap includes event processing, detection and correlation rules, enrichment, alerts, case management (including comments, evidence, priority changes, and timeline entries), JWT login/RBAC, Docker Compose, PostgreSQL persistence, React console, and GitHub Actions quality checks.

At the previous verified checkpoint: 216 pytest tests passed; Ruff passed; local mypy passed. The GitHub Actions run for commit `3f43ec3` succeeded. CI's mypy step is currently advisory, so check its step result separately from the overall workflow status.

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

The Compose setup uses PostgreSQL and enables best-effort indexing of processed events to OpenSearch. In OpenSearch Dashboards, create a `security-events` data view using `timestamp` as the time field. The relational database is authoritative; OpenSearch indexing failures are logged and are not retried durably.

## Quality checks

```powershell
python -m ruff check .
python -m mypy --ignore-missing-imports --namespace-packages --explicit-package-bases .
python -m pytest -q
```

Expected at the last verified checkpoint: Ruff passes, mypy reports no issues, and pytest reports 216 passing tests. Re-run these after changes because this handoff records a point-in-time state.

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

- OpenSearch indexing runs after the relational transaction commits; failures are logged, and no durable outbox/retry exists yet.
- PostgreSQL schema management does not yet use a migration tool.
- CI's mypy step is advisory (`continue-on-error: true`).
- The API handles event processing synchronously; there is no durable work queue or retry mechanism.
- Deployment settings are for local development and need a production security review before external exposure.
- The health endpoint reports API liveness, not readiness of every dependency.

Possible next work: add a durable outbox/retry worker for OpenSearch indexing; add schema migrations; enforce mypy in CI; add operational metrics and dependency readiness checks; then harden deployment configuration.
