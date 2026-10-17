from __future__ import annotations

from collections.abc import Callable

from application.dto.get_event import GetEventResponse
from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class GetEventService(
    ApplicationService[
        IdentifierRequest,
        GetEventResponse,
    ],
):
    """
    Retrieves a single event.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IdentifierRequest,
    ) -> GetEventResponse:

        with self._unit_of_work_factory() as uow:
            event = uow.events.get(request.id)

        if event is None:
            raise ResourceNotFoundError(f"Event '{request.id}' was not found.")

        return GetEventResponse(
            event=event,
        )
