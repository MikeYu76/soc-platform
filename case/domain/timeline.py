from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CaseTimelineEventType(StrEnum):
    CASE_CREATED = "CASE_CREATED"
    ASSIGNED = "ASSIGNED"
    INVESTIGATION_STARTED = "INVESTIGATION_STARTED"
    ESCALATED = "ESCALATED"
    COMMENT_ADDED = "COMMENT_ADDED"
    EVIDENCE_ADDED = "EVIDENCE_ADDED"
    PRIORITY_CHANGED = "PRIORITY_CHANGED"
    SLA_BREACHED = "SLA_BREACHED"
    STATUS_CHANGED = "STATUS_CHANGED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class CaseTimelineEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)

    event_type: CaseTimelineEventType

    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    description: str

    actor: str | None = None
