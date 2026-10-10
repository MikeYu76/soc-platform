from case.models import Case
from case.processing.base import CaseProcessor

from common.detection import Severity


class CaseAssignmentProcessor(CaseProcessor):
    """
    Assign newly created cases to an operational team.

    Current policy routes based on alert severity.
    """

    TEAM_MAPPING = {
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
            case.metadata["assigned_team"] = (
                self.TEAM_MAPPING[case.alert.severity]
            )

        return cases