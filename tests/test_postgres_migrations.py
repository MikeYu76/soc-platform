import sqlite3
from typing import Any, cast

from infrastructure.postgres.connection import PostgreSQLConnection
from infrastructure.postgres.migrations.runner import upgrade_schema
from infrastructure.postgres.schema import initialize_schema


class SQLiteMigrationConnection:
    """Run portable migration SQL against SQLite for fast unit tests."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def execute(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Cursor:
        return self._connection.execute(query, parameters)


def test_initial_migration_adopts_existing_schema_and_runs_once() -> None:
    raw_connection = sqlite3.connect(":memory:")
    raw_connection.row_factory = sqlite3.Row
    raw_connection.execute(
        """CREATE TABLE events (
            id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, log_source TEXT NOT NULL,
            event_type TEXT NOT NULL, hostname TEXT, username TEXT, source_ip TEXT,
            destination_ip TEXT, data TEXT NOT NULL
        )"""
    )
    raw_connection.execute(
        "INSERT INTO events (id, timestamp, log_source, event_type, data) "
        "VALUES (?, ?, ?, ?, ?)",
        ("existing-event", "2026-01-01T00:00:00Z", "test", "unknown", "{}"),
    )
    connection = SQLiteMigrationConnection(raw_connection)
    postgres_connection = cast(PostgreSQLConnection, connection)

    initialize_schema(postgres_connection)
    raw_connection.commit()
    initialize_schema(postgres_connection)
    raw_connection.commit()

    event = raw_connection.execute(
        "SELECT id FROM events WHERE id = ?",
        ("existing-event",),
    ).fetchone()
    versions = raw_connection.execute(
        "SELECT version FROM soc_schema_migrations"
    ).fetchall()
    tables = {
        row["name"]
        for row in raw_connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }

    assert event is not None
    assert [row["version"] for row in versions] == ["0001_initial_schema"]
    assert {
        "events",
        "detections",
        "alerts",
        "cases",
        "users",
        "event_index_outbox",
    }.issubset(tables)
    raw_connection.close()


def test_migration_runner_rejects_unknown_recorded_version() -> None:
    raw_connection = sqlite3.connect(":memory:")
    raw_connection.row_factory = sqlite3.Row
    raw_connection.execute(
        """CREATE TABLE soc_schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    raw_connection.execute(
        "INSERT INTO soc_schema_migrations (version) VALUES (?)",
        ("9999_unknown",),
    )
    connection = SQLiteMigrationConnection(raw_connection)

    try:
        upgrade_schema(cast(PostgreSQLConnection, connection))
    except RuntimeError as exc:
        assert "9999_unknown" in str(exc)
    else:
        raise AssertionError("Unknown migration versions must stop startup.")
    finally:
        raw_connection.close()
