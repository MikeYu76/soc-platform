from datetime import datetime

from alert.models import Alert
from case.domain.timeline import CaseTimelineEventType
from case.models import Case
from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_case() -> Case:
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
        title="Failed Login Alert",
        severity=Severity.HIGH,
        status=AlertStatus.NEW,
        source=detection,
    )

    return Case(
        title="Investigation",
        alert=alert,
        status=CaseStatus.NEW,
        priority=CasePriority.MEDIUM,
    )


def test_comment_is_added():
    case = build_case()

    case.add_comment(author="alice", message="Investigating.")

    assert len(case.comments) == 1
    assert case.comments[0].author == "alice"
    assert case.comments[0].message == "Investigating."


def test_comment_creates_timeline_event():
    case = build_case()

    case.add_comment(author="alice", message="Investigating.")

    assert len(case.timeline) == 2

    assert case.timeline[-1].event_type == CaseTimelineEventType.COMMENT_ADDED


def test_timeline_actor_matches_author():
    case = build_case()

    case.add_comment(author="alice", message="Investigating.")

    assert case.timeline[-1].actor == "alice"
