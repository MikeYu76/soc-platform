from datetime import datetime

from pydantic import BaseModel, Field

from enrichment.models import EnrichedDetection

class CorrelationResult(BaseModel):
    """A pattern identified across multiple enriched detections."""

    correlation_id: str
    rule_id: str
    title: str
    matched_at: datetime
    detections: list[EnrichedDetection] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)

