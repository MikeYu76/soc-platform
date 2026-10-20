from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from threading import Event

from opensearchpy.exceptions import OpenSearchException

from repositories.event_indexer import EventIndexer
from repositories.unit_of_work import UnitOfWork

logger = logging.getLogger(__name__)


def process_pending_event_indexes(
    unit_of_work_factory: Callable[[], UnitOfWork],
    event_indexer: EventIndexer,
    *,
    batch_size: int = 25,
) -> int:
    """Deliver one batch of due outbox entries and return attempt count."""
    with unit_of_work_factory() as uow:
        pending = uow.event_index_outbox.get_pending(batch_size)
        entries = [
            (entry, uow.events.get(entry.event_id))
            for entry in pending
        ]

    attempted = 0
    for entry, event in entries:
        if event is None:
            logger.error(
                "OpenSearch outbox references a missing event",
                extra={"event_id": entry.event_id},
            )
            with unit_of_work_factory() as uow:
                uow.event_index_outbox.mark_delivered(entry.event_id)
                uow.commit()
            continue

        attempted += 1
        try:
            event_indexer.index(event)
        except OpenSearchException as exc:
            delay_seconds = min(2 ** min(entry.attempts, 9), 300)
            next_attempt = datetime.now(UTC) + timedelta(seconds=delay_seconds)
            error_type = type(exc).__name__
            with unit_of_work_factory() as uow:
                uow.event_index_outbox.schedule_retry(
                    entry.event_id,
                    next_attempt.isoformat(),
                    error_type,
                )
                uow.commit()
            logger.warning(
                "OpenSearch indexing failed; retry scheduled",
                extra={
                    "event_id": entry.event_id,
                    "attempt": entry.attempts + 1,
                    "retry_delay_seconds": delay_seconds,
                    "error_type": error_type,
                },
            )
        else:
            with unit_of_work_factory() as uow:
                uow.event_index_outbox.mark_delivered(entry.event_id)
                uow.commit()

    return attempted


def run_event_index_outbox_worker(
    unit_of_work_factory: Callable[[], UnitOfWork],
    event_indexer: EventIndexer,
    stop_event: Event,
    *,
    poll_interval_seconds: float = 2.0,
    batch_size: int = 25,
) -> None:
    """Poll durable indexing work until the API asks this worker to stop."""
    while not stop_event.is_set():
        try:
            process_pending_event_indexes(
                unit_of_work_factory,
                event_indexer,
                batch_size=batch_size,
            )
        except Exception:
            logger.exception("OpenSearch outbox worker iteration failed")
        stop_event.wait(poll_interval_seconds)
