from fastapi.testclient import TestClient

from alert.models import Alert
from common.alert_status import AlertStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


def build_detection() -> Detection:
    """
    Build a sample detection for alert API tests.
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

    return Detection(
        rule_id="AUTH-001",
        title="Windows Failed Login",
        severity=Severity.HIGH,
        event=event,
    )


def test_list_alerts(
    client: TestClient,
) -> None:
    payload = {
        "event": {
            "timestamp": "2026-01-01T00:00:00Z",
            "log_source": "windows",
            "event_type": "authentication_failed",
            "message": "Failed login",
            "raw_message": "User admin failed to log in.",
            "hostname": "dc01",
            "username": "admin",
            "source_ip": "8.8.8.8",
            "destination_ip": "10.0.0.5",
        }
    }

    process_response = client.post(
        "/events",
        json=payload,
    )

    assert process_response.status_code == 200

    response = client.get("/alerts")

    assert response.status_code == 200

    body = response.json()

    assert "alerts" in body
    assert isinstance(body["alerts"], list)


def test_acknowledge_alert(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = build_detection()

    alert = Alert(
        title="Windows Failed Login",
        severity=Severity.HIGH,
        source=detection,
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.alerts.save(alert)
        uow.commit()

    response = client.patch(
        f"/alerts/{alert.id}/acknowledge",
        json={
            "analyst": "alice",
        },
    )

    assert response.status_code == 200

    body = response.json()

    acknowledged = body["alert"]

    assert acknowledged["id"] == str(alert.id)
    assert acknowledged["status"] == AlertStatus.ACKNOWLEDGED.value
    assert acknowledged["acknowledged_by"] == "alice"
    assert acknowledged["acknowledged_at"] is not None


def test_start_alert_investigation(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = build_detection()

    alert = Alert(
        title="Windows Failed Login",
        severity=Severity.HIGH,
        source=detection,
        status=AlertStatus.ACKNOWLEDGED,
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.alerts.save(alert)
        uow.commit()

    response = client.patch(
        f"/alerts/{alert.id}/start",
    )

    assert response.status_code == 200

    body = response.json()

    started = body["alert"]

    assert started["id"] == str(alert.id)
    assert started["status"] == AlertStatus.IN_PROGRESS.value


def test_close_alert(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = build_detection()

    alert = Alert(
        title="Windows Failed Login",
        severity=Severity.HIGH,
        source=detection,
        status=AlertStatus.IN_PROGRESS,
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.alerts.save(alert)
        uow.commit()

    response = client.patch(
        f"/alerts/{alert.id}/close",
    )

    assert response.status_code == 200

    body = response.json()

    closed = body["alert"]

    assert closed["id"] == str(alert.id)
    assert closed["status"] == AlertStatus.CLOSED.value
