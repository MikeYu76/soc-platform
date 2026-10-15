from __future__ import annotations

from dataclasses import dataclass

from alert.models import Alert

from application.dto.base import Response


@dataclass(slots=True)
class GetAlertResponse(Response):
    """
    Response returned when retrieving a single alert.
    """

    alert: Alert


@dataclass(slots=True)
class ListAlertsResponse(Response):
    """
    Response returned when listing alerts.
    """

    alerts: list[Alert]