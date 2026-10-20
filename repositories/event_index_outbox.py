from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PendingEventIndex:
    """A committed event waiting to be indexed."""

    event_id: str
    attempts: int


@dataclass(frozen=True, slots=True)
class EventIndexOutboxStatus:
    """Aggregate state for queued OpenSearch indexing work."""

    pending_count: int
    ready_count: int
    retry_wait_count: int
    retrying_count: int
    oldest_created_at: str | None
    max_attempts: int


class EventIndexOutboxRepository(ABC):
    """Persistence port for durable OpenSearch indexing work."""

    @abstractmethod
    def enqueue(self, event_id: str) -> None:
        """Add an event to the queue in the current transaction."""
        raise NotImplementedError

    @abstractmethod
    def get_pending(self, limit: int) -> list[PendingEventIndex]:
        """Return due queue entries in creation order."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> EventIndexOutboxStatus:
        """Return aggregate counts and age information for queued work."""
        raise NotImplementedError

    @abstractmethod
    def mark_delivered(self, event_id: str) -> None:
        """Remove a successfully indexed event from the queue."""
        raise NotImplementedError

    @abstractmethod
    def schedule_retry(
        self,
        event_id: str,
        next_attempt_at: str,
        error_type: str,
    ) -> None:
        """Record a failed attempt and its next eligible time."""
        raise NotImplementedError
