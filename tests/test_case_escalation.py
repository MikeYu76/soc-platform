from datetime import UTC, datetime

from alert.models import Alert

from case.models import Case
from case.domain.timeline import CaseTimelineEventType

from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_case() -> Case:
    event = Event(
        timestamp=datetime.now(UTC),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Failed login",
    )

    detection = Detection(
        rule_id="failed-login",
        title="Failed Login",
        severity=Severity.HIGH,
        event=event,
    )

    alert = Alert(
        title="Failed Login Alert",
        severity=Severity.HIGH,
        status=AlertStatus.NEW,
        source=detection,
    )

    return Case(
        title="Investigation",
        alert=alert,
        status=CaseStatus.NEW,
        priority=CasePriority.HIGH,
    )


def test_case_escalation_is_created():
    case = build_case()

    case.escalate(
        level=2,
        team="Tier 2",
        reason="SLA breached.",
    )

    assert case.escalation is not None
    assert case.escalation.level == 2
    assert case.escalation.team == "Tier 2"
    assert case.escalation.reason == "SLA breached."


def test_assigned_team_is_updated():
    case = build_case()

    case.escalate(
        level=2,
        team="Tier 2",
        reason="SLA breached.",
    )

    assert case.assigned_to == "Tier 2"
    assert case.assigned_at == case.escalation.escalated_at


def test_escalation_adds_timeline_event():
    case = build_case()

    case.escalate(
        level=2,
        team="Tier 2",
        reason="SLA breached.",
    )

    event = case.timeline[-1]

    assert event.event_type == CaseTimelineEventType.ESCALATED
    assert event.description == "Escalated to Tier 2 (Level 2)."