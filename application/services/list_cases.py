from __future__ import annotations

from collections.abc import Callable

from application.dto.case import (
    ListCasesRequest,
    ListCasesResponse,
)
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class ListCasesService(
    ApplicationService[
        ListCasesRequest,
        ListCasesResponse,
    ],
):
    """
    Retrieves cases matching query criteria.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: ListCasesRequest,
    ) -> ListCasesResponse:
        with self._unit_of_work_factory() as uow:
            cases = uow.cases.search(
                request.query,
            )

        return ListCasesResponse(
            cases=cases,
        )
