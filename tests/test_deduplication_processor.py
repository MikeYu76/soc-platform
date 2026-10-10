from datetime import datetime

from alert.models import Alert
from alert.processing.deduplication import DeduplicationProcessor

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_detection() -> Detection:
    event = Event(
        timestamp=datetime.now(),
        log_source="windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Failed login",
    )

    return Detection(
        rule_id="failed_login",
        title="Failed Login",
        severity=Severity.HIGH,
        event=event,
    )


def build_alert(detection: Detection) -> Alert:
    return Alert(
        title=detection.title,
        severity=detection.severity,
        source=detection,
    )


def test_empty_list_returns_empty():
    processor = DeduplicationProcessor()

    assert processor.process([]) == []


def test_unique_alerts_are_preserved():
    processor = DeduplicationProcessor()

    alert1 = build_alert(build_detection())
    alert2 = build_alert(build_detection())

    result = processor.process([alert1, alert2])

    assert len(result) == 2


def test_duplicate_detection_alerts_are_removed():
    processor = DeduplicationProcessor()

    detection = build_detection()

    alert1 = build_alert(detection)
    alert2 = build_alert(detection)

    result = processor.process([alert1, alert2])

    assert len(result) == 1
    assert result[0] == alert1


def test_first_duplicate_is_preserved():
    processor = DeduplicationProcessor()

    detection = build_detection()

    alerts = [
        build_alert(detection),
        build_alert(detection),
        build_alert(detection),
    ]

    result = processor.process(alerts)

    assert len(result) == 1