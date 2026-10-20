from datetime import UTC, datetime

from alert.models import Alert
from alert.processing.routing import AlertRoutingProcessor
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def make_alert(severity: Severity) -> Alert:
    detection = Detection(
        rule_id="rule",
        title="Test Detection",
        severity=severity,
        event=Event(
            timestamp=datetime(2025, 1, 1, 0, 0, tzinfo=UTC),
            log_source="windows",
            event_type=EventType.AUTHENTICATION_FAILED,
            message="Failed login",
            raw_message="4625 Failed login",
        ),
    )

    return Alert(
        title="Alert",
        severity=severity,
        source=detection,
    )


def test_routes_low_alert():
    processor = AlertRoutingProcessor()

    alert = make_alert(Severity.LOW)

    result = processor.process([alert])

    assert result[0].metadata["route"] == "Tier 1"


def test_routes_medium_alert():
    processor = AlertRoutingProcessor()

    alert = make_alert(Severity.MEDIUM)

    result = processor.process([alert])

    assert result[0].metadata["route"] == "Tier 1"


def test_routes_high_alert():
    processor = AlertRoutingProcessor()

    alert = make_alert(Severity.HIGH)

    result = processor.process([alert])

    assert result[0].metadata["route"] == "Tier 2"


def test_routes_critical_alert():
    processor = AlertRoutingProcessor()

    alert = make_alert(Severity.CRITICAL)

    result = processor.process([alert])

    assert result[0].metadata["route"] == "Incident Response"


def test_returns_same_alert_objects():
    processor = AlertRoutingProcessor()

    alert = make_alert(Severity.HIGH)

    result = processor.process([alert])

    assert result[0] is alert
