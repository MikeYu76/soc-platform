from __future__ import annotations

from collections.abc import Callable

from application.dto.base import Request
from application.dto.case import ListCasesResponse
from application.services.base import ApplicationService

from repositories.unit_of_work import UnitOfWork


class ListCasesService(
    ApplicationService[
        Request,
        ListCasesResponse,
    ],
):
    """
    Lists all active cases.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: Request,
    ) -> ListCasesResponse:

        with self._unit_of_work_factory() as uow:
            cases = uow.cases.list_active()

        return ListCasesResponse(
            cases=cases,
        )