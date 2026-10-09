
from datetime import datetime
from pydantic import BaseModel, Field

from common.event import Event


class CorrelationResult(BaseModel):
    """A pattern identified across multiple security events."""

    correlation_id: str
    rule_id: str
    title: str
    matched_at: datetime
    events: list[Event] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)