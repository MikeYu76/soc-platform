from __future__ import annotations

from alert.base import AlertRule
from alert.models import Alert

from common.detection import Detection

from correlation.models import CorrelationResult


class CorrelationAlertRule(AlertRule):
    """
    Generates one alert for every correlation result.

    This implementation intentionally performs no filtering,
    suppression, grouping, or deduplication. Those policies are
    handled by other AlertRule implementations or downstream
    processing components.
    """

    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        """
        Generate alerts from correlation results.

        Detections are ignored by this rule.
        """
        alerts: list[Alert] = []

        for correlation in correlations:
            alert = self.from_correlation(correlation)

            if alert is not None:
                alerts.append(alert)

        return alerts

    def from_detection(
        self,
        detection: Detection,
    ) -> Alert | None:
        """
        Correlation alerts are never generated directly from
        detections.
        """
        return None

    def from_correlation(
        self,
        correlation: CorrelationResult,
    ) -> Alert | None:
        """
        Generate an alert from a correlation result.
        """
        return Alert(
            title=correlation.title,
            severity=correlation.severity,
            source=correlation,
        )