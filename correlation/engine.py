from correlation.base import CorrelationRule
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class CorrelationEngine:
    """Runs a collection of correlation rules."""

    def __init__(
        self,
        rules: list[CorrelationRule],
    ) -> None:
        self.rules = rules

    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:

        results: list[CorrelationResult] = []

        for rule in self.rules:
            results.extend(rule.correlate(detections))

        return results
