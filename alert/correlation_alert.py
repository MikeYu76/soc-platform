from alert.base import AlertRule
from alert.models import Alert
from common.detection import Detection
from correlation.models import CorrelationResult


class CorrelationAlertRule(AlertRule):
    """
    Generates one alert for every correlation result.

    This initial implementation intentionally applies no filtering,
    suppression, grouping, or deduplication. Those policies can be
    introduced later as separate AlertRule implementations.
    """

    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        """
        Generate an alert for every correlation result.

        Detections are ignored by this rule.
        """
        alerts: list[Alert] = []

        for correlation in correlations:
            alerts.append(
                Alert(
                    title=correlation.title,
                    severity=correlation.severity,
                    source=correlation,
                )
            )

        return alerts