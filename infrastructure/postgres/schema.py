from __future__ import annotations

from infrastructure.postgres.connection import PostgreSQLConnection
from infrastructure.postgres.migrations.runner import upgrade_schema


def initialize_schema(connection: PostgreSQLConnection) -> None:
    """Apply all pending PostgreSQL schema migrations."""
    upgrade_schema(connection)
