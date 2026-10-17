from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class CaseAssignment(BaseModel):
    team: str

    assigned_by: str

    reason: str

    assigned_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
