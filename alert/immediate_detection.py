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
        Generate alerts for detections meeting the configured
        minimum severity.

        Correlations are ignored by this rule.
        """
        minimum_rank = self._SEVERITY_ORDER[self._minimum_severity]

        alerts: list[Alert] = []

        for detection in detections:
            detection_rank = self._SEVERITY_ORDER[detection.severity]

            if detection_rank < minimum_rank:
                continue

            alerts.append(
                Alert(
                    title=detection.title,
                    severity=detection.severity,
                    source=detection,
                )
            )

        return alerts