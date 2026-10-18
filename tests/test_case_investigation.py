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


def build_assigned_case() -> Case:
    case = build_case()

    case.assign(
        team="Tier 2",
        assigned_by="system",
        reason="Automatic routing",
    )

    return case


def test_case_can_start_investigation():
    case = build_assigned_case()

    case.start_investigation(
        analyst="alice",
    )

    assert case.status == CaseStatus.IN_PROGRESS


def test_start_investigation_creates_timeline_event():
    case = build_assigned_case()

    case.start_investigation(
        analyst="alice",
    )

    assert (
        case.timeline[-1].event_type
        == CaseTimelineEventType.INVESTIGATION_STARTED
    )
    assert case.timeline[-1].actor == "alice"


@pytest.mark.parametrize(
    "status",
    [
        CaseStatus.NEW,
        CaseStatus.IN_PROGRESS,
        CaseStatus.RESOLVED,
        CaseStatus.CLOSED,
    ],
)
def test_start_investigation_rejects_invalid_states(
    status: CaseStatus,
):
    case = build_case(
        status=status,
    )

    with pytest.raises(InvalidCaseStateError):
        case.start_investigation(
            analyst="alice",
        )
