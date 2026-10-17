from __future__ import annotations

from collections.abc import Callable

from application.dto.alert import GetAlertResponse
from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class GetAlertService(
    ApplicationService[
        IdentifierRequest,
        GetAlertResponse,
    ],
):
    """
    Retrieves a single alert by its identifier.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: IdentifierRequest,
    ) -> GetAlertResponse:

        with self._unit_of_work_factory() as uow:
            alert = uow.alerts.get(request.id)

        if alert is None:
            raise ResourceNotFoundError(f"Alert '{request.id}' was not found.")

        return GetAlertResponse(
            alert=alert,
        )
