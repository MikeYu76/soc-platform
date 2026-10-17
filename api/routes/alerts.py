from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.dependencies import (
    get_acknowledge_alert_service,
    get_close_alert_service,
    get_get_alert_service,
    get_list_alerts_service,
    get_start_alert_investigation_service,
)
from application.dto.alert import (
    AcknowledgeAlertRequest,
    AcknowledgeAlertResponse,
    CloseAlertResponse,
    GetAlertResponse,
    ListAlertsResponse,
    StartAlertInvestigationResponse,
)
from application.dto.base import Request
from application.dto.identifier import IdentifierRequest
from application.services.acknowledge_alert import AcknowledgeAlertService
from application.services.close_alert import CloseAlertService
from application.services.get_alert import GetAlertService
from application.services.list_alerts import ListAlertsService
from application.services.start_alert_investigation import (
    StartAlertInvestigationService,
)


class AcknowledgeAlertBody(BaseModel):
    """
    Request body for acknowledging an alert.
    """

    analyst: str


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


@router.patch(
    "/{id}/acknowledge",
    response_model=AcknowledgeAlertResponse,
    summary="Acknowledge an alert",
)
def acknowledge_alert(
    id: str,
    body: AcknowledgeAlertBody,
    service: AcknowledgeAlertService = Depends(
        get_acknowledge_alert_service,
    ),
) -> AcknowledgeAlertResponse:
    return service.execute(
        AcknowledgeAlertRequest(
            alert_id=id,
            analyst=body.analyst,
        )
    )


@router.patch(
    "/{id}/start",
    response_model=StartAlertInvestigationResponse,
    summary="Start investigating an alert",
)
def start_alert_investigation(
    id: str,
    service: StartAlertInvestigationService = Depends(
        get_start_alert_investigation_service,
    ),
) -> StartAlertInvestigationResponse:
    return service.execute(
        IdentifierRequest(
            id=id,
        )
    )


@router.patch(
    "/{id}/close",
    response_model=CloseAlertResponse,
    summary="Close an alert",
)
def close_alert(
    id: str,
    service: CloseAlertService = Depends(
        get_close_alert_service,
    ),
) -> CloseAlertResponse:
    return service.execute(
        IdentifierRequest(
            id=id,
        )
    )
