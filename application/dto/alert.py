from __future__ import annotations

from dataclasses import dataclass

from application.dto.base import (
    Request,
    Response,
)

from alert.models import Alert


@dataclass(slots=True)
class ListAlertsResponse(Response):
    """
    Response containing active alerts.
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