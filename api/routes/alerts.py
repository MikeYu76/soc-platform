from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from api.dependencies import (
    get_acknowledge_alert_service,
    get_close_alert_service,
    get_get_alert_service,
    get_list_alerts_service,
    get_start_alert_investigation_service,
)
from api.security import get_current_user, require_roles
from application.dto.alert import (
    AcknowledgeAlertRequest,
    AcknowledgeAlertResponse,
    CloseAlertResponse,
    GetAlertResponse,
    ListAlertsRequest,
    ListAlertsResponse,
    StartAlertInvestigationResponse,
)
from application.dto.identifier import IdentifierRequest
from application.services.acknowledge_alert import AcknowledgeAlertService
from application.services.close_alert import CloseAlertService
from application.services.get_alert import GetAlertService
from application.services.list_alerts import ListAlertsService
from application.services.start_alert_investigation import (
    StartAlertInvestigationService,
)
from common.alert_status import AlertStatus
from common.detection import Severity
from common.user_role import UserRole
from identity.user import User
from repositories.queries.alert_query import AlertQuery


class AcknowledgeAlertBody(BaseModel):
    """
    Request body for acknowledging an alert.
    """

    analyst: str


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=ListAlertsResponse,
    summary="List alerts",
)
def list_alerts(
    status: AlertStatus | None = Query(
        default=None,
        description="Filter by alert status.",
    ),
    severity: Severity | None = Query(
        default=None,
        description="Filter by alert severity.",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        description="Maximum number of alerts to return.",
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of alerts to skip.",
    ),
    service: ListAlertsService = Depends(
        get_list_alerts_service,
    ),
) -> ListAlertsResponse:
    """
    Retrieve persisted alerts.
    """
    return service.execute(
        ListAlertsRequest(
            query=AlertQuery(
                status=status,
                severity=severity,
                limit=limit,
                offset=offset,
            ),
        )
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
    """
    Retrieve an alert by its internal identifier.
    """
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
    _user: User = Depends(
        require_roles(
            UserRole.ANALYST,
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> AcknowledgeAlertResponse:
    """
    Acknowledge an alert.
    """
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
    _user: User = Depends(
        require_roles(
            UserRole.ANALYST,
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> StartAlertInvestigationResponse:
    """
    Start investigating an alert.
    """
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
    _user: User = Depends(
        require_roles(
            UserRole.SENIOR_ANALYST,
            UserRole.INCIDENT_RESPONDER,
            UserRole.SOC_MANAGER,
            UserRole.ADMINISTRATOR,
        )
    ),
) -> CloseAlertResponse:
    """
    Close an alert.
    """
    return service.execute(
        IdentifierRequest(
            id=id,
        )
    )
