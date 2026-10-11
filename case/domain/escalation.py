from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class CaseEscalation(BaseModel):
    """
    Represents the escalation of a case to a higher support level.
    """

    level: int

    team: str

    reason: str

    escalated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )