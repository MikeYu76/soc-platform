from __future__ import annotations

from common.event import Event

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
        id: str,
    ) -> Event | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM events
            WHERE id = ?
            """,
            (id,),
        )

        if row is None:
            return None

        return EventMapper.from_record(
            self._row_to_dict(row),
        )

    def list(
        self,
    ) -> list[Event]:
        rows = self._fetch_all(
            """
            SELECT *
            FROM events
            ORDER BY timestamp DESC
            """
        )

        return [
            EventMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]