import itertools
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from common.detection import Severity
from common.event_types import EventType
from correlation.base import CorrelationRule
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class ImpossibleTravelRule(CorrelationRule):
    """Detect successful logins from different countries within a short time window."""

    def __init__(
        self,
        window_hours: int = 2,
    ) -> None:
        if window_hours < 1:
            raise ValueError("window_hours must be at least 1")

        self.window = timedelta(hours=window_hours)

    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:

        successful_logins = [
            detection
            for detection in detections
            if (
                detection.detection.event.event_type
                == EventType.AUTHENTICATION_SUCCESS
                and detection.detection.event.username is not None
            )
        ]

        detections_by_user: dict[str, list[EnrichedDetection]] = {}

        for detection in successful_logins:
            username = detection.detection.event.username
            if username is None:
                continue
            detections_by_user.setdefault(username, []).append(detection)

        results: list[CorrelationResult] = []

        for username, user_detections in detections_by_user.items():

            user_detections.sort(
                key=lambda detection: detection.detection.event.timestamp
            )

            for previous, current in itertools.pairwise(user_detections):

                previous_context = previous.enrichment.data.get("ip_context")
                current_context = current.enrichment.data.get("ip_context")

                if previous_context is None or current_context is None:
                    continue

                previous_country = previous_context.get("country")
                current_country = current_context.get("country")

                if previous_country is None or current_country is None:
                    continue

                if previous_country == current_country:
                    continue

                time_difference = (
                    current.detection.event.timestamp
                    - previous.detection.event.timestamp
                )

                if time_difference > self.window:
                    continue

                results.append(
                    CorrelationResult(
                        correlation_id=str(uuid4()),
                        rule_id="CORR-AUTH-002",
                        title="Impossible Travel",
                        severity=Severity.HIGH,
                        matched_at=datetime.now(UTC),
                        detections=[previous, current],
                        metadata={
                            "username": username,
                            "previous_country": previous_country,
                            "current_country": current_country,
                            "window_hours": self.window.total_seconds() / 3600,
                        },
                    )
                )

        return results
