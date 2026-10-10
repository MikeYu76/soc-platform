from alert.models import Alert

from case.immediate_case import ImmediateCaseRule
from case.processing.assignment import CaseAssignmentProcessor

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def make_case(severity: Severity):
    detection = Detection(
        rule_id="rule",
        title="Detection",
        severity=severity,
        event=Event(
            timestamp="2025-01-01T00:00:00Z",
            log_source="windows",
            event_type=EventType.AUTHENTICATION_FAILED,
            message="Failed login",
            raw_message="4625 Failed Login",
        ),
    )

    alert = Alert(
        title="Alert",
        severity=severity,
        source=detection,
    )

    return ImmediateCaseRule().generate([alert])[0]


def test_routes_low_case():
    processor = CaseAssignmentProcessor()

    case = make_case(Severity.LOW)

    result = processor.process([case])

    assert result[0].metadata["assigned_team"] == "Tier 1"


def test_routes_medium_case():
    processor = CaseAssignmentProcessor()

    case = make_case(Severity.MEDIUM)

    result = processor.process([case])

    assert result[0].metadata["assigned_team"] == "Tier 1"


def test_routes_high_case():
    processor = CaseAssignmentProcessor()

    case = make_case(Severity.HIGH)

    result = processor.process([case])

    assert result[0].metadata["assigned_team"] == "Tier 2"


def test_routes_critical_case():
    processor = CaseAssignmentProcessor()

    case = make_case(Severity.CRITICAL)

    result = processor.process([case])

    assert (
        result[0].metadata["assigned_team"]
        == "Incident Response"
    )


def test_returns_same_case_instance():
    processor = CaseAssignmentProcessor()

    case = make_case(Severity.HIGH)

    result = processor.process([case])

    assert result[0] is case