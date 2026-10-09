
from datetime import datetime, timedelta, UTC

from common.event import Event
from common.event_types import EventType
from correlation.failed_login_burst import FailedLoginBurstRule


def make_failed_login(
    timestamp: datetime,
    source_ip: str = "203.0.113.10",
    username: str = "alice",
    event_type: str = EventType.AUTHENTICATION_FAILED,
) -> Event:
    return Event(
        timestamp=timestamp,
        log_source="windows",
        event_type=event_type,
        message="Authentication attempt",
        raw_message="Authentication attempt",
        source_ip=source_ip,
        username=username,
    )


def test_detects_failed_login_burst():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)
    events = [
        make_failed_login(start + timedelta(seconds=30 * i))
        for i in range(5)
    ]

    rule = FailedLoginBurstRule(threshold=5, window_minutes=5)

    results = rule.correlate(events)

    assert len(results) == 1
    assert results[0].rule_id == "CORR-AUTH-001"
    assert results[0].metadata["source_ip"] == "203.0.113.10"
    assert results[0].metadata["attempt_count"] == 5
    assert len(results[0].events) == 5


def test_does_not_detect_below_threshold():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)
    events = [
        make_failed_login(start + timedelta(seconds=30 * i))
        for i in range(4)
    ]

    rule = FailedLoginBurstRule(threshold=5, window_minutes=5)

    assert rule.correlate(events) == []


def test_does_not_correlate_different_source_ips():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)
    events = [
        make_failed_login(
            start + timedelta(seconds=i),
            source_ip=f"203.0.113.{i + 1}",
        )
        for i in range(5)
    ]

    rule = FailedLoginBurstRule(threshold=5, window_minutes=5)

    assert rule.correlate(events) == []


def test_ignores_successful_logins():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)
    events = [
        make_failed_login(start + timedelta(seconds=i))
        for i in range(4)
    ]
    events.append(
        make_failed_login(
            start + timedelta(seconds=4),
            event_type=EventType.AUTHENTICATION_SUCCESS,
        )
    )

    rule = FailedLoginBurstRule(threshold=5, window_minutes=5)

    assert rule.correlate(events) == []


def test_does_not_correlate_attempts_outside_window():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)
    events = [
        make_failed_login(start + timedelta(minutes=2 * i))
        for i in range(5)
    ]

    rule = FailedLoginBurstRule(threshold=5, window_minutes=5)

    assert rule.correlate(events) == []


def test_result_contains_only_threshold_events():
    start = datetime(2026, 10, 9, 10, 0, tzinfo=UTC)
    events = [
        make_failed_login(start + timedelta(seconds=10 * i))
        for i in range(8)
    ]

    rule = FailedLoginBurstRule(threshold=5, window_minutes=5)

    results = rule.correlate(events)

    assert len(results) == 1
    assert len(results[0].events) == 5
    assert results[0].metadata["attempt_count"] == 5