from alert.models import Alert

from case.base import CaseRule
from case.models import Case


class ImmediateCaseRule(CaseRule):
    """
    Creates one case for every alert.
    """

    def generate(
        self,
        alerts: list[Alert],
    ) -> list[Case]:
        return [
            Case(
                title=alert.title,
                alert=alert,
            )
            for alert in alerts
        ]