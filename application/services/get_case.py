from __future__ import annotations

from collections.abc import Callable

from application.dto.case import GetCaseResponse
from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService

from repositories.unit_of_work import UnitOfWork


class GetCaseService(
    ApplicationService[
        IdentifierRequest,
        GetCaseResponse,
    ],
):
    """
    Retrieves a single case by its identifier.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IdentifierRequest,
    ) -> GetCaseResponse:

        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(request.id)

        if case is None:
            raise ResourceNotFoundError(
                f"Case '{request.id}' was not found."
            )

        return GetCaseResponse(
            case=case,
        )