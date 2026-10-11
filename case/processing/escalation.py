from case.models import Case
from case.processing.base import CaseProcessor


class CaseEscalationProcessor(CaseProcessor):
    """
    Escalates cases whose SLA has been breached.
    """

    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        for case in cases:
            if case.sla is None:
                continue

            if not case.sla.breached:
                continue

            if case.escalation is not None:
                continue

            case.escalate(
                level=2,
                team="Tier 2",
                reason="SLA breached.",
            )

        return cases