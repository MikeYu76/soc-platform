from __future__ import annotations

from dataclasses import dataclass, field

from alert.models import Alert
from application.dto.base import Request, Response
from repositories.queries.alert_query import AlertQuery


@dataclass(slots=True)
class ListAlertsRequest(Request):
    """
    Request to retrieve alerts.
    """

    query: AlertQuery = field(
        default_factory=AlertQuery,
    )


@dataclass(slots=True)
class ListAlertsResponse(Response):
    """
    Response containing alerts.
    """

    alerts: list[Alert]


@dataclass(slots=True)
class GetAlertResponse(Response):
    """
    Response containing a single alert.
    """

    alert: Alert


@dataclass(slots=True)
class AcknowledgeAlertRequest(Request):
    """
    Request to acknowledge an alert.
    """

    alert_id: str

    analyst: str


@dataclass(slots=True)
class AcknowledgeAlertResponse(Response):
    """
    Response after acknowledging an alert.
    """

    alert: Alert


@dataclass(slots=True)
class StartAlertInvestigationResponse(Response):
    """
    Response after starting an alert investigation.
    """

    alert: Alert


@dataclass(slots=True)
class CloseAlertResponse(Response):
    """
    Response after closing an alert.
    """

    alert: Alert
