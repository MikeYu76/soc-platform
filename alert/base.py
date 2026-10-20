from __future__ import annotations

from abc import ABC, abstractmethod

from alert.models import Alert
from common.detection import Detection
from correlation.models import CorrelationResult


class AlertRule(ABC):
    """
    Base interface for alert generation rules.

    Each rule is responsible for generating at most one alert
    from a single detection or a single correlation result.

    The AlertEngine orchestrates execution across collections
    of detections and correlations.
    """

    @abstractmethod
    def generate(
        self,
        detections: list[Detection],
        correlations: list[CorrelationResult],
    ) -> list[Alert]:
        """Generate alerts from detections and correlation results."""
        raise NotImplementedError
    @abstractmethod
    def from_detection(
        self,
        detection: Detection,
    ) -> Alert | None:
        """
        Generate an alert from a detection.

        Returns None if this rule does not apply.
        """
        raise NotImplementedError

    @abstractmethod
    def from_correlation(
        self,
        correlation: CorrelationResult,
    ) -> Alert | None:
        """
        Generate an alert from a correlation result.

        Returns None if this rule does not apply.
        """
        raise NotImplementedError
