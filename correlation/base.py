from abc import ABC, abstractmethod

from common.event import Event
from correlation.models import CorrelationResult


class CorrelationRule(ABC):
    """Base class for all correlation rules."""

    @abstractmethod
    def correlate(
        self,
        events: list[Event],
    ) -> list[CorrelationResult]:
        """Return any correlation results for the supplied events."""
        raise NotImplementedError