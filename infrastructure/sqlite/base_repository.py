from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class SQLiteRepository:
    """
    Shared functionality for SQLite repository implementations.
    """

    def __init__(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        self._connection = connection

    @staticmethod
    def _serialize(
        model: BaseModel,
    ) -> str:
        return model.model_dump_json()

    @staticmethod
    def _deserialize(
        model_type: type[T],
        payload: str,
    ) -> T:
        return model_type.model_validate_json(payload)

    @staticmethod
    def _row_to_dict(
        row: sqlite3.Row | None,
    ) -> dict[str, Any] | None:
        if row is None:
            return None

        return dict(row)

    def _fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Row | None:
        cursor = self._connection.execute(query, parameters)
        return cursor.fetchone()

    def _fetch_all(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[sqlite3.Row]:
        cursor = self._connection.execute(query, parameters)
        return list(cursor.fetchall())

    def _fetch_by_column(
        self,
        *,
        table: str,
        column: str,
        value: Any,
    ) -> list[sqlite3.Row]:
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