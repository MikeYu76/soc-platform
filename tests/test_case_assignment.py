from datetime import datetime

from alert.models import Alert
from case.models import Case
from case.processing.assignment import CaseAssignmentProcessor
from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from case.domain.timeline import CaseTimelineEventType


def build_case(severity: Severity) -> Case:
    event = Event(
        timestamp=datetime.now(),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Failed login",
    )

    detection = Detection(
        rule_id="failed-login",
        title="Failed Login",
        severity=severity,
        event=event,
    )

    alert = Alert(
        title="Alert",
        severity=severity,
        status=AlertStatus.NEW,
        source=detection,
    )

    return Case(
        title="Investigation",
        alert=alert,
        status=CaseStatus.NEW,
        priority=CasePriority.MEDIUM,
    )


def test_assignment_processor_creates_assignment():
    case = build_case(Severity.HIGH)

    processor = CaseAssignmentProcessor()

    processor.process([case])

    assert case.assignment is not None
    assert case.assignment.team == "Tier 2"


def test_assignment_updates_current_assignment():
    case = build_case(Severity.CRITICAL)

    CaseAssignmentProcessor().process([case])

    assert case.assigned_to == "Incident Response"
    assert case.assigned_at is not None


def test_assignment_creates_timeline_event():
    case = build_case(Severity.HIGH)

    CaseAssignmentProcessor().process([case])

    assert case.timeline[-1].event_type == CaseTimelineEventType.ASSIGNED