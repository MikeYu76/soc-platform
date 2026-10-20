from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from typing import Any, Protocol


class RepositoryConnection(Protocol):
    """Connection interface shared by SQLite and PostgreSQL adapters."""

    def execute(
        self,
        query: str,
        parameters: Any = (),
    ) -> Any: ...


class SQLiteRepository:
    """
    Shared functionality for SQLite repository implementations.

    This class provides generic SQL helpers that operate on a shared
    SQLite connection managed by the UnitOfWork.

    Table and column names supplied to these helpers must be trusted
    constants defined by repository implementations. They must never
    originate from user input.
    """

    def __init__(
        self,
        connection: RepositoryConnection,
    ) -> None:
        self._connection = connection

    @staticmethod
    def _row_to_dict(
        row: sqlite3.Row,
    ) -> dict[str, Any]:
        """Convert a non-null sqlite3.Row into a dictionary."""
        return dict(row)

    def _fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Row | None:
        """
        Execute a query expected to return at most one row.
        """
        cursor = self._connection.execute(
            query,
            parameters,
        )
        return cursor.fetchone()

    def _fetch_all(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[sqlite3.Row]:
        """
        Execute a query returning zero or more rows.
        """
        cursor = self._connection.execute(
            query,
            parameters,
        )
        return cursor.fetchall()

    def _fetch_by_column(
        self,
        *,
        table: str,
        column: str,
        value: Any,
    ) -> list[sqlite3.Row]:
        """
        Fetch all rows where a column matches a value.
        """
        query = f"""
            SELECT *
            FROM {table}
            WHERE {column} = ?
        """

        return self._fetch_all(
            query,
            (value,),
        )

    def _delete(
        self,
        *,
        table: str,
        id_column: str,
        id_value: Any,
    ) -> None:
        """
        Delete a row by its identifier.
        """
        self._connection.execute(
            f"""
            DELETE FROM {table}
            WHERE {id_column} = ?
            """,
            (id_value,),
        )

    def _upsert(
        self,
        *,
        table: str,
        values: Mapping[str, Any],
    ) -> None:
        """
        Insert or update a row using SQLite's ON CONFLICT support.

        The supplied mapping must include an ``id`` column that serves
        as the table's primary key.
        """
        columns = list(values.keys())

        placeholders = ", ".join("?" for _ in columns)

        assignments = ", ".join(
            f"{column}=excluded.{column}"
            for column in columns
            if column != "id"
        )

        sql = f"""
            INSERT INTO {table}
            ({", ".join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(id)
            DO UPDATE SET
            {assignments}
        """

        self._connection.execute(
            sql,
            tuple(values[column] for column in columns),
        )
