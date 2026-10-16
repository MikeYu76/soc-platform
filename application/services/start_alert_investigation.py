from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.alert import (
    StartAlertInvestigationResponse,
)
from application.dto.identifier import (
    IdentifierRequest,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService

from common.alert_status import AlertStatus

from repositories.unit_of_work import UnitOfWork


class StartAlertInvestigationService(
    ApplicationService[
        IdentifierRequest,
        StartAlertInvestigationResponse,
    ],
):
    """
    Starts analyst investigation of an acknowledged alert.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IdentifierRequest,
    ) -> StartAlertInvestigationResponse:

        with self._unit_of_work_factory() as uow:
            alert = uow.alerts.get(
                UUID(request.id),
            )

            if alert is None:
                raise ResourceNotFoundError(
                    f"Alert '{request.id}' was not found."
                )

            alert.status = AlertStatus.IN_PROGRESS

            uow.alerts.update(alert)

            uow.commit()

        return StartAlertInvestigationResponse(
            alert=alert,
        )