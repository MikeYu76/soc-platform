import pytest

from common.detection import Detection
from common.event import Event
from common.event_types import EventType
from common.severity import Severity

from detection.base import DetectionRule
from detection.engine import DetectionEngine


class NoMatchRule(DetectionRule):
    def match(self, event: Event) -> Detection | None:
        return None


class MatchRule(DetectionRule):
    def match(self, event: Event) -> Detection | None:
        return Detection(
            rule_id="Test-001",
            title="Test Detection",
            severity=Severity.LOW,
            event=event,
        )


class AnotherMatchRule(DetectionRule):
    def match(self, event: Event) -> Detection | None:
        return Detection(
            rule_id="Test-002",
            title="Another Test Detection",
            severity=Severity.MEDIUM,
            event=event,
        )


@pytest.fixture
def sample_event() -> Event:
    return Event(
        timestamp="2026-01-01T12:00:00Z",
        log_source="windows",
        event_type=EventType.UNKNOWN,
        message="Test event",
        raw_message="Test event",
    )


def test_detection_engine_with_no_rules_returns_empty_list(sample_event: Event):
    # Arrange
    engine = DetectionEngine([])

    # Act
    detections = engine.process(sample_event)

    # Assert
    assert detections == []


def test_detection_engine_returns_empty_list_when_no_rules_match(
    sample_event: Event,
):
    # Arrange
    engine = DetectionEngine([NoMatchRule()])

    # Act
    detections = engine.process(sample_event)

    # Assert
    assert detections == []


def test_detection_engine_returns_detection_when_rule_matches(
    sample_event: Event,
):
    # Arrange
    engine = DetectionEngine([MatchRule()])

    # Act
    detections = engine.process(sample_event)

    # Assert
    assert len(detections) == 1

    detection = detections[0]

    assert detection.rule_id == "Test-001"
    assert detection.title == "Test Detection"
    assert detection.severity == Severity.LOW
    assert detection.event == sample_event


def test_detection_engine_returns_all_matching_detections(
    sample_event: Event,
):
    # Arrange
    engine = DetectionEngine([
        MatchRule(),
        AnotherMatchRule(),
    ])

    # Act
    detections = engine.process(sample_event)

    # Assert
    assert len(detections) == 2

    assert detections[0].rule_id == "Test-001"
    assert detections[1].rule_id == "Test-002"