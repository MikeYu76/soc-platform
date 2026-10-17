from typing import ClassVar

from case.models import Case
from case.processing.base import CaseProcessor
from common.detection import Severity


class CaseAssignmentProcessor(CaseProcessor):
    """
    Assign newly created cases to an operational team.
    """

    TEAM_MAPPING: ClassVar[dict[Severity, str]] = {
        Severity.LOW: "Tier 1",
        Severity.MEDIUM: "Tier 1",
        Severity.HIGH: "Tier 2",
        Severity.CRITICAL: "Incident Response",
    }

    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        for case in cases:
            case.assign(
                team=self.TEAM_MAPPING[case.alert.severity],
                assigned_by="AssignmentProcessor",
                reason="Severity routing",
            )

        return cases
