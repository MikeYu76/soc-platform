from __future__ import annotations

from typing import ClassVar

from repositories.queries.case_query import CaseQuery
from repositories.queries.case_sort import CaseSort
from repositories.queries.sort_order import SortOrder


class CaseQueryBuilder:
    """
    Builds SQL queries for searching persisted cases.

    The builder translates a CaseQuery into SQL and query
    parameters. It performs no database operations.
    """

    _SORT_COLUMNS: ClassVar[dict[CaseSort, str]] = {
        CaseSort.CREATED_AT: "created_at",
        CaseSort.PRIORITY: "priority",
        CaseSort.STATUS: "status",
        CaseSort.ASSIGNED_TO: "assigned_to",
    }

    @classmethod
    def build(
        cls,
        query: CaseQuery,
    ) -> tuple[str, tuple[object, ...]]:
        """
        Build a SQL statement and parameter tuple.
        """

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

        sort_column = cls._SORT_COLUMNS[query.sort_by]

        direction = "ASC" if query.sort_order is SortOrder.ASC else "DESC"

        sql += f"""
            ORDER BY {sort_column} {direction}, id DESC
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
