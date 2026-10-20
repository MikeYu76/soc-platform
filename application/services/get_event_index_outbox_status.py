from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime

from application.dto.event_index_outbox import (
    GetEventIndexOutboxStatusResponse,
)
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class GetEventIndexOutboxStatusService(
    ApplicationService[None, GetEventIndexOutboxStatusResponse],
):
    """Reads queue health without exposing individual event contents."""

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
        *,
        enabled: bool,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._enabled = enabled

    def execute(
        self,
        request: None = None,
    ) -> GetEventIndexOutboxStatusResponse:
        del request
        with self._unit_of_work_factory() as uow:
            status = uow.event_index_outbox.get_status()

        oldest_pending_at = (
            datetime.fromisoformat(status.oldest_created_at)
            if status.oldest_created_at is not None
            else None
        )
        if oldest_pending_at is not None and oldest_pending_at.tzinfo is None:
            oldest_pending_at = oldest_pending_at.replace(tzinfo=UTC)

        now = datetime.now(UTC)
        oldest_age_seconds = (
            max(0.0, (now - oldest_pending_at.astimezone(UTC)).total_seconds())
            if oldest_pending_at is not None
            else None
        )
        return GetEventIndexOutboxStatusResponse(
            enabled=self._enabled,
            pending_count=status.pending_count,
            ready_count=status.ready_count,
            retry_wait_count=status.retry_wait_count,
            retrying_count=status.retrying_count,
            oldest_pending_at=oldest_pending_at,
            oldest_pending_age_seconds=oldest_age_seconds,
            max_attempts=status.max_attempts,
        )
