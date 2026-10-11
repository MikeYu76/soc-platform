from __future__ import annotations

from datetime import datetime

from common.event import Event
from common.event_types import EventType

from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.event_mapper import EventMapper

from repositories.event_repository import EventRepository


class SQLiteEventRepository(
    SQLiteRepository,
    EventRepository,
):
    """
    SQLite implementation of EventRepository.
    """

    TABLE = "events"

    def save(
        self,
        event: Event,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=EventMapper.to_record(event),
        )

    def get(
        self,
        event_id: str | int,
    ) -> Event | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM events
            WHERE id = ?
            """,
            (str(event_id),),
        )

        if row is None:
            return None

        return EventMapper.from_record(
            self._row_to_dict(row),
        )

    def list_since(
        self,
        since: datetime,
    ) -> list[Event]:
        rows = self._fetch_all(
            """
            SELECT *
            FROM events
            WHERE timestamp >= ?
            ORDER BY timestamp
            """,
            (since.isoformat(),),
        )

        return [
            EventMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_source(
        self,
        log_source: str,
    ) -> list[Event]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="log_source",
            value=log_source,
        )

        return [
            EventMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def list_by_type(
        self,
        event_type: EventType,
    ) -> list[Event]:
        rows = self._fetch_by_column(
            table=self.TABLE,
            column="event_type",
            value=event_type.value,
        )

        return [
            EventMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]