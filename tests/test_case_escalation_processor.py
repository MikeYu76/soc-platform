from datetime import UTC, datetime, timedelta

from alert.models import Alert

from case.domain.sla import CaseSLA
from case.models import Case
from case.processing.escalation import CaseEscalationProcessor

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


def test_case_without_sla_is_not_escalated():
    case = build_case()

    CaseEscalationProcessor().process([case])

    assert case.escalation is None


def test_case_within_sla_is_not_escalated():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) + timedelta(minutes=10),
        breached=False,
    )

    CaseEscalationProcessor().process([case])

    assert case.escalation is None


def test_breached_case_is_escalated():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) - timedelta(minutes=10),
        breached=True,
        breached_at=datetime.now(UTC),
    )

    CaseEscalationProcessor().process([case])

    assert case.escalation is not None
    assert case.escalation.level == 2
    assert case.escalation.team == "Tier 2"
    assert case.assigned_to == "Tier 2"


def test_already_escalated_case_is_not_modified():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC) - timedelta(minutes=10),
        breached=True,
        breached_at=datetime.now(UTC),
    )

    case.escalate(
        level=2,
        team="Tier 2",
        reason="Initial escalation.",
    )

    original_time = case.escalation.escalated_at

    CaseEscalationProcessor().process([case])

    assert case.escalation is not None
    assert case.escalation.escalated_at == original_time


def test_processor_returns_same_case_list():
    case = build_case()

    case.sla = CaseSLA(
        target_minutes=60,
        due_at=datetime.now(UTC),
        breached=False,
    )

    cases = [case]

    result = CaseEscalationProcessor().process(cases)

    assert result is cases