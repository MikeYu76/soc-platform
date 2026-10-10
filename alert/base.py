from abc import ABC, abstractmethod

from alert.models import Alert
from common.detection import Detection
from correlation.models import CorrelationResult


class AlertRule(ABC):
    """
    Base interface for alert generation rules.
    """

    @abstractmethod
    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        """
        Generate alerts from detections and correlation results.
        """
        raise NotImplementedError