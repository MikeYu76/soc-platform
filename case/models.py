from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from alert.models import Alert
from case.domain.timeline import (
    CaseTimelineEvent,
    CaseTimelineEventType,
)
from common.case_priority import CasePriority
from common.case_status import CaseStatus


class Case(BaseModel):
    """
    Represents an analyst investigation.
    """

    case_id: UUID = Field(default_factory=uuid4)

    title: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    status: CaseStatus = CaseStatus.NEW

    priority: CasePriority = CasePriority.MEDIUM

    alert: Alert

    assigned_to: str | None = None

    assigned_at: datetime | None = None

    closed_at: datetime | None = None

    resolution: str | None = None

    timeline: list[CaseTimelineEvent] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def initialize_timeline(self) -> "Case":
        if not self.timeline:
            self.timeline.append(
                CaseTimelineEvent(
                    event_type=CaseTimelineEventType.CASE_CREATED,
                    description="Case created.",
                )
            )

        return self