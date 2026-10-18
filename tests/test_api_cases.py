from fastapi.testclient import TestClient

from alert.models import Alert
from case.models import Case
from common.alert_status import AlertStatus
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


def build_case() -> Case:
    """
    Build a sample case for Case API tests.
    """

    event = Event(
        timestamp="2026-01-01T00:00:00Z",
        log_source="windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="User admin failed to log in.",
        hostname="dc01",
        username="admin",
        source_ip="8.8.8.8",
        destination_ip="10.0.0.5",
    )

    detection = Detection(
        rule_id="AUTH-001",
        title="Windows Failed Login",
        severity=Severity.HIGH,
        event=event,
    )

    alert = Alert(
        title="Windows Failed Login",
        severity=Severity.HIGH,
        status=AlertStatus.NEW,
        source=detection,
    )

    return Case(
        title="Windows Failed Login Investigation",
        alert=alert,
    )


def test_list_cases(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.get("/cases")

    assert response.status_code == 200

    body = response.json()

    assert "cases" in body
    assert isinstance(body["cases"], list)
    assert len(body["cases"]) == 1
    assert body["cases"][0]["id"] == str(case.id)


def test_get_case(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.get(f"/cases/{case.id}")

    assert response.status_code == 200

    body = response.json()

    returned = body["case"]

    assert returned["id"] == str(case.id)
    assert returned["title"] == case.title
    assert returned["status"] == CaseStatus.NEW.value


def test_assign_case(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.patch(
        f"/cases/{case.id}/assign",
        json={
            "team": "Tier 2",
            "assigned_by": "alice",
            "reason": "High severity authentication activity",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assigned = body["case"]

    assert assigned["id"] == str(case.id)
    assert assigned["status"] == CaseStatus.ASSIGNED.value
    assert assigned["assigned_to"] == "Tier 2"
    assert assigned["assigned_at"] is not None
    assert assigned["assignment"] is not None


def test_start_case_investigation(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    case.assign(
        team="Tier 2",
        assigned_by="alice",
        reason="High severity authentication activity",
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.patch(
        f"/cases/{case.id}/start",
        json={
            "analyst": "alice",
        },
    )

    assert response.status_code == 200

    body = response.json()

    started = body["case"]

    assert started["id"] == str(case.id)
    assert started["status"] == CaseStatus.IN_PROGRESS.value


def test_resolve_case(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    case.assign(
        team="Tier 2",
        assigned_by="alice",
        reason="High severity authentication activity",
    )

    case.start_investigation(
        analyst="alice",
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.patch(
        f"/cases/{case.id}/resolve",
        json={
            "resolution_type": "False Positive",
            "summary": "Expected administrator activity.",
            "resolved_by": "alice",
        },
    )

    assert response.status_code == 200

    body = response.json()

    resolved = body["case"]

    assert resolved["id"] == str(case.id)
    assert resolved["status"] == CaseStatus.RESOLVED.value
    assert resolved["resolution"] is not None
    assert resolved["closed_at"] is not None


def test_close_case(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = build_case()

    case.assign(
        team="Tier 2",
        assigned_by="alice",
        reason="High severity authentication activity",
    )

    case.start_investigation(
        analyst="alice",
    )

    case.resolve(
        resolution_type="False Positive",
        summary="Expected administrator activity.",
        resolved_by="alice",
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    response = client.patch(
        f"/cases/{case.id}/close",
        json={
            "closed_by": "alice",
        },
    )

    assert response.status_code == 200

    body = response.json()

    closed = body["case"]

    assert closed["id"] == str(case.id)
    assert closed["status"] == CaseStatus.CLOSED.value
    assert closed["closed_at"] is not None
