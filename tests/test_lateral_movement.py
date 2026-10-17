from datetime import UTC, datetime, timedelta

import pytest

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from correlation.rules.lateral_movement import LateralMovementRule
from enrichment.models import EnrichedDetection, Enrichment


def make_detection(
    *,
    username: str,
    hostname: str,
    timestamp: datetime,
) -> EnrichedDetection:
    detection = Detection(
        rule_id="AUTH-001",
        title="Successful Login",
        severity=Severity.LOW,
        event=Event(
            timestamp=timestamp,
            log_source="windows",
            event_type=EventType.AUTHENTICATION_SUCCESS,
            message="Successful login",
            raw_message="4624",
            username=username,
            hostname=hostname,
        ),
    )

    return EnrichedDetection(
        detection=detection,
        enrichment=Enrichment(),
    )


def test_invalid_threshold_raises():
    with pytest.raises(ValueError):
        LateralMovementRule(
            threshold=1,
        )


def test_invalid_window_raises():
    with pytest.raises(ValueError):
        LateralMovementRule(
            window_minutes=0,
        )


def test_empty_input_returns_no_results():
    rule = LateralMovementRule()

    assert rule.correlate([]) == []


def test_below_threshold_returns_no_results():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now,
        ),
        make_detection(
            username="alice",
            hostname="FILE01",
            timestamp=now + timedelta(minutes=5),
        ),
    ]

    rule = LateralMovementRule(
        threshold=3,
    )

    results = rule.correlate(
        detections,
    )

    assert results == []


def test_multiple_hosts_within_window_produces_result():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now,
        ),
        make_detection(
            username="alice",
            hostname="FILE01",
            timestamp=now + timedelta(minutes=5),
        ),
        make_detection(
            username="alice",
            hostname="DC01",
            timestamp=now + timedelta(minutes=10),
        ),
    ]

    rule = LateralMovementRule()

    results = rule.correlate(
        detections,
    )

    assert len(results) == 1

    result = results[0]

    assert result.rule_id == "CORR-AUTH-003"
    assert result.title == "Possible Lateral Movement"
    assert result.severity == Severity.HIGH

    assert result.metadata["username"] == "alice"
    assert result.metadata["host_count"] == 3

    assert sorted(
        result.metadata["hosts"],
    ) == [
        "DC01",
        "FILE01",
        "PC01",
    ]


def test_same_host_multiple_times_does_not_trigger():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now,
        ),
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now + timedelta(minutes=2),
        ),
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now + timedelta(minutes=4),
        ),
    ]

    rule = LateralMovementRule()

    results = rule.correlate(
        detections,
    )

    assert results == []


def test_events_outside_window_do_not_trigger():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now,
        ),
        make_detection(
            username="alice",
            hostname="FILE01",
            timestamp=now + timedelta(minutes=45),
        ),
        make_detection(
            username="alice",
            hostname="DC01",
            timestamp=now + timedelta(minutes=90),
        ),
    ]

    rule = LateralMovementRule()

    results = rule.correlate(
        detections,
    )

    assert results == []


def test_multiple_users_are_processed_independently():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            username="alice",
            hostname="PC01",
            timestamp=now,
        ),
        make_detection(
            username="alice",
            hostname="FILE01",
            timestamp=now + timedelta(minutes=5),
        ),
        make_detection(
            username="alice",
            hostname="DC01",
            timestamp=now + timedelta(minutes=10),
        ),
        make_detection(
            username="bob",
            hostname="WEB01",
            timestamp=now,
        ),
    ]

    rule = LateralMovementRule()

    results = rule.correlate(
        detections,
    )

    assert len(results) == 1
    assert results[0].metadata["username"] == "alice"
