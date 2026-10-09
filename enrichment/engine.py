from typing import Any

from common.detection import Detection

from enrichment.base import Enricher
from enrichment.models import EnrichedDetection, Enrichment


class EnrichmentEngine:
    """
    Coordinates enrichment components and combines their results into
    a single EnrichedDetection.
    """

    def __init__(self, enrichers: list[Enricher]) -> None:
        """
        Initialize the enrichment engine.

        Args:
            enrichers: The enrichment components that will be executed
                for every detection processed by the engine.
        """
        self._enrichers = enrichers

    def process(self, detection: Detection) -> EnrichedDetection:
        """
        Process a detection through every configured enricher.

        Args:
            detection: The detection to enrich.

        Returns:
            An EnrichedDetection containing the original detection and
            all collected enrichment data.
        """
        combined_data: dict[str, Any] = {}

        for enricher in self._enrichers:
            enrichment = enricher.enrich(detection)
            combined_data.update(enrichment.data)

        return EnrichedDetection(
            detection=detection,
            enrichment=Enrichment(data=combined_data),
        )