from datetime import datetime

import pytest

from alert.immediate_detection import ImmediateDetectionAlertRule

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_detection(severity: Severity) -> Detection:
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
        severity=severity,
        event=event,
    )


@pytest.mark.parametrize(
    ("severity", "expected"),
    [
        (Severity.LOW, False),
        (Severity.MEDIUM, False),
        (Severity.HIGH, True),
        (Severity.CRITICAL, True),
    ],
)
def test_generates_alerts_above_default_threshold(
    severity: Severity,
    expected: bool,
):
    detection = build_detection(severity)

    rule = ImmediateDetectionAlertRule()

    alerts = rule.generate([detection], [])

    assert (len(alerts) == 1) is expected


def test_generated_alert_preserves_detection():
    detection = build_detection(Severity.CRITICAL)

    rule = ImmediateDetectionAlertRule()

    alerts = rule.generate([detection], [])

    assert len(alerts) == 1

    alert = alerts[0]

    assert alert.source == detection
    assert alert.title == detection.title
    assert alert.severity == detection.severity


def test_custom_threshold():
    detections = [
        build_detection(Severity.MEDIUM),
        build_detection(Severity.HIGH),
    ]

    rule = ImmediateDetectionAlertRule(
        minimum_severity=Severity.MEDIUM,
    )

    alerts = rule.generate(detections, [])

    assert len(alerts) == 2