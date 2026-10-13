from datetime import UTC, datetime, timedelta
from uuid import uuid4

from common.detection import Severity
from common.event_types import EventType
from correlation.base import CorrelationRule
from correlation.models import CorrelationResult
from enrichment.models import EnrichedDetection


class FailedLoginBurstRule(CorrelationRule):
    """Detect repeated failed logins from the same source IP."""

    def __init__(
        self,
        threshold: int = 5,
        window_minutes: int = 5,
    ) -> None:
        if threshold < 1:
            raise ValueError("threshold must be at least 1")

        if window_minutes < 1:
            raise ValueError("window_minutes must be at least 1")

        self.threshold = threshold
        self.window = timedelta(minutes=window_minutes)

    def correlate(
        self,
        detections: list[EnrichedDetection],
    ) -> list[CorrelationResult]:

        failed_detections = [
            detection
            for detection in detections
            if (
                detection.detection.event.event_type
                == EventType.AUTHENTICATION_FAILED
                and detection.detection.event.source_ip is not None
            )
        ]

        detections_by_ip: dict[str, list[EnrichedDetection]] = {}

        for detection in failed_detections:
            ip = str(detection.detection.event.source_ip)
            detections_by_ip.setdefault(ip, []).append(detection)

        results: list[CorrelationResult] = []

        for ip, ip_detections in detections_by_ip.items():

            ip_detections.sort(
                key=lambda detection: detection.detection.event.timestamp
            )

            for start_index, start_detection in enumerate(ip_detections):

                matching = [
                    detection
                    for detection in ip_detections[start_index:]
                    if (
                        detection.detection.event.timestamp
                        - start_detection.detection.event.timestamp
                        <= self.window
                    )
                ]

                if len(matching) < self.threshold:
                    continue

                matched = matching[: self.threshold]

                results.append(
                    CorrelationResult(
                        correlation_id=str(uuid4()),
                        rule_id="CORR-AUTH-001",
                        title="Repeated Failed Login Attempts",
                        severity=Severity.HIGH,
                        matched_at=datetime.now(UTC),
                        detections=matched,
                        metadata={
                            "source_ip": ip,
                            "attempt_count": len(matched),
                            "threshold": self.threshold,
                            "window_minutes": self.window.total_seconds() / 60,
                        },
                    )
                )

                # One result per source IP for this implementation.
                break

        return results