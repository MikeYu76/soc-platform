from abc import ABC, abstractmethod

from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class CorrelationRule(ABC):
    """Base class for all correlation rules."""

    @abstractmethod
    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:
        """Return correlation results for the supplied enriched detections."""
        raise NotImplementedError