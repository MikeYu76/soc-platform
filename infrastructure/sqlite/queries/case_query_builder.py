from __future__ import annotations

from repositories.queries.case_query import CaseQuery
from repositories.queries.sort_order import SortOrder


class CaseQueryBuilder:
    """
    Builds SQL queries for searching persisted cases.

    The builder translates a CaseQuery into SQL and query
    parameters. It performs no database operations.
    """

    @classmethod
    def build(
        cls,
        query: CaseQuery,
    ) -> tuple[str, tuple[object, ...]]:
        where_clauses: list[str] = []
        parameters: list[object] = []

        if query.status is not None:
            where_clauses.append("status = ?")
            parameters.append(query.status.value)

        if query.priority is not None:
            where_clauses.append("priority = ?")
            parameters.append(query.priority.value)

        if query.assigned_to is not None:
            where_clauses.append("assigned_to = ?")
            parameters.append(query.assigned_to)

        sql = """
            SELECT *
            FROM cases
        """

        if where_clauses:
            sql += "\nWHERE " + " AND ".join(where_clauses)

        direction = (
            "ASC"
            if query.sort_order is SortOrder.ASC
            else "DESC"
        )

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
