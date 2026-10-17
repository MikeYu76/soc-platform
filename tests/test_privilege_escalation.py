from datetime import UTC, datetime, timedelta

import pytest

from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType
from correlation.rules.privilege_escalation import PrivilegeEscalationRule
from enrichment.models import EnrichedDetection, Enrichment


def make_detection(
    *,
    event_type: EventType,
    username: str = "alice",
    hostname: str = "workstation-01",
    timestamp: datetime | None = None,
    process_name: str | None = None,
    command_line: str | None = None,
    message: str = "",
) -> EnrichedDetection:

    if timestamp is None:
        timestamp = datetime.now(UTC)

    event = Event(
        timestamp=timestamp,
        log_source="windows",
        event_type=event_type,
        message=message,
        raw_message=message,
        username=username,
        hostname=hostname,
        process_name=process_name,
        command_line=command_line,
    )

    detection = Detection(
        rule_id="TEST-001",
        title="Test Detection",
        severity=Severity.LOW,
        event=event,
    )

    return EnrichedDetection(
        detection=detection,
        enrichment=Enrichment(),
    )


def test_invalid_window_raises_value_error():
    with pytest.raises(ValueError):
        PrivilegeEscalationRule(window_minutes=0)


def test_empty_input_returns_no_results():
    rule = PrivilegeEscalationRule()

    assert rule.correlate([]) == []


def test_login_only_returns_no_results():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            event_type=EventType.AUTHENTICATION_SUCCESS,
            timestamp=now,
        )
    ]

    rule = PrivilegeEscalationRule()

    assert rule.correlate(detections) == []


def test_process_only_returns_no_results():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            event_type=EventType.PROCESS_CREATED,
            timestamp=now,
            process_name="runas.exe",
            command_line="runas /user:Administrator cmd.exe",
        )
    ]

    rule = PrivilegeEscalationRule()

    assert rule.correlate(detections) == []


def test_detects_privilege_escalation():
    now = datetime.now(UTC)

    login = make_detection(
        event_type=EventType.AUTHENTICATION_SUCCESS,
        timestamp=now,
    )

    process = make_detection(
        event_type=EventType.PROCESS_CREATED,
        timestamp=now + timedelta(minutes=2),
        process_name="runas.exe",
        command_line="runas /user:Administrator cmd.exe",
    )

    rule = PrivilegeEscalationRule()

    results = rule.correlate(
        [
            login,
            process,
        ]
    )

    assert len(results) == 1

    result = results[0]

    assert result.rule_id == "CORR-PRIV-001"
    assert result.title == "Possible Privilege Escalation"
    assert result.severity == Severity.HIGH
    assert result.detections == [login, process]

    assert result.metadata["username"] == "alice"
    assert result.metadata["hostname"] == "workstation-01"
    assert result.metadata["process"] == "runas.exe"


def test_outside_time_window_returns_no_results():
    now = datetime.now(UTC)

    login = make_detection(
        event_type=EventType.AUTHENTICATION_SUCCESS,
        timestamp=now,
    )

    process = make_detection(
        event_type=EventType.PROCESS_CREATED,
        timestamp=now + timedelta(minutes=20),
        process_name="runas.exe",
        command_line="runas administrator",
    )

    rule = PrivilegeEscalationRule(
        window_minutes=10,
    )

    assert (
        rule.correlate(
            [
                login,
                process,
            ]
        )
        == []
    )


def test_different_host_returns_no_results():
    now = datetime.now(UTC)

    login = make_detection(
        event_type=EventType.AUTHENTICATION_SUCCESS,
        timestamp=now,
        hostname="host-1",
    )

    process = make_detection(
        event_type=EventType.PROCESS_CREATED,
        timestamp=now + timedelta(minutes=2),
        hostname="host-2",
        process_name="sudo",
        command_line="sudo su",
    )

    rule = PrivilegeEscalationRule()

    assert (
        rule.correlate(
            [
                login,
                process,
            ]
        )
        == []
    )


def test_different_user_returns_no_results():
    now = datetime.now(UTC)

    login = make_detection(
        event_type=EventType.AUTHENTICATION_SUCCESS,
        username="alice",
        timestamp=now,
    )

    process = make_detection(
        event_type=EventType.PROCESS_CREATED,
        username="bob",
        timestamp=now + timedelta(minutes=2),
        process_name="sudo",
        command_line="sudo su",
    )

    rule = PrivilegeEscalationRule()

    assert (
        rule.correlate(
            [
                login,
                process,
            ]
        )
        == []
    )


def test_process_without_privilege_indicator_returns_no_results():
    now = datetime.now(UTC)

    login = make_detection(
        event_type=EventType.AUTHENTICATION_SUCCESS,
        timestamp=now,
    )

    process = make_detection(
        event_type=EventType.PROCESS_CREATED,
        timestamp=now + timedelta(minutes=2),
        process_name="notepad.exe",
        command_line="notepad.exe",
    )

    rule = PrivilegeEscalationRule()

    assert (
        rule.correlate(
            [
                login,
                process,
            ]
        )
        == []
    )


def test_multiple_users_only_matching_user_generates_result():
    now = datetime.now(UTC)

    detections = [
        make_detection(
            event_type=EventType.AUTHENTICATION_SUCCESS,
            username="alice",
            timestamp=now,
        ),
        make_detection(
            event_type=EventType.PROCESS_CREATED,
            username="alice",
            timestamp=now + timedelta(minutes=2),
            process_name="sudo",
            command_line="sudo su",
        ),
        make_detection(
            event_type=EventType.AUTHENTICATION_SUCCESS,
            username="bob",
            timestamp=now,
        ),
        make_detection(
            event_type=EventType.PROCESS_CREATED,
            username="bob",
            timestamp=now + timedelta(minutes=2),
            process_name="python.exe",
            command_line="python script.py",
        ),
    ]

    rule = PrivilegeEscalationRule()

    results = rule.correlate(detections)

    assert len(results) == 1
    assert results[0].metadata["username"] == "alice"
