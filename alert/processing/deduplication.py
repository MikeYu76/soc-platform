from common.detection import Detection
from correlation.models import CorrelationResult

from alert.models import Alert
from alert.processing.base import AlertProcessor


class DeduplicationProcessor(AlertProcessor):
    """
    Removes duplicate alerts.

    Alerts are considered duplicates when they reference the
    same underlying Detection or CorrelationResult.
    """

    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        """
        Remove duplicate alerts while preserving the first
        occurrence of each unique source.
        """
        seen: set[tuple[str, str]] = set()

        deduplicated: list[Alert] = []

        for alert in alerts:
            source = alert.source

            if isinstance(source, Detection):
                key = ("detection", source.id)

            elif isinstance(source, CorrelationResult):
                key = ("correlation", source.correlation_id)

            else:
                # Defensive programming. The Alert model currently
                # guarantees one of these two types.
                continue

            if key in seen:
                continue

            seen.add(key)
            deduplicated.append(alert)

        return deduplicated