from alert.models import Alert
from alert.processing.base import AlertProcessor


class AlertGroupingProcessor(AlertProcessor):
    """
    Groups related alerts into a single representative alert.

    Current policy:
        - Alerts are grouped by title.
        - The first alert becomes the representative.
        - Group membership is recorded in metadata.
    """

    def process(
        self,
        alerts: list[Alert],
    ) -> list[Alert]:
        groups: dict[str, list[Alert]] = {}

        for alert in alerts:
            groups.setdefault(alert.title, []).append(alert)

        grouped_alerts: list[Alert] = []

        for group in groups.values():
            representative = group[0]

            if len(group) > 1:
                representative.metadata["grouped_ids"] = [
                    alert.id for alert in group
                ]

            grouped_alerts.append(representative)

        return grouped_alerts
