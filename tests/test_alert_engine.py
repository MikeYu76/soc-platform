from datetime import datetime

from alert.base import AlertRule
from alert.engine import AlertEngine
from alert.models import Alert

from common.alert_status import AlertStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType

from correlation.models import CorrelationResult


class NoOpAlertRule(AlertRule):
    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        return []

    def from_detection(
        self,
        detection: Detection,
    ) -> Alert | None:
        return None

    def from_correlation(
        self,
        correlation: CorrelationResult,
    ) -> Alert | None:
        return None


class StaticAlertRule(AlertRule):
    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        return [
            alert
            for detection in detections
            if (alert := self.from_detection(detection)) is not None
        ]

    def from_detection(
        self,
        detection: Detection,
    ) -> Alert | None:
        return Alert(
            title="Test Alert",
            severity=Severity.HIGH,
            source=detection,
        )

    def from_correlation(
        self,
        correlation: CorrelationResult,
    ) -> Alert | None:
        return None


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


def test_engine_returns_empty_when_no_rules_match():
    detection = build_detection()

    engine = AlertEngine([NoOpAlertRule()])

    alerts = engine.generate([detection], [])

    assert alerts == []


def test_engine_returns_alerts_from_rule():
    detection = build_detection()

    engine = AlertEngine([StaticAlertRule()])

    alerts = engine.generate([detection], [])

    assert len(alerts) == 1

    alert = alerts[0]

    assert alert.title == "Test Alert"
    assert alert.severity == Severity.HIGH
    assert alert.status == AlertStatus.NEW
    assert alert.source == detection


def test_engine_merges_results_from_multiple_rules():
    detection = build_detection()

    engine = AlertEngine(
        [
            StaticAlertRule(),
            StaticAlertRule(),
        ]
    )

    alerts = engine.generate([detection], [])

    assert len(alerts) == 2

    assert all(
        alert.title == "Test Alert"
        for alert in alerts
    )