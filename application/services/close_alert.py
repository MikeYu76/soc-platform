from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from application.dto.alert import CloseAlertResponse
from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class CloseAlertService(
    ApplicationService[
        IdentifierRequest,
        CloseAlertResponse,
    ],
):
    """
    Closes an alert.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IdentifierRequest,
    ) -> CloseAlertResponse:
        with self._unit_of_work_factory() as uow:
            alert = uow.alerts.get(UUID(request.id))

            if alert is None:
                raise ResourceNotFoundError(
                    f"Alert '{request.id}' was not found."
                )

            alert.close()

            uow.alerts.update(alert)

            uow.commit()

        return CloseAlertResponse(
            alert=alert,
        )
