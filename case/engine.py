from alert.models import Alert

from case.base import CaseRule
from case.models import Case


class CaseEngine:
    """
    Coordinates case creation by executing CaseRules.
    """

    def __init__(
        self,
        rules: list[CaseRule],
    ) -> None:
        self._rules = rules

    def generate(
        self,
        alerts: list[Alert],
    ) -> list[Case]:
        cases: list[Case] = []

        for rule in self._rules:
            cases.extend(rule.generate(alerts))

        return cases