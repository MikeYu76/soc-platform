from __future__ import annotations

from datetime import UTC, datetime

import pytest

from alert.models import Alert
from case.models import Case

from common.alert_status import AlertStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType

from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


import tempfile
from pathlib import Path

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
        rule_id="failed-login",
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
        alert=make_alert(),
    )


def test_save_and_get_case(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = make_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)

    with SQLiteUnitOfWork(connection_factory) as uow:
        loaded = uow.cases.get(case.case_id)

    assert loaded is not None
    assert loaded.case_id == case.case_id
    assert loaded.title == case.title
    assert loaded.status == case.status
    assert loaded.priority == case.priority