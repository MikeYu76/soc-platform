from abc import ABC, abstractmethod
from typing import Any

from common.event import Event


class BaseParser(ABC):
    """
    Abstract base class for all log parsers.
    """

    @abstractmethod
    def parse(self, raw_log: Any) -> Event:
        """
        Parse a raw log into a canonical Event.

        Args:
            raw_log: The original log in its source-specific format.

        Returns:
            A normalized Event.
        """
