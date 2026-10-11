from datetime import UTC, datetime, timedelta

from alert.models import Alert

from case.domain.sla import CaseSLA
from case.models import Case
from case.processing.sla_breach import CaseSLABreachProcessor

from common.alert_status import AlertStatus
from common.case_priority import CasePriority
from common.case_status import CaseStatus
from common.detection import Detection, Severity
from common.event import Event
from common.event_types import EventType


def build_case() -> Case:
    event = Event(
        timestamp=datetime.now(UTC),
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
        priority=CasePriority.HIGH,
    )


def test_case_without_sla_is_ignored():
    case = build_case()

    result = CaseSLABreachProcessor().process([case])

    assert result == [case]
    assert case.sla is None


def test_future_due_date_is_not_breached():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) + timedelta(minutes=10),
    )

    CaseSLABreachProcessor().process([case])

    assert case.sla.breached is False
    assert case.sla.breached_at is None


def test_overdue_case_is_marked_breached():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) - timedelta(minutes=10),
    )

    CaseSLABreachProcessor().process([case])

    assert case.sla.breached is True
    assert case.sla.breached_at is not None


def test_already_breached_case_is_unchanged():
    case = build_case()

    breached_at = datetime.now(UTC) - timedelta(minutes=5)

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) - timedelta(minutes=10),
        breached=True,
        breached_at=breached_at,
    )

    CaseSLABreachProcessor().process([case])

    assert case.sla.breached is True
    assert case.sla.breached_at == breached_at


def test_processor_returns_same_case_list():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) + timedelta(minutes=10),
    )

    cases = [case]

    result = CaseSLABreachProcessor().process(cases)

    assert result is cases