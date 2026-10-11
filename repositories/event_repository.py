from abc import ABC, abstractmethod
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

    @abstractmethod
    def get(
        self,
        event_id: str | int,
    ) -> Event | None:
        raise NotImplementedError

    @abstractmethod
    def list_since(
        self,
        since: datetime,
    ) -> list[Event]:
        raise NotImplementedError

    @abstractmethod
    def list_by_source(
        self,
        log_source: str,
    ) -> list[Event]:
        raise NotImplementedError

    @abstractmethod
    def list_by_type(
        self,
        event_type: EventType,
    ) -> list[Event]:
        raise NotImplementedError