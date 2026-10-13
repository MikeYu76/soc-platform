from correlation.models import CorrelationResult

from alert.models import Alert


class AlertFactory:
    """
    Creates Alert aggregates from correlation results.
    """

    def create(
        self,
        result: CorrelationResult,
    ) -> Alert:
        return Alert(
            title=result.title,
            severity=result.severity,
            source=result,
        )