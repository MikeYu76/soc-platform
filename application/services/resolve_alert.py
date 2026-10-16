from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID

from application.dto.alert import (
    ResolveAlertRequest,
    ResolveAlertResponse,
)
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService

from common.alert_status import AlertStatus

from repositories.unit_of_work import UnitOfWork


class ResolveAlertService(
    ApplicationService[
        ResolveAlertRequest,
        ResolveAlertResponse,
    ],
):
    """
    Marks an alert as resolved.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: ResolveAlertRequest,
    ) -> ResolveAlertResponse:
        with self._unit_of_work_factory() as uow:
            alert = uow.alerts.get(
                UUID(request.alert_id),
            )

            if alert is None:
                raise ResourceNotFoundError(
                    f"Alert '{request.alert_id}' was not found."
                )

            alert.status = AlertStatus.RESOLVED

            alert.metadata["resolution"] = request.resolution
            alert.metadata["resolved_at"] = (
                datetime.now(UTC).isoformat()
            )

            uow.alerts.update(alert)

            uow.commit()

        return ResolveAlertResponse(
            alert=alert,
        )