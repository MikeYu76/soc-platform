from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.case import (
    AddCaseCommentRequest,
    AddCaseCommentResponse,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class AddCaseCommentService(
    ApplicationService[
        AddCaseCommentRequest,
        AddCaseCommentResponse,
    ],
):
    """Adds an analyst comment to a case and persists the updated case."""

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: AddCaseCommentRequest,
    ) -> AddCaseCommentResponse:
        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(UUID(request.case_id))

            if case is None:
                raise ResourceNotFoundError(
                    f"Case '{request.case_id}' was not found."
                )

            case.add_comment(
                author=request.author,
                message=request.message,
            )

            uow.cases.update(case)
            uow.commit()

        return AddCaseCommentResponse(case=case)
