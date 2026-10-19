from datetime import UTC, datetime

from case.models import Case
from case.processing.base import CaseProcessor


class CaseSLABreachProcessor(CaseProcessor):
    """
    Marks cases whose SLA has been breached.
    """

    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        now = datetime.now(UTC)

        for case in cases:
            if case.sla is None:
                continue

            if case.sla.breached:
                continue

            if now > case.sla.due_at:
                case.mark_sla_breached(now)

        return cases
