# API Reference

Base URL for local Compose: `http://localhost:8000`. FastAPI serves interactive docs at `/docs`, alternative docs at `/redoc`, and the OpenAPI document at `/openapi.json`. The running OpenAPI schema is authoritative if this summary differs from the implementation.

All `/alerts`, `/cases`, and `/events` routes require a valid bearer access token. `/auth/login` is public. User creation requires the Administrator role. Role-restricted operations return `403` for an authenticated user without permission; missing or invalid credentials return `401`.

## Authentication

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/login` | Exchange username and password for an access token. |
| `GET` | `/auth/me` | Return the authenticated user's public profile. |
| `POST` | `/auth/users` | Create a user; Administrator only. |

Login body:

```json
{"username":"admin","password":"your-password"}
```

The login response includes a bearer token. Send it on protected requests as `Authorization: Bearer <token>`.

Create user body:

```json
{"username":"analyst.one","password":"a-long-unique-password","role":"Analyst"}
```

Allowed role names: `Analyst`, `Senior Analyst`, `Incident Responder`, `SOC Manager`, `Administrator`. Password length is 12–256 characters; usernames are 3–64 characters and may contain letters, numbers, periods, underscores, and hyphens.

## Events

| Method | Path | Description |
|---|---|---|
| `GET` | `/events` | List persisted events. Supports event type, hostname, username, log source, source/destination IP, sort field, order, limit, and offset filters. |
| `GET` | `/events/{id}` | Retrieve one event. |
| `POST` | `/events` | Process a normalized security event through the SOC pipeline, persist it relationally, and queue it for durable OpenSearch indexing. Incident Responder, SOC Manager, or Administrator role required. |

List defaults: `limit=50`, `offset=0`, descending timestamp order. `limit` must be at least 1; `offset` must be nonnegative.

## Alerts

| Method | Path | Description | Permission |
|---|---|---|---|
| `GET` | `/alerts` | List alerts; optional `status`, `severity`, `limit`, `offset`. | Any authenticated user |
| `GET` | `/alerts/{id}` | Retrieve an alert. | Any authenticated user |
| `PATCH` | `/alerts/{id}/acknowledge` | Acknowledge an alert; body includes `analyst`. | Analyst and above |
| `PATCH` | `/alerts/{id}/start` | Start alert investigation. | Analyst and above |
| `PATCH` | `/alerts/{id}/close` | Close an alert. | Senior Analyst, Incident Responder, SOC Manager, Administrator |

Alert list defaults to `limit=50`, `offset=0`.

## Cases

| Method | Path | Description | Permission |
|---|---|---|---|
| `GET` | `/cases` | List cases; optional status, priority, assigned_to, limit, offset. | Any authenticated user |
| `GET` | `/cases/{id}` | Retrieve a case. | Any authenticated user |
| `GET` | `/cases/{id}/timeline` | Retrieve case activity history. | Any authenticated user |
| `POST` | `/cases/{id}/comments` | Add comment; body: `author`, `message`. | Analyst and above |
| `POST` | `/cases/{id}/evidence` | Add evidence; body: `name`, `description`, `source`. | Analyst and above |
| `PATCH` | `/cases/{id}/priority` | Change priority; body: `priority`, `changed_by`. | Senior Analyst, Incident Responder, SOC Manager, Administrator |
| `PATCH` | `/cases/{id}/assign` | Assign to team; body: `team`, `assigned_by`, `reason`. | Senior Analyst, Incident Responder, SOC Manager, Administrator |
| `PATCH` | `/cases/{id}/start` | Start investigation; body: `analyst`. | Analyst and above |
| `PATCH` | `/cases/{id}/resolve` | Resolve; body: `resolution_type`, `summary`, `resolved_by`. | Senior Analyst, Incident Responder, SOC Manager, Administrator |
| `PATCH` | `/cases/{id}/close` | Close; body: `closed_by`. | Senior Analyst, Incident Responder, SOC Manager, Administrator |

Case list defaults to `limit=50`, `offset=0`.

## Health

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness response with service name and version. |

The health endpoint does not authenticate. A healthy response confirms the API process responds; it is not a complete dependency-readiness report.

## Operations

| Method | Path | Description | Permission |
|---|---|---|---|
| `GET` | `/operations/opensearch-indexing` | Return OpenSearch outbox queue counts, oldest pending item age, and highest retry count. | Administrator |

The response includes `enabled`, `pending_count`, `ready_count`, `retry_wait_count`, `retrying_count`, `oldest_pending_at`, `oldest_pending_age_seconds`, and `max_attempts`. Event contents and credentials are not returned. An empty queue reports zero counts and null oldest-item fields.

## Errors and validation

FastAPI validates request bodies and query parameters. Invalid inputs produce a `422` response. Authentication failures produce `401`, role failures `403`, missing entities normally `404`, and duplicate usernames `409`. Authentication configuration problems may produce `503`. Exact response schemas are documented in `/docs`.

## Example calls

PowerShell login:

```powershell
$login = Invoke-RestMethod -Method Post -Uri http://localhost:8000/auth/login `
  -ContentType 'application/json' `
  -Body '{"username":"admin","password":"your-password"}'
$headers = @{ Authorization = "Bearer $($login.access_token)" }
Invoke-RestMethod -Uri http://localhost:8000/cases?limit=10 -Headers $headers
```

Use the response fields shown in `/docs` for the exact login token response and event request schema.


## OpenSearch event index

The Compose stack indexes processed events into the `security-events` index. OpenSearch Dashboards can inspect the index through **Discover** after creating a data view named `security-events` and selecting `timestamp` as the time field. A relational outbox is written in the same transaction as the event and processed in the background. Indexing failures are retried with capped exponential backoff; the API response can return before OpenSearch becomes searchable.
