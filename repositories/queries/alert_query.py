from __future__ import annotations

from dataclasses import dataclass

from common.alert_status import AlertStatus
from common.detection import Severity


@dataclass(slots=True)
class AlertQuery:
    """
    Query criteria for searching alerts.
    """

    status: AlertStatus | None = None

    severity: Severity | None = None
