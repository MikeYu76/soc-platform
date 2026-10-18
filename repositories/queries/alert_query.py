from __future__ import annotations

from common.alert_status import AlertStatus
from common.detection import Severity
from repositories.queries.base import Query


class AlertQuery(Query):
    """
    Query criteria for searching alerts.
    """

    status: AlertStatus | None = None

    severity: Severity | None = None
