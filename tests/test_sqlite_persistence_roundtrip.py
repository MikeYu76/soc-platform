from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest

from alert.models import Alert
from case.models import Case
from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


@pytest.fixture
def connection_factory() -> SQLiteConnectionFactory:
    with tempfile.TemporaryDirectory() as tmpdir:
        database = Path(tmpdir) / "test.db"
        yield SQLiteConnectionFactory(str(database))


def make_event() -> Event:
    return Event(
        timestamp=datetime.now(UTC),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Event 4625",
    )


def make_detection() -> Detection:
    return Detection(
        rule_id="failed-login-burst",
        title="Failed Login Burst",
        severity=Severity.HIGH,
        event=make_event(),
    )


def make_alert() -> Alert:
    return Alert(
        title="Failed Login Alert",
        severity=Severity.HIGH,
        status=AlertStatus.NEW,
        source=make_detection(),
    )


def make_case() -> Case:
    return Case(
        title="Investigate Failed Login",
        priority=CasePriority.HIGH,
        status=CaseStatus.NEW,
        alert=make_alert(),
    )


def test_event_roundtrip(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    event = make_event()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.events.save(event)

    with SQLiteUnitOfWork(connection_factory) as uow:
        loaded = uow.events.get(event.id)

    assert loaded is not None
    assert loaded == event


def test_detection_roundtrip(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    detection = make_detection()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.detections.save(detection)

    with SQLiteUnitOfWork(connection_factory) as uow:
        loaded = uow.detections.get(
            detection.id,
        )

    assert loaded is not None
    assert loaded == detection


def test_alert_roundtrip(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    alert = make_alert()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.alerts.save(alert)

    with SQLiteUnitOfWork(connection_factory) as uow:
        loaded = uow.alerts.get(
            alert.id,
        )

    assert loaded is not None
    assert loaded == alert


def test_case_roundtrip(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = make_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)

    with SQLiteUnitOfWork(connection_factory) as uow:
        loaded = uow.cases.get(
            case.id,
        )

    assert loaded is not None
    assert loaded == case
