from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.case import AssignCaseRequest, AssignCaseResponse
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class AssignCaseService(
    ApplicationService[
        AssignCaseRequest,
        AssignCaseResponse,
    ],
):
    """
    Assigns a case to an analyst team.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: AssignCaseRequest,
    ) -> AssignCaseResponse:
        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(UUID(request.case_id))

            if case is None:
                raise ResourceNotFoundError(
                    f"Case '{request.case_id}' was not found."
                )

            case.assign(
                team=request.team,
                assigned_by=request.assigned_by,
                reason=request.reason,
            )

            uow.cases.update(case)

            uow.commit()

        return AssignCaseResponse(
            case=case,
        )
