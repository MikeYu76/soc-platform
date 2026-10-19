from __future__ import annotations

from collections.abc import Callable

from application.dto.case import GetCaseTimelineResponse
from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class GetCaseTimelineService(
    ApplicationService[
        IdentifierRequest,
        GetCaseTimelineResponse,
    ],
):
    """
    Retrieves the timeline for a single case.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IdentifierRequest,
    ) -> GetCaseTimelineResponse:
        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(request.id)

        if case is None:
            raise ResourceNotFoundError(
                f"Case '{request.id}' was not found."
            )

        return GetCaseTimelineResponse.from_domain(
            case.timeline,
        )

