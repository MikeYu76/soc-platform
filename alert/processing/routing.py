from alert.models import Alert
from alert.processing.base import AlertProcessor
from common.detection import Severity


class AlertRoutingProcessor(AlertProcessor):
    """
    Assigns alerts to an operational queue.

    Current routing policy is severity-based.
    """

    ROUTES = {
        Severity.LOW: "Tier 1",
        Severity.MEDIUM: "Tier 1",
        Severity.HIGH: "Tier 2",
        Severity.CRITICAL: "Incident Response",
    }

    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        for alert in alerts:
            alert.metadata["route"] = self.ROUTES[alert.severity]

        return alerts