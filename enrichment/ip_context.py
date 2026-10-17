from typing import Any

from common.detection import Detection
from enrichment.base import Enricher
from enrichment.models import Enrichment


class IPContextEnricher(Enricher):
    """Enrich detections using a supplied IP context lookup."""

    def __init__(self, ip_context: dict[str, dict[str, Any]]) -> None:
        self._ip_context = ip_context

    def enrich(self, detection: Detection) -> Enrichment:
        source_ip = detection.event.source_ip

        if source_ip is None:
            return Enrichment()

        source_ip_str = str(source_ip)
        context = self._ip_context.get(source_ip_str)

        if context is None:
            return Enrichment()

        return Enrichment(
            data={
                "ip_context": {
                    "source_ip": source_ip_str,
                    **context,
                }
            }
        )
