from __future__ import annotations

from common.detection import Detection, Severity

from alert.base import AlertRule
from alert.models import Alert

from correlation.models import CorrelationResult


class ImmediateDetectionAlertRule(AlertRule):
    """
    Generates alerts immediately for detections whose severity
    meets or exceeds a configurable threshold.
    """

    _SEVERITY_ORDER = {
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }

    def __init__(
        self,
        minimum_severity: Severity = Severity.HIGH,
    ) -> None:
        self._minimum_severity = minimum_severity

    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        """
        Generate alerts from qualifying detections.

        Correlations are ignored by this rule.
        """
        alerts: list[Alert] = []

        for detection in detections:
            alert = self.from_detection(detection)

            if alert is not None:
                alerts.append(alert)

        return alerts

    def from_detection(
        self,
        detection: Detection,
    ) -> Alert | None:
        """
        Generate an alert from a qualifying detection.
        """
        minimum_rank = self._SEVERITY_ORDER[self._minimum_severity]
        detection_rank = self._SEVERITY_ORDER[detection.severity]

        if detection_rank < minimum_rank:
            return None

        return Alert(
            title=detection.title,
            severity=detection.severity,
            source=detection,
        )

    def from_correlation(
        self,
        correlation: CorrelationResult,
    ) -> Alert | None:
        """
        Immediate detection alerts are never generated from
        correlation results.
        """
        return None