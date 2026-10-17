from __future__ import annotations

from typing import ClassVar

from repositories.queries.event_query import EventQuery
from repositories.queries.event_sort import EventSort
from repositories.queries.sort_order import SortOrder


class EventQueryBuilder:
    """
    Builds SQL queries for searching persisted events.

    The builder translates an EventQuery into SQL and query
    parameters. It performs no database operations.
    """

    _SORT_COLUMNS: ClassVar[dict[EventSort, str]] = {
        EventSort.TIMESTAMP: "timestamp",
        EventSort.EVENT_TYPE: "event_type",
        EventSort.HOSTNAME: "hostname",
        EventSort.USERNAME: "username",
    }

    @classmethod
    def build(
        cls,
        query: EventQuery,
    ) -> tuple[str, tuple[object, ...]]:
        """
        Build a SQL statement and parameter tuple.
        """

        where_clauses: list[str] = []
        parameters: list[object] = []

        if query.event_type is not None:
            where_clauses.append("event_type = ?")
            parameters.append(query.event_type.value)

        if query.hostname is not None:
            where_clauses.append("hostname = ?")
            parameters.append(query.hostname)

        if query.username is not None:
            where_clauses.append("username = ?")
            parameters.append(query.username)

        if query.log_source is not None:
            where_clauses.append("log_source = ?")
            parameters.append(query.log_source)

        if query.source_ip is not None:
            where_clauses.append("source_ip = ?")
            parameters.append(str(query.source_ip))

        if query.destination_ip is not None:
            where_clauses.append("destination_ip = ?")
            parameters.append(str(query.destination_ip))

        sql = """
            SELECT *
            FROM events
        """

        if where_clauses:
            sql += "\nWHERE " + " AND ".join(where_clauses)

        sort_column = cls._SORT_COLUMNS[query.sort_by]

        direction = "ASC" if query.order is SortOrder.ASC else "DESC"

        sql += f"""
            ORDER BY {sort_column} {direction}
            LIMIT ?
            OFFSET ?
        """

        parameters.extend(
            [
                query.limit,
                query.offset,
            ]
        )

        return (
            sql,
            tuple(parameters),
        )
