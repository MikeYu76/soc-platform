from __future__ import annotations

import tempfile
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest

from application.dto.get_event import GetEventResponse
from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.get_event import GetEventService
from common.event import Event
from common.event_types import EventType
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


@pytest.fixture
def connection_factory() -> Iterator[SQLiteConnectionFactory]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield SQLiteConnectionFactory(
            str(Path(tmpdir) / "test.db"),
        )


def make_event() -> Event:
    return Event(
        event_id="EVENT-001",
        timestamp=datetime.now(UTC),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Event 4625",
    )


def test_get_existing_event(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    event = make_event()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.events.save(event)

    service = GetEventService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
    )

    response = service.execute(
        IdentifierRequest(
            id=event.id,
        )
    )

    assert response == GetEventResponse(
        event=event,
    )


def test_missing_event_raises_exception(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    service = GetEventService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
    )

    with pytest.raises(ResourceNotFoundError):
        service.execute(
            IdentifierRequest(
                id="does-not-exist",
            )
        )
