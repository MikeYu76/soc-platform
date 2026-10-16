from __future__ import annotations

from collections.abc import Callable

from application.dto.list_events import (
    ListEventsRequest,
    ListEventsResponse,
)
from application.services.base import ApplicationService

from repositories.unit_of_work import UnitOfWork


class ListEventsService(
    ApplicationService[
        ListEventsRequest,
        ListEventsResponse,
    ],
):
    """
    Retrieves persisted security events.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: ListEventsRequest,
    ) -> ListEventsResponse:

        with self._unit_of_work_factory() as uow:
            events = uow.events.search(
                request.query,
            )

        return ListEventsResponse(
            events=events,
        )