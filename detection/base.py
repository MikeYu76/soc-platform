from abc import ABC, abstractmethod

from common.detection import Detection
from common.event import Event


class DetectionRule(ABC):
    """
    Base interface for detection rules.

    Every detection rule evaluates a canonical Event and
    returns a Detection if the rule matches, or None if it
    does not.
    """

    @abstractmethod
    def match(self, event: Event) -> Detection | None:
        """
        Evaluate an event against this detection rule.

        Args:
            event (Event): The event to evaluate.

        Returns:
            Detection | None: A Detection if the rule matches, or None if it does not.
        """
