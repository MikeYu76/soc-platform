from __future__ import annotations

from collections.abc import Callable

from application.dto.alert import (
    ListAlertsRequest,
    ListAlertsResponse,
)
from application.services.base import ApplicationService
from repositories.unit_of_work import UnitOfWork


class ListAlertsService(
    ApplicationService[
        ListAlertsRequest,
        ListAlertsResponse,
    ],
):
    """
    Retrieves alerts matching query criteria.
    """

    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(
        self,
        request: ListAlertsRequest,
    ) -> ListAlertsResponse:
        with self._unit_of_work_factory() as uow:
            alerts = uow.alerts.search(
                request.query,
            )

        return ListAlertsResponse(
            alerts=alerts,
        )
