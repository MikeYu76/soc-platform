from __future__ import annotations

from repositories.queries.alert_query import AlertQuery
from repositories.queries.sort_order import SortOrder


class AlertQueryBuilder:
    """
    Builds SQL queries for searching persisted alerts.

    The builder translates an AlertQuery into SQL and query
    parameters. It performs no database operations.
    """

    @classmethod
    def build(
        cls,
        query: AlertQuery,
    ) -> tuple[str, tuple[object, ...]]:
        where_clauses: list[str] = []
        parameters: list[object] = []

        if query.status is not None:
            where_clauses.append("status = ?")
            parameters.append(query.status.value)

        if query.severity is not None:
            where_clauses.append("severity = ?")
            parameters.append(query.severity.value)

        sql = """
            SELECT *
            FROM alerts
        """

        if where_clauses:
            sql += "\nWHERE " + " AND ".join(where_clauses)

        direction = "ASC" if query.sort_order is SortOrder.ASC else "DESC"

        sql += f"""
            ORDER BY created_at {direction}
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
