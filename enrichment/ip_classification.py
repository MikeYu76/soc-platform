
import ipaddress

from common.detection import Detection
from enrichment.base import Enricher
from enrichment.models import Enrichment


class IPClassificationEnricher(Enricher):
    """Classify the network properties of a detection's source IP."""

    def enrich(self, detection: Detection) -> Enrichment:
        source_ip = detection.event.source_ip

        if source_ip is None:
            return Enrichment()

        ip_address = ipaddress.ip_address(str(source_ip))

        return Enrichment(
            data={
                "ip_classification": {
                    "source_ip": str(ip_address),
                    "is_private": ip_address.is_private,
                    "is_loopback": ip_address.is_loopback,
                    "is_link_local": ip_address.is_link_local,
                    "is_global": ip_address.is_global,
                }
            }
        )