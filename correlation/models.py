from datetime import datetime

from pydantic import BaseModel, Field

from common.detection import Severity
from enrichment.models import EnrichedDetection


class CorrelationResult(BaseModel):
    """
    Represents a security pattern identified across multiple
    enriched detections.

    Correlation rules assign an appropriate severity to each
    result. Downstream components, such as the Alert layer,
    preserve this severity rather than redefining it.
    """

    correlation_id: str
    rule_id: str
    title: str
    severity: Severity
    matched_at: datetime
    detections: list[EnrichedDetection] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
