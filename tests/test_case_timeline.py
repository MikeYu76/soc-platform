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


def test_case_starts_with_creation_event():
    case = build_case()

    assert len(case.timeline) == 1


def test_creation_event_type():
    case = build_case()

    assert case.timeline[0].event_type == CaseTimelineEventType.CASE_CREATED


def test_creation_event_has_timestamp():
    case = build_case()

    assert case.timeline[0].occurred_at is not None


def test_creation_event_has_description():
    case = build_case()

    assert case.timeline[0].description == "Case created."
