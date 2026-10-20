from __future__ import annotations

import builtins
from abc import ABC, abstractmethod
from collections.abc import Iterable

from common.event import Event
from repositories.queries.event_query import EventQuery


class EventRepository(ABC):
    """
    Repository interface for Event persistence.
    """

    @abstractmethod
    def save(
        self,
        event: Event,
    ) -> None:
        """
        Persist a single event.
        """
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
        id: str,
    ) -> Event | None:
        """
        Retrieve an event by its internal identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
    ) -> builtins.list[Event]:
        """
        Return all persisted events.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: EventQuery,
    ) -> builtins.list[Event]:
        """
        Search for persisted events using query criteria.
        """
        raise NotImplementedError
