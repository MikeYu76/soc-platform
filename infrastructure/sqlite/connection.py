from __future__ import annotations

import sqlite3
from pathlib import Path

from infrastructure.sqlite.schema import initialize_schema


class SQLiteConnectionFactory:
    """
    Creates configured SQLite connections.

    Automatically initializes the database schema.
    """

    def __init__(
        self,
        database: str = ":memory:",
    ) -> None:
        self._database = database

    @property
    def database(
        self,
    ) -> str:
        return self._database

    def connect(
        self,
    ) -> sqlite3.Connection:
        """
        Create and configure a SQLite connection.
        """

        if self._database != ":memory:":
            Path(self._database).parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        connection = sqlite3.connect(self._database)

        connection.row_factory = sqlite3.Row

        connection.execute(
            "PRAGMA foreign_keys = ON",
        )

        initialize_schema(connection)

        return connection
