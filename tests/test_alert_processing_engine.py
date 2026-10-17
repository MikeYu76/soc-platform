from datetime import datetime

from alert.models import Alert
from alert.processing.base import AlertProcessor
from alert.processing.engine import AlertProcessingEngine
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_detection(severity: Severity = Severity.HIGH) -> Detection:
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


def build_alert() -> Alert:
    detection = build_detection()

    return Alert(
        title=detection.title,
        severity=detection.severity,
        source=detection,
    )


class PassThroughProcessor(AlertProcessor):
    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        return alerts


class DuplicateProcessor(AlertProcessor):
    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        return alerts + alerts


class EmptyProcessor(AlertProcessor):
    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        return []


def test_no_processors_returns_original_alerts():
    alerts = [build_alert()]

    engine = AlertProcessingEngine([])

    result = engine.process(alerts)

    assert result == alerts


def test_single_processor_runs():
    alerts = [build_alert()]

    engine = AlertProcessingEngine(
        [
            PassThroughProcessor(),
        ]
    )

    result = engine.process(alerts)

    assert result == alerts


def test_processors_execute_in_order():
    alerts = [build_alert()]

    engine = AlertProcessingEngine(
        [
            DuplicateProcessor(),
            EmptyProcessor(),
        ]
    )

    result = engine.process(alerts)

    assert result == []


def test_multiple_processors_chain_results():
    alerts = [build_alert()]

    engine = AlertProcessingEngine(
        [
            DuplicateProcessor(),
        ]
    )

    result = engine.process(alerts)

    assert len(result) == 2
