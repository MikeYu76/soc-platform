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
        title="Failed Login Alert",
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


def test_routes_low_case():
    case = build_case(Severity.LOW)

    CaseAssignmentProcessor().process([case])

    assert case.assignment is not None
    assert case.assignment.team == "Tier 1"
    assert case.assigned_to == "Tier 1"


def test_routes_medium_case():
    case = build_case(Severity.MEDIUM)

    CaseAssignmentProcessor().process([case])

    assert case.assignment is not None
    assert case.assignment.team == "Tier 1"
    assert case.assigned_to == "Tier 1"


def test_routes_high_case():
    case = build_case(Severity.HIGH)

    CaseAssignmentProcessor().process([case])

    assert case.assignment is not None
    assert case.assignment.team == "Tier 2"
    assert case.assigned_to == "Tier 2"


def test_routes_critical_case():
    case = build_case(Severity.CRITICAL)

    CaseAssignmentProcessor().process([case])

    assert case.assignment is not None
    assert case.assignment.team == "Incident Response"
    assert case.assigned_to == "Incident Response"