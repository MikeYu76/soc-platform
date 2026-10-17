from alert.base import AlertRule
from alert.models import Alert
from common.detection import Detection
from correlation.models import CorrelationResult


class AlertEngine:
    """
    Coordinates alert generation by executing registered alert rules.
    """

    def __init__(self, rules: list[AlertRule]):
        self._rules = rules

    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        """
        Execute each registered alert rule and return all generated alerts.
        """
        alerts: list[Alert] = []

        for rule in self._rules:
            alerts.extend(rule.generate(detections, correlations))

        return alerts
