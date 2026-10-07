from common.detection import Severity
from common.event import Event
from common.event_types import EventType
from detection.rules.failed_login import FailedLoginRule


def test_failed_login_rule_matches_failed_authentication():
    # Arrange
    event = Event(
        timestamp="2026-01-01T12:00:00Z",
        log_source="windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Failed login raw event",
    )

    rule = FailedLoginRule()

    # Act
    detection = rule.match(event)

    # Assert
    assert detection is not None
    assert detection.rule_id == "AUTH-001"
    assert detection.title == "Windows Failed Login"
    assert detection.severity == Severity.MEDIUM
    assert detection.event == event


def test_failed_login_rule_ignores_other_events():
    # Arrange
    event = Event(
        timestamp="2026-01-01T12:00:00Z",
        log_source="windows",
        event_type=EventType.AUTHENTICATION_SUCCESS,
        message="Successful login",
        raw_message="Raw Windows event for successful login",
    )

    rule = FailedLoginRule()

    # Act
    detection = rule.match(event)

    # Assert
    assert detection is None