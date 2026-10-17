from __future__ import annotations

from alert.models import Alert
from case.models import Case


class CaseFactory:
    """
    Creates Case aggregates from alerts.
    """

    def create(
        self,
        alert: Alert,
    ) -> Case:
        return Case(
            title=alert.title,
            alert=alert,
        )
