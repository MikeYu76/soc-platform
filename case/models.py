from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from alert.models import Alert
from case.domain.assignment import CaseAssignment
from case.domain.comment import CaseComment
from case.domain.evidence import CaseEvidence
from case.domain.escalation import CaseEscalation
from case.domain.resolution import CaseResolution
from case.domain.sla import CaseSLA
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

    id: UUID = Field(default_factory=uuid4)

    title: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    status: CaseStatus = CaseStatus.NEW

    priority: CasePriority = CasePriority.MEDIUM

    alert: Alert

    assigned_to: str | None = None

    assigned_at: datetime | None = None

    assignment: CaseAssignment | None = None

    escalation: CaseEscalation | None = None

    closed_at: datetime | None = None

    resolution: CaseResolution | None = None

    sla: CaseSLA | None = None

    timeline: list[CaseTimelineEvent] = Field(default_factory=list)

    comments: list[CaseComment] = Field(default_factory=list)

    evidence: list[CaseEvidence] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def initialize_timeline(self) -> "Case":
        if not self.timeline:
            self._add_timeline_event(
                event_type=CaseTimelineEventType.CASE_CREATED,
                description="Case created.",
            )

        return self

    def _add_timeline_event(
        self,
        event_type: CaseTimelineEventType,
        description: str,
        actor: str | None = None,
    ) -> None:
        """
        Records a timeline event for the case.
        """
        self.timeline.append(
            CaseTimelineEvent(
                event_type=event_type,
                description=description,
                actor=actor,
            )
        )

    def add_comment(
        self,
        author: str,
        message: str,
    ) -> None:
        comment = CaseComment(
            author=author,
            message=message,
        )

        self.comments.append(comment)

        self._add_timeline_event(
            event_type=CaseTimelineEventType.COMMENT_ADDED,
            description=f"Comment added by {author}.",
            actor=author,
        )

    def add_evidence(
        self,
        name: str,
        description: str,
        source: str,
    ) -> None:
        evidence = CaseEvidence(
            name=name,
            description=description,
            source=source,
        )

        self.evidence.append(evidence)

        self._add_timeline_event(
            event_type=CaseTimelineEventType.EVIDENCE_ADDED,
            description=f"Evidence '{name}' added.",
        )

    def assign(
        self,
        team: str,
        assigned_by: str,
        reason: str,
    ) -> None:
        assignment = CaseAssignment(
            team=team,
            assigned_by=assigned_by,
            reason=reason,
        )

        self.assignment = assignment
        self.assigned_to = team
        self.assigned_at = assignment.assigned_at
        self.status = CaseStatus.ASSIGNED

        self._add_timeline_event(
            event_type=CaseTimelineEventType.ASSIGNED,
            description=f"Assigned to {team}.",
            actor=assigned_by,
        )

    def start_investigation(
        self,
        analyst: str,
    ) -> None:
        self.status = CaseStatus.IN_PROGRESS

        self._add_timeline_event(
            event_type=CaseTimelineEventType.INVESTIGATION_STARTED,
            description="Investigation started.",
            actor=analyst,
        )

    def escalate(
        self,
        level: int,
        team: str,
        reason: str,
    ) -> None:
        escalation = CaseEscalation(
            level=level,
            team=team,
            reason=reason,
        )

        self.escalation = escalation
        self.assigned_to = team
        self.assigned_at = escalation.escalated_at

        self._add_timeline_event(
            event_type=CaseTimelineEventType.ESCALATED,
            description=f"Escalated to {team} (Level {level}).",
        )

    def resolve(
        self,
        resolution_type: str,
        summary: str,
        resolved_by: str,
    ) -> None:
        resolution = CaseResolution(
            resolution_type=resolution_type,
            summary=summary,
            resolved_by=resolved_by,
        )

        self.resolution = resolution
        self.status = CaseStatus.RESOLVED
        self.closed_at = resolution.resolved_at

        self._add_timeline_event(
            event_type=CaseTimelineEventType.RESOLVED,
            description=f"Case resolved: {resolution_type}.",
            actor=resolved_by,
        )

    def close(
        self,
        closed_by: str,
    ) -> None:
        self.status = CaseStatus.CLOSED
        self.closed_at = datetime.now(UTC)

        self._add_timeline_event(
            event_type=CaseTimelineEventType.CLOSED,
            description="Case closed.",
            actor=closed_by,
        )