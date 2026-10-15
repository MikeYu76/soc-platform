from __future__ import annotations

from collections.abc import Callable

from application.dto.alert import ListAlertsResponse
from application.dto.base import Request
from application.services.base import ApplicationService

from repositories.unit_of_work import UnitOfWork


class ListAlertsService(
    ApplicationService[
        Request,
        ListAlertsResponse,
    ],
):
    """
    Lists all active alerts.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: Request,
    ) -> ListAlertsResponse:

        with self._unit_of_work_factory() as uow:
            alerts = uow.alerts.list_active()

        return ListAlertsResponse(
            alerts=alerts,
        )