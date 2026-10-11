from datetime import datetime

from alert.models import Alert

from case.models import Case
from case.processing.sla import CaseSLAProcessor

from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_case(priority: CasePriority) -> Case:
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
        priority=priority,
    )


def test_low_priority_sla():
    case = build_case(CasePriority.LOW)

    CaseSLAProcessor().process([case])

    assert case.sla is not None
    assert case.sla.target_minutes == 1440


def test_medium_priority_sla():
    case = build_case(CasePriority.MEDIUM)

    CaseSLAProcessor().process([case])

    assert case.sla is not None
    assert case.sla.target_minutes == 240


def test_high_priority_sla():
    case = build_case(CasePriority.HIGH)

    CaseSLAProcessor().process([case])

    assert case.sla is not None
    assert case.sla.target_minutes == 60


def test_critical_priority_sla():
    case = build_case(CasePriority.CRITICAL)

    CaseSLAProcessor().process([case])

    assert case.sla is not None
    assert case.sla.target_minutes == 15


def test_due_at_is_after_created_at():
    case = build_case(CasePriority.HIGH)

    CaseSLAProcessor().process([case])

    assert case.sla is not None
    assert case.sla.due_at > case.created_at


def test_sla_is_not_breached_by_default():
    case = build_case(CasePriority.HIGH)

    CaseSLAProcessor().process([case])

    assert case.sla is not None
    assert case.sla.breached is False
    assert case.sla.breached_at is None