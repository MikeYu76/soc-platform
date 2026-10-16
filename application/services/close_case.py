from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.case import (
    CloseCaseRequest,
    CloseCaseResponse,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService

from repositories.unit_of_work import UnitOfWork


class CloseCaseService(
    ApplicationService[
        CloseCaseRequest,
        CloseCaseResponse,
    ],
):
    """
    Closes a case.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: CloseCaseRequest,
    ) -> CloseCaseResponse:
        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(
                UUID(request.case_id),
            )

            if case is None:
                raise ResourceNotFoundError(
                    f"Case '{request.case_id}' was not found."
                )

            case.close(
                closed_by=request.closed_by,
            )

            uow.cases.save(case)

            uow.commit()

        return CloseCaseResponse(
            case=case,
        )