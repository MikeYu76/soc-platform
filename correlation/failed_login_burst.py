
from datetime import datetime, timedelta, UTC
from uuid import uuid4

from common.event import Event
from common.event_types import EventType
from correlation.models import CorrelationResult


class FailedLoginBurstRule:
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
        events: list[Event],
    ) -> list[CorrelationResult]:
        failed_events = [
            event
            for event in events
            if event.event_type == EventType.AUTHENTICATION_FAILED
            and event.source_ip is not None
        ]

        events_by_ip: dict[str, list[Event]] = {}

        for event in failed_events:
            ip = str(event.source_ip)
            events_by_ip.setdefault(ip, []).append(event)

        results: list[CorrelationResult] = []

        for ip, ip_events in events_by_ip.items():
            ip_events.sort(key=lambda event: event.timestamp)

            for start_index, start_event in enumerate(ip_events):
                matching_events = [
                    event
                    for event in ip_events[start_index:]
                    if event.timestamp - start_event.timestamp <= self.window
                ]

                if len(matching_events) < self.threshold:
                    continue

                matched_events = matching_events[:self.threshold]

                results.append(
                    CorrelationResult(
                        correlation_id=str(uuid4()),
                        rule_id="CORR-AUTH-001",
                        title="Repeated Failed Login Attempts",
                        matched_at=datetime.now(UTC),
                        events=matched_events,
                        metadata={
                            "source_ip": ip,
                            "attempt_count": len(matched_events),
                            "threshold": self.threshold,
                            "window_minutes": self.window.total_seconds() / 60,
                        },
                    )
                )

                # One result per source IP for this initial implementation.
                break

        return results