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


def test_filter_alerts_by_status(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = build_detection()

    new_alert = Alert(
        title="New Alert",
        severity=Severity.HIGH,
        source=detection,
        status=AlertStatus.NEW,
    )

    closed_alert = Alert(
        title="Closed Alert",
        severity=Severity.HIGH,
        source=detection,
        status=AlertStatus.CLOSED,
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.alerts.save(new_alert)
        uow.alerts.save(closed_alert)
        uow.commit()

    response = client.get(
        "/alerts",
        params={
            "status": "NEW",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["alerts"]) == 1

    alert = body["alerts"][0]

    assert alert["id"] == str(new_alert.id)
    assert alert["status"] == AlertStatus.NEW.value


def test_filter_alerts_by_severity(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    high_detection = build_detection()

    critical_event = Event(
        timestamp="2026-01-01T00:00:01Z",
        log_source="windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Critical Failed Login",
        raw_message="Critical Failed Login",
        hostname="dc01",
        username="admin",
        source_ip="1.1.1.1",
        destination_ip="10.0.0.5",
    )

    critical_detection = Detection(
        rule_id="AUTH-002",
        title="Critical Detection",
        severity=Severity.CRITICAL,
        event=critical_event,
    )

    high_alert = Alert(
        title="High Alert",
        severity=Severity.HIGH,
        source=high_detection,
    )

    critical_alert = Alert(
        title="Critical Alert",
        severity=Severity.CRITICAL,
        source=critical_detection,
    )

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.alerts.save(high_alert)
        uow.alerts.save(critical_alert)
        uow.commit()

    response = client.get(
        "/alerts",
        params={
            "severity": "critical",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["alerts"]) == 1

    alert = body["alerts"][0]

    assert alert["id"] == str(critical_alert.id)
    assert alert["severity"] == Severity.CRITICAL.value


def test_limit_alerts(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = build_detection()

    with SQLiteUnitOfWork(connection_factory) as uow:
        for i in range(3):
            alert = Alert(
                title=f"Alert {i}",
                severity=Severity.HIGH,
                source=detection,
            )
            uow.alerts.save(alert)

        uow.commit()

    response = client.get(
        "/alerts",
        params={
            "limit": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["alerts"]) == 2


def test_offset_alerts(
    client: TestClient,
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = build_detection()

    created_alerts: list[Alert] = []

    with SQLiteUnitOfWork(connection_factory) as uow:
        for i in range(3):
            alert = Alert(
                title=f"Alert {i}",
                severity=Severity.HIGH,
                source=detection,
            )
            uow.alerts.save(alert)
            created_alerts.append(alert)

        uow.commit()

    response = client.get(
        "/alerts",
        params={
            "limit": 2,
            "offset": 1,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert response.status_code == 200

    body = response.json()

    assert len(body["alerts"]) == 2

    titles = [alert["title"] for alert in body["alerts"]]

    assert titles == [
        "Alert 1",
        "Alert 0",
    ]

    assert len(body["alerts"]) == 2

    titles = [alert["title"] for alert in body["alerts"]]

    assert titles == [
        "Alert 1",
        "Alert 0",
    ]


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
    print(body)

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
