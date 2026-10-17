from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path

from application.dto.ingest_event import IngestEventRequest
from application.services.ingest_event import IngestEventService
from common.event import Event
from common.event_types import EventType
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


def make_event() -> Event:
    return Event(
        timestamp=datetime.now(UTC),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Event 4625",
    )


def test_ingest_event() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        factory = SQLiteConnectionFactory(str(Path(tmpdir) / "test.db"))

        service = IngestEventService(lambda: SQLiteUnitOfWork(factory))

        event = make_event()

        request = IngestEventRequest(
            event=event,
        )

        result = service.execute(request)

        with SQLiteUnitOfWork(factory) as uow:
            loaded = uow.events.get(event.id)

        assert result == event
        assert loaded == event
