from abc import ABC, abstractmethod

from common.detection import Detection
from enrichment.models import Enrichment


class Enricher(ABC):
    """
    Base interface for all enrichment components.
    """

    @abstractmethod
    def enrich(self, detection: Detection) -> Enrichment:
        """
        Add contextual information to a detection.
        """
        ...
