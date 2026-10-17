from __future__ import annotations

from collections.abc import Callable

from application.dto.ingest_event import IngestEventRequest
from application.services.base import ApplicationService
from common.event import Event
from repositories.unit_of_work import UnitOfWork


class IngestEventService(
    ApplicationService[
        IngestEventRequest,
        Event,
    ],
):
    """
    Persists a normalized security event.

    This is the application entry point for ingesting
    events into the platform.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IngestEventRequest,
    ) -> Event:
        event = request.event

        with self._unit_of_work_factory() as uow:
            uow.events.save(event)
            uow.commit()

        return event
