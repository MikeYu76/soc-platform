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
        title="Alert",
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


def test_case_can_be_resolved():
    case = build_case()

    case.resolve(
        resolution_type="False Positive",
        summary="Expected administrator activity.",
        resolved_by="alice",
    )

    assert case.resolution is not None
    assert case.resolution.resolution_type == "False Positive"


def test_resolution_updates_case_status():
    case = build_case()

    case.resolve(
        resolution_type="False Positive",
        summary="Expected administrator activity.",
        resolved_by="alice",
    )

    assert case.status == CaseStatus.RESOLVED
    assert case.closed_at is not None


def test_resolution_creates_timeline_event():
    case = build_case()

    case.resolve(
        resolution_type="False Positive",
        summary="Expected administrator activity.",
        resolved_by="alice",
    )

    assert case.timeline[-1].event_type == CaseTimelineEventType.RESOLVED
    assert case.timeline[-1].actor == "alice"
