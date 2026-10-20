from __future__ import annotations

from infrastructure.postgres.connection import PostgreSQLConnection
from infrastructure.postgres.migrations import Migration
from infrastructure.postgres.migrations.versions.v0001_initial_schema import (
    MIGRATION as INITIAL_SCHEMA_MIGRATION,
)

MIGRATIONS: tuple[Migration, ...] = (INITIAL_SCHEMA_MIGRATION,)


def upgrade_schema(connection: PostgreSQLConnection) -> None:
    """Apply migrations that are not yet recorded in the database."""
    versions = tuple(migration.version for migration in MIGRATIONS)
    if versions != tuple(sorted(set(versions))):
        raise ValueError("Migration versions must be unique and sorted.")

    connection.execute(
        """CREATE TABLE IF NOT EXISTS soc_schema_migrations (
            version TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        )"""
    )
    applied_rows = connection.execute(
        "SELECT version FROM soc_schema_migrations"
    ).fetchall()
    applied_versions = {str(row["version"]) for row in applied_rows}
    known_versions = set(versions)
    unknown_versions = applied_versions - known_versions
    if unknown_versions:
        raise RuntimeError(
            "Database contains unknown schema migration version(s): "
            f"{', '.join(sorted(unknown_versions))}."
        )

    for migration in MIGRATIONS:
        if migration.version in applied_versions:
            continue
        for statement in migration.statements:
            connection.execute(statement)
        connection.execute(
            "INSERT INTO soc_schema_migrations (version) VALUES (?)",
            (migration.version,),
        )
