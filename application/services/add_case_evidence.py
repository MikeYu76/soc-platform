from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.case import (
    AddCaseEvidenceRequest,
    AddCaseEvidenceResponse,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class AddCaseEvidenceService(
    ApplicationService[
        AddCaseEvidenceRequest,
        AddCaseEvidenceResponse,
    ],
):
    """Adds evidence to a case and persists the updated case."""

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: AddCaseEvidenceRequest,
    ) -> AddCaseEvidenceResponse:
        with self._unit_of_work_factory() as uow:
            case = uow.cases.get(UUID(request.case_id))

            if case is None:
                raise ResourceNotFoundError(
                    f"Case '{request.case_id}' was not found."
                )

            case.add_evidence(
                name=request.name,
                description=request.description,
                source=request.source,
            )

            uow.cases.update(case)
            uow.commit()

        return AddCaseEvidenceResponse(case=case)
