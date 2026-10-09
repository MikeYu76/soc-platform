from correlation.base import CorrelationRule
from correlation.models import CorrelationResult
from common.event import Event


class CorrelationEngine:
    """Runs a collection of correlation rules."""

    def __init__(
        self,
        rules: list[CorrelationRule],
    ) -> None:
        self.rules = rules

    def correlate(
        self,
        events: list[Event],
    ) -> list[CorrelationResult]:

        results: list[CorrelationResult] = []

        for rule in self.rules:
            results.extend(rule.correlate(events))

        return results