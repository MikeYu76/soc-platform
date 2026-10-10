from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from common.alert_status import AlertStatus
from common.detection import Detection
from common.detection import Detection, Severity
from correlation.models import CorrelationResult


class Alert(BaseModel):
    """
    Represents an analyst-facing security alert.

    Alerts are generated from either individual detections
    or correlation results and represent work items that
    should be investigated by a security analyst.
    """

    alert_id: UUID = Field(default_factory=uuid4)

    title: str

    severity: Severity

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    status: AlertStatus = AlertStatus.NEW

    source: Detection | CorrelationResult

    metadata: dict[str, Any] = Field(default_factory=dict)