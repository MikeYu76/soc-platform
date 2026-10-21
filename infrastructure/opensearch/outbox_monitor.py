from __future__ import annotations

from datetime import UTC, datetime
from threading import Lock
from time import monotonic

from repositories.event_index_outbox import EventIndexOutboxStatus


class EventIndexOutboxMonitor:
    """Keeps aggregate queue metrics and detects a sustained backlog."""

    def __init__(
        self,
        *,
        pending_threshold: int,
        sustained_seconds: int,
    ) -> None:
        if pending_threshold <= 0:
            raise ValueError("pending_threshold must be positive.")
        if sustained_seconds <= 0:
            raise ValueError("sustained_seconds must be positive.")
        self._pending_threshold = pending_threshold
        self._sustained_seconds = sustained_seconds
        self._lock = Lock()
        self._pending_count = 0
        self._ready_count = 0
        self._retry_wait_count = 0
        self._retrying_count = 0
        self._oldest_pending_age_seconds = 0.0
        self._max_attempts = 0
        self._enabled = False
        self._last_observed_timestamp_seconds = 0.0
        self._above_threshold_since: float | None = None
        self._alert_started_timestamp_seconds = 0.0
        self._alert_active = False

    def observe(
        self,
        status: EventIndexOutboxStatus,
        *,
        enabled: bool,
    ) -> str | None:
        """Record a successful sample; return a new alert/recovery transition."""
        monotonic_now = monotonic()
        timestamp_now = datetime.now(UTC).timestamp()
        oldest_age = self._get_oldest_age_seconds(status.oldest_created_at)
        with self._lock:
            self._pending_count = status.pending_count
            self._ready_count = status.ready_count
            self._retry_wait_count = status.retry_wait_count
            self._retrying_count = status.retrying_count
            self._oldest_pending_age_seconds = oldest_age
            self._max_attempts = status.max_attempts
            self._enabled = enabled
            self._last_observed_timestamp_seconds = timestamp_now

            threshold_exceeded = (
                enabled and status.pending_count >= self._pending_threshold
            )
            if not threshold_exceeded:
                self._above_threshold_since = None
                if self._alert_active:
                    self._alert_active = False
                    self._alert_started_timestamp_seconds = 0.0
                    return "recovered"
                return None

            if self._above_threshold_since is None:
                self._above_threshold_since = monotonic_now
            elapsed = monotonic_now - self._above_threshold_since
            if not self._alert_active and elapsed >= self._sustained_seconds:
                self._alert_active = True
                self._alert_started_timestamp_seconds = timestamp_now
                return "alert"
            return None

    def alert_log_context(self) -> dict[str, int | float]:
        with self._lock:
            return {
                "pending_count": self._pending_count,
                "pending_threshold": self._pending_threshold,
                "sustained_seconds": self._sustained_seconds,
                "oldest_pending_age_seconds": self._oldest_pending_age_seconds,
            }

    def to_prometheus_text(self) -> str:
        """Render aggregate queue gauges in Prometheus text exposition format."""
        with self._lock:
            values: tuple[tuple[str, str, int | float], ...] = (
                (
                    "soc_opensearch_outbox_enabled",
                    "Whether OpenSearch event indexing is enabled.",
                    int(self._enabled),
                ),
                (
                    "soc_opensearch_outbox_pending_events",
                    "Number of events waiting for OpenSearch indexing.",
                    self._pending_count,
                ),
                (
                    "soc_opensearch_outbox_ready_events",
                    "Number of due events waiting for an indexing attempt.",
                    self._ready_count,
                ),
                (
                    "soc_opensearch_outbox_retry_wait_events",
                    "Number of events waiting for their next retry time.",
                    self._retry_wait_count,
                ),
                (
                    "soc_opensearch_outbox_retrying_events",
                    "Number of events that have failed at least once.",
                    self._retrying_count,
                ),
                (
                    "soc_opensearch_outbox_oldest_pending_age_seconds",
                    "Age in seconds of the oldest queued event.",
                    self._oldest_pending_age_seconds,
                ),
                (
                    "soc_opensearch_outbox_max_attempts",
                    "Highest indexing attempt count among queued events.",
                    self._max_attempts,
                ),
                (
                    "soc_opensearch_outbox_backlog_alert_active",
                    "Whether the sustained backlog alert is active.",
                    int(self._alert_active),
                ),
                (
                    "soc_opensearch_outbox_backlog_pending_threshold",
                    "Pending event count that starts the backlog alert timer.",
                    self._pending_threshold,
                ),
                (
                    "soc_opensearch_outbox_backlog_sustained_seconds",
                    "Seconds the backlog threshold must persist to alert.",
                    self._sustained_seconds,
                ),
                (
                    "soc_opensearch_outbox_last_observed_timestamp_seconds",
                    "Unix timestamp of the latest successful queue sample.",
                    self._last_observed_timestamp_seconds,
                ),
                (
                    "soc_opensearch_outbox_backlog_alert_started_timestamp_seconds",
                    "Unix timestamp when the sustained backlog alert activated.",
                    self._alert_started_timestamp_seconds,
                ),
            )

        output: list[str] = []
        for name, help_text, value in values:
            output.extend(
                (
                    f"# HELP {name} {help_text}",
                    f"# TYPE {name} gauge",
                    f"{name} {value}",
                )
            )
        return "\n".join(output) + "\n"

    @staticmethod
    def _get_oldest_age_seconds(oldest_created_at: str | None) -> float:
        if oldest_created_at is None:
            return 0.0
        oldest = datetime.fromisoformat(oldest_created_at)
        if oldest.tzinfo is None:
            oldest = oldest.replace(tzinfo=UTC)
        return max(0.0, (datetime.now(UTC) - oldest.astimezone(UTC)).total_seconds())

