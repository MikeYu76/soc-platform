from datetime import datetime

from alert.models import Alert
from case.domain.timeline import CaseTimelineEventType
from case.factory import CaseFactory
from case.models import Case
from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_alert() -> Alert:
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

    return Alert(
        title="Suspicious Authentication",
        severity=Severity.HIGH,
        status=AlertStatus.NEW,
        source=detection,
    )


def test_factory_creates_case():
    alert = build_alert()

    case = CaseFactory().create(alert)

    assert isinstance(case, Case)


def test_factory_uses_alert_title():
    alert = build_alert()

    case = CaseFactory().create(alert)

    assert case.title == alert.title


def test_factory_attaches_alert():
    alert = build_alert()

    case = CaseFactory().create(alert)

    assert case.alert == alert


def test_factory_initializes_default_case_state():
    alert = build_alert()

    case = CaseFactory().create(alert)

    assert case.status == CaseStatus.NEW
    assert case.priority == CasePriority.MEDIUM
    assert len(case.timeline) == 1
    assert case.timeline[0].event_type == CaseTimelineEventType.CASE_CREATED
