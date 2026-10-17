from __future__ import annotations

from common.event import Event
from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.event_mapper import EventMapper
from infrastructure.sqlite.queries.event_query_builder import EventQueryBuilder
from repositories.event_repository import EventRepository
from repositories.queries.event_query import EventQuery


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
        return self.search(
            EventQuery(),
        )

    def search(
        self,
        query: EventQuery,
    ) -> list[Event]:
        sql, parameters = EventQueryBuilder.build(
            query,
        )

        rows = self._fetch_all(
            sql,
            parameters,
        )

        return [
            EventMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]
