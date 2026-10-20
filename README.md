# SOC Platform

A modular Security Operations Center (SOC) learning and portfolio project. The platform processes normalized security events through detection, enrichment, correlation, alerting, and case management. It includes a FastAPI backend, a React console, SQLite and PostgreSQL persistence adapters, authentication with role checks, and a Docker Compose development stack.

## Current capabilities

- Event ingestion and normalization, with detection and correlation rules.
- Enrichment and risk context, followed by alert generation and processing.
- Case creation and investigation workflows, comments, evidence, priority changes, and a case activity timeline.
- REST API for events, alerts, cases, and authentication.
- SQLite for local development/tests; PostgreSQL is configured for the Docker Compose stack.
- React console at `http://localhost:3000` when Compose is running.
- Processed events are indexed into OpenSearch for searching in OpenSearch Dashboards. The relational database remains the source of truth.

This is a development and portfolio project. Review the security and deployment limitations in [Design decisions](docs/DESIGN-DECISIONS.md) before using it outside a local environment.

## Start the development stack

1. Install Docker Desktop and start it.
2. Copy `.env.docker.example` to `.env` and replace every placeholder with a strong, private value. Do not commit `.env`.
3. In PowerShell, from the project directory, run:

   ```powershell
   docker compose up --build -d
   ```

4. Open the console at `http://localhost:3000`. API docs are at `http://localhost:8000/docs`; health is at `http://localhost:8000/health`. OpenSearch Dashboards is at `http://localhost:5601`.
5. Stop the stack with `docker compose down`. This preserves named data volumes. `docker compose down -v` deletes the PostgreSQL and OpenSearch volumes.

See [Docker setup](DOCKER-SETUP.txt) and [PostgreSQL setup](POSTGRESQL-SETUP.txt) for details. Compose selects PostgreSQL; running the API directly uses SQLite by default.

## Run locally without Docker

Use Python 3.12. In PowerShell from the project directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m uvicorn api.main:app --reload
```

The default local database is `soc_platform.db` (override with `SOC_DATABASE_PATH`). Authentication requires a configured `SOC_JWT_SECRET`; set a sufficiently long random secret and configure a bootstrap administrator before launching. The app exposes its interactive API documentation at `http://127.0.0.1:8000/docs`.

## Quality checks

```powershell
python -m ruff check .
python -m mypy --ignore-missing-imports --namespace-packages --explicit-package-bases .
python -m pytest -q
```

The GitHub Actions workflow runs Ruff, mypy, and pytest with coverage. Mypy is currently advisory in CI (`continue-on-error`) while it is being adopted; keep it passing locally and update that workflow setting when the project decides to make it blocking.

## Documentation

- [Architecture and event sequence](docs/ARCHITECTURE.md)
- [API reference](docs/API.md) (the live OpenAPI schema at `/openapi.json` is authoritative)
- [Design decisions and trade-offs](docs/DESIGN-DECISIONS.md)
- [Developer handoff](docs/HANDOFF.md)

## Project layout`r`n`r`n```text`r`napi/                  FastAPI routes, security, and exception mapping`r`napplication/          Use cases, DTOs, settings, dependency composition`r`nalert/, case/,        Security domain models, rules, and processing`r`ncorrelation/,`r`ndetection/, enrichment/`r`ninfrastructure/        SQLite and PostgreSQL adapters, schemas, mappers`r`nrepositories/          Repository and Unit of Work abstractions`r`nnormalization/         Raw event normalization`r`nfrontend/              React SOC console`r`nDockerfile, compose.yaml  Local multi-service development environment`r`ntests/                  Unit, API, and persistence tests`r`ndocs/                   Architecture, API, decisions, and handoff`r`n```

## License

No license is currently declared. Contact the repository owner before reusing or distributing this project.


