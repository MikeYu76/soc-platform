from datetime import UTC, datetime

from alert.models import Alert
from case.immediate_case import ImmediateCaseRule
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def make_alert() -> Alert:
    detection = Detection(
        rule_id="rule",
        title="Failed Login",
        severity=Severity.HIGH,
        event=Event(
            timestamp=datetime(2025, 1, 1, 0, 0, tzinfo=UTC),
            log_source="windows",
            event_type=EventType.AUTHENTICATION_FAILED,
            message="Failed login",
            raw_message="4625 Failed login",
        ),
    )

    return Alert(
        title="Failed Login",
        severity=Severity.HIGH,
        source=detection,
    )


def test_generates_case_for_every_alert():
    rule = ImmediateCaseRule()

    alerts = [
        make_alert(),
        make_alert(),
    ]

    cases = rule.generate(alerts)

    assert len(cases) == 2


def test_case_title_matches_alert():
    rule = ImmediateCaseRule()

    alert = make_alert()

    case = rule.generate([alert])[0]

    assert case.title == alert.title


def test_case_references_original_alert():
    rule = ImmediateCaseRule()

    alert = make_alert()

    case = rule.generate([alert])[0]

    assert case.alert is alert


def test_new_cases_start_in_new_status():
    rule = ImmediateCaseRule()

    case = rule.generate([make_alert()])[0]

    assert case.status.value == "NEW"


def test_default_priority_is_medium():
    rule = ImmediateCaseRule()

    case = rule.generate([make_alert()])[0]

    assert case.priority.value == "MEDIUM"


def test_case_starts_unassigned():
    rule = ImmediateCaseRule()

    case = rule.generate([make_alert()])[0]

    assert case.assigned_to is None
    assert case.assigned_at is None


def test_case_is_not_closed_when_created():
    rule = ImmediateCaseRule()

    case = rule.generate([make_alert()])[0]

    assert case.closed_at is None
    assert case.resolution is None
