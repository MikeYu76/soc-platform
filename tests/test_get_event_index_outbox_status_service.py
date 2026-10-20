from datetime import UTC, datetime, timedelta

from application.services.get_event_index_outbox_status import (
    GetEventIndexOutboxStatusService,
)
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


def test_status_reports_pending_and_retrying_events(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.event_index_outbox.enqueue("event-ready")
        uow.event_index_outbox.enqueue("event-retrying")
        uow.event_index_outbox.schedule_retry(
            "event-retrying",
            (datetime.now(UTC) + timedelta(minutes=1)).isoformat(),
            "ConnectionError",
        )

    service = GetEventIndexOutboxStatusService(
        lambda: SQLiteUnitOfWork(connection_factory),
        enabled=True,
    )
    response = service.execute()

    assert response.enabled is True
    assert response.pending_count == 2
    assert response.ready_count == 1
    assert response.retry_wait_count == 1
    assert response.retrying_count == 1
    assert response.oldest_pending_at is not None
    assert response.oldest_pending_age_seconds is not None
    assert response.max_attempts == 1


def test_status_for_empty_queue_and_disabled_indexing(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    service = GetEventIndexOutboxStatusService(
        lambda: SQLiteUnitOfWork(connection_factory),
        enabled=False,
    )

    response = service.execute()

    assert response.enabled is False
    assert response.pending_count == 0
    assert response.ready_count == 0
    assert response.retry_wait_count == 0
    assert response.retrying_count == 0
    assert response.oldest_pending_at is None
    assert response.oldest_pending_age_seconds is None
    assert response.max_attempts == 0
