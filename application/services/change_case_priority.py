from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.case import (
    ChangeCasePriorityRequest,
    ChangeCasePriorityResponse,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from common.case_priority import CasePriority
from repositories.unit_of_work import UnitOfWork


class ChangeCasePriorityService(
    ApplicationService[
        ChangeCasePriorityRequest,
        ChangeCasePriorityResponse,
    ],
):
    """Changes a case priority and persists its timeline event."""

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: ChangeCasePriorityRequest,
    ) -> ChangeCasePriorityResponse:
        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(UUID(request.case_id))

            if case is None:
                raise ResourceNotFoundError(
                    f"Case '{request.case_id}' was not found."
                )

            case.change_priority(
                priority=CasePriority(request.priority),
                changed_by=request.changed_by,
            )

            uow.cases.update(case)
            uow.commit()

        return ChangeCasePriorityResponse(case=case)
