from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class CaseResolution(BaseModel):
    resolution_type: str

    summary: str

    resolved_by: str

    resolved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
