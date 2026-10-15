from __future__ import annotations

from fastapi import APIRouter, Depends

from api.dependencies import (
    get_get_alert_service,
    get_list_alerts_service,
)

from application.dto.base import Request
from application.dto.identifier import IdentifierRequest

from application.dto.alert import (
    GetAlertResponse,
    ListAlertsResponse,
)

from application.services.get_alert import (
    GetAlertService,
)
from application.services.list_alerts import (
    ListAlertsService,
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get(
    "",
    response_model=ListAlertsResponse,
    summary="List active alerts",
)
def list_alerts(
    service: ListAlertsService = Depends(
        get_list_alerts_service,
    ),
) -> ListAlertsResponse:
    return service.execute(
        Request(),
    )


@router.get(
    "/{id}",
    response_model=GetAlertResponse,
    summary="Retrieve an alert",
)
def get_alert(
    id: str,
    service: GetAlertService = Depends(
        get_get_alert_service,
    ),
) -> GetAlertResponse:
    return service.execute(
        IdentifierRequest(
            id=id,
        )
    )