from datetime import UTC, datetime, timedelta
from uuid import uuid4

from common.detection import Severity
from common.event_types import EventType
from correlation.base import CorrelationRule
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class LateralMovementRule(CorrelationRule):
    """
    Detect successful authentication to multiple hosts by the same
    user within a short period of time.
    """

    def __init__(
        self,
        threshold: int = 3,
        window_minutes: int = 30,
    ) -> None:
        if threshold < 2:
            raise ValueError(
                "threshold must be at least 2",
            )

        if window_minutes < 1:
            raise ValueError(
                "window_minutes must be at least 1",
            )

        self.threshold = threshold
        self.window = timedelta(
            minutes=window_minutes,
        )

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
                and detection.detection.event.hostname is not None
            )
        ]

        detections_by_user: dict[
            str,
            list[EnrichedDetection],
        ] = {}

        for detection in successful_logins:
            username = detection.detection.event.username
            detections_by_user.setdefault(
                username,
                [],
            ).append(
                detection,
            )

        results: list[CorrelationResult] = []

        for username, user_detections in detections_by_user.items():

            user_detections.sort(
                key=lambda detection: detection.detection.event.timestamp,
            )

            for start_index, start_detection in enumerate(
                user_detections,
            ):

                matching = [
                    detection
                    for detection in user_detections[start_index:]
                    if (
                        detection.detection.event.timestamp
                        - start_detection.detection.event.timestamp
                        <= self.window
                    )
                ]

                hosts = {
                    detection.detection.event.hostname
                    for detection in matching
                }

                if len(hosts) < self.threshold:
                    continue

                results.append(
                    CorrelationResult(
                        correlation_id=str(uuid4()),
                        rule_id="CORR-AUTH-003",
                        title="Possible Lateral Movement",
                        severity=Severity.HIGH,
                        matched_at=datetime.now(UTC),
                        detections=matching,
                        metadata={
                            "username": username,
                            "host_count": len(hosts),
                            "hosts": sorted(hosts),
                            "window_minutes": (
                                self.window.total_seconds() / 60
                            ),
                        },
                    )
                )

                # Produce one correlation per user.
                break

        return results
