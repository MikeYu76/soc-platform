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


def test_evidence_is_added():
    case = build_case()

    case.add_evidence(
        name="Security Log",
        description="Authentication log",
        source="Windows Event Log",
    )

    assert len(case.evidence) == 1
    assert case.evidence[0].name == "Security Log"


def test_evidence_creates_timeline_event():
    case = build_case()

    case.add_evidence(
        name="Security Log",
        description="Authentication log",
        source="Windows Event Log",
    )

    assert len(case.timeline) == 2
    assert case.timeline[-1].event_type == CaseTimelineEventType.EVIDENCE_ADDED


def test_evidence_source_is_stored():
    case = build_case()

    case.add_evidence(
        name="Security Log",
        description="Authentication log",
        source="Windows Event Log",
    )

    assert case.evidence[0].source == "Windows Event Log"
