from datetime import timedelta
from typing import ClassVar

from case.domain.sla import CaseSLA
from case.models import Case
from case.processing.base import CaseProcessor
from common.case_priority import CasePriority


class CaseSLAProcessor(CaseProcessor):
    """
    Assign SLA targets based on case priority.
    """

    SLA_MINUTES: ClassVar[dict[CasePriority, int]] = {
        CasePriority.LOW: 24 * 60,
        CasePriority.MEDIUM: 4 * 60,
        CasePriority.HIGH: 60,
        CasePriority.CRITICAL: 15,
    }

    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        for case in cases:
            minutes = self.SLA_MINUTES[case.priority]

            case.sla = CaseSLA(
                target_minutes=minutes,
                due_at=case.created_at + timedelta(minutes=minutes),
            )

        return cases
