from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime

from common.event import Event
from common.event_types import EventType


class EventRepository(ABC):
    """
    Repository interface for Event persistence.
    """

    @abstractmethod
    def save(
        self,
        event: Event,
    ) -> None:
        raise NotImplementedError

    def save_all(
        self,
        events: Iterable[Event],
    ) -> None:
        """
        Persist multiple events.

        Repositories may override this with a more efficient
        implementation.
        """
        for event in events:
            self.save(event)

    @abstractmethod
    def get(
        self,
        event_id: str | int,
    ) -> Event | None:
        raise NotImplementedError