from __future__ import annotations

import re
from typing import Any

import psycopg
from psycopg.rows import dict_row


class PostgreSQLConnection:
    """Adapts shared repository SQL to PostgreSQL."""

    def __init__(self, connection: psycopg.Connection) -> None:
        self._connection = connection

    def execute(self, query: str, parameters: tuple[Any, ...] = ()):
        query = re.sub(
            r"\busername\s*=\s*\?\s+COLLATE\s+NOCASE\b",
            "LOWER(username) = LOWER(?)",
            query,
            flags=re.IGNORECASE,
        )
        return self._connection.execute(query.replace("?", "%s"), parameters)

    def commit(self) -> None:
        self._connection.commit()

    def rollback(self) -> None:
        self._connection.rollback()

    def close(self) -> None:
        self._connection.close()


class PostgreSQLConnectionFactory:
    """Opens PostgreSQL connections and initializes the application schema."""

    def __init__(
        self,
        *,
        host: str,
        port: int,
        dbname: str,
        user: str,
        password: str,
    ) -> None:
        self._parameters = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
            "row_factory": dict_row,
        }

    def connect(self) -> PostgreSQLConnection:
        from infrastructure.postgres.schema import initialize_schema

        connection = psycopg.connect(**self._parameters)
        adapted = PostgreSQLConnection(connection)
        try:
            initialize_schema(adapted)
            adapted.commit()
        except Exception:
            adapted.rollback()
            adapted.close()
            raise
        return adapted
