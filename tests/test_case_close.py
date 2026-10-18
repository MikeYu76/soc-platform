from datetime import datetime

import pytest

from alert.models import Alert
from case.domain.timeline import CaseTimelineEventType
from case.exceptions import InvalidCaseStateError
from case.models import Case
from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_case(
    status: CaseStatus = CaseStatus.NEW,
) -> Case:
    event = Event(
        timestamp=datetime.now(),
        log_source="Windows",
        event_type=EventType.AUTHENTICATION_FAILED,
        message="Failed login",
        raw_message="Failed login",
    )

    detection = Detection(
        rule_id="failed-login",
        title="Failed Login",
        severity=Severity.HIGH,
        event=event,
    )

    alert = Alert(
        title="Alert",
        severity=Severity.HIGH,
        status=AlertStatus.NEW,
        source=detection,
    )

    return Case(
        title="Investigation",
        alert=alert,
        status=status,
        priority=CasePriority.MEDIUM,
    )


def build_resolved_case() -> Case:
    case = build_case()

    case.assign(
        team="Tier 2",
        assigned_by="system",
        reason="Automatic routing",
    )

    case.start_investigation(
        analyst="alice",
    )

    case.resolve(
        resolution_type="False Positive",
        summary="Expected administrator activity.",
        resolved_by="alice",
    )

    return case


def test_case_can_be_closed():
    case = build_resolved_case()

    case.close(
        closed_by="alice",
    )

    assert case.status == CaseStatus.CLOSED
    assert case.closed_at is not None


def test_close_creates_timeline_event():
    case = build_resolved_case()

    case.close(
        closed_by="alice",
    )

    assert case.timeline[-1].event_type == CaseTimelineEventType.CLOSED
    assert case.timeline[-1].actor == "alice"


@pytest.mark.parametrize(
    "status",
    [
        CaseStatus.NEW,
        CaseStatus.ASSIGNED,
        CaseStatus.IN_PROGRESS,
        CaseStatus.CLOSED,
    ],
)
def test_close_rejects_invalid_states(
    status: CaseStatus,
) -> None:
    case = build_case(
        status=status,
    )

    with pytest.raises(InvalidCaseStateError):
        case.close(
            closed_by="alice",
        )
