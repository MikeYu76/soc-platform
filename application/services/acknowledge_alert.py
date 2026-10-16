from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID

from application.dto.alert import (
    AcknowledgeAlertRequest,
    AcknowledgeAlertResponse,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService

from common.alert_status import AlertStatus

from repositories.unit_of_work import UnitOfWork


class AcknowledgeAlertService(
    ApplicationService[
        AcknowledgeAlertRequest,
        AcknowledgeAlertResponse,
    ],
):
    """
    Acknowledges an alert for analyst investigation.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: AcknowledgeAlertRequest,
    ) -> AcknowledgeAlertResponse:
        with self._unit_of_work_factory() as uow:
            alert = uow.alerts.get(
                UUID(request.alert_id)
            )

            if alert is None:
                raise ResourceNotFoundError(
                    f"Alert '{request.alert_id}' was not found."
                )

            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_by = request.analyst
            alert.acknowledged_at = datetime.now(UTC)

            uow.alerts.update(alert)

            uow.commit()

        return AcknowledgeAlertResponse(
            alert=alert,
        )