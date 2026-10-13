from datetime import UTC, datetime, timedelta

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from enrichment.models import EnrichedDetection, Enrichment
from correlation.rules.impossible_travel import ImpossibleTravelRule


def make_auth_detection(
    timestamp: datetime,
    username: str,
    country: str,
    source_ip: str = "203.0.113.10",
    event_type: str = EventType.AUTHENTICATION_SUCCESS
) -> EnrichedDetection:

    event = Event(
        timestamp=timestamp,
        log_source="windows",
        event_type=event_type,
        message="Successful authentication",
        raw_message="Successful authentication",
        source_ip=source_ip,
        username=username,
    )

    detection = Detection(
        rule_id="TEST-001",
        title="Successful Login",
        severity=Severity.LOW,
        event=event,
    )

    return EnrichedDetection(
        detection=detection,
        enrichment=Enrichment(
            data={
                "ip_context": {
                    "source_ip": source_ip,
                    "country": country,
                }
            }
        ),
    )


def test_detects_impossible_travel():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)

    detections = [
        make_auth_detection(
            start,
            username="alice",
            country="United States",
        ),
        make_auth_detection(
            start + timedelta(minutes=30),
            username="alice",
            country="Germany",
        ),
    ]

    rule = ImpossibleTravelRule(window_hours=2)

    results = rule.correlate(detections)

    assert len(results) == 1
    assert results[0].rule_id == "CORR-AUTH-002"
    assert len(results[0].detections) == 2 
    

def test_does_not_detect_same_country():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)

    detections = [
        make_auth_detection(
            start,
            username="alice",
            country="United States",
        ),
        make_auth_detection(
            start + timedelta(minutes=30),
            username="alice",
            country="United States",
        ),
    ]

    rule = ImpossibleTravelRule(window_hours=2)

    assert rule.correlate(detections) == []  


def test_does_not_correlate_different_users():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)

    detections = [
        make_auth_detection(
            start,
            username="alice",
            country="United States",
        ),
        make_auth_detection(
            start + timedelta(minutes=30),
            username="bob",
            country="Germany",
        ),
    ]

    rule = ImpossibleTravelRule(window_hours=2)

    assert rule.correlate(detections) == []


def test_does_not_detect_outside_time_window():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)

    detections = [
        make_auth_detection(
            start,
            username="alice",
            country="United States",
        ),
        make_auth_detection(
            start + timedelta(hours=3),
            username="alice",
            country="Germany",
        ),
    ]

    rule = ImpossibleTravelRule(window_hours=2)

    assert rule.correlate(detections) == []


def test_ignores_failed_authentications():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)

    detections = [
        make_auth_detection(
            start,
            username="alice",
            country="United States",
            event_type=EventType.AUTHENTICATION_FAILED,
        ),
        make_auth_detection(
            start + timedelta(minutes=30),
            username="alice",
            country="Germany",
            event_type=EventType.AUTHENTICATION_FAILED,
        ),
    ]

    rule = ImpossibleTravelRule(window_hours=2)

    assert rule.correlate(detections) == []


def test_handles_unordered_input():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)

    detections = [
        make_auth_detection(
            start + timedelta(minutes=30),
            username="alice",
            country="Germany",
        ),
        make_auth_detection(
            start,
            username="alice",
            country="United States",
        ),
    ]

    rule = ImpossibleTravelRule(window_hours=2)

    results = rule.correlate(detections)

    assert len(results) == 1
    assert len(results[0].detections) == 2                    