from infrastructure.sqlite.sqlite_event_index_outbox_repository import (
    SQLiteEventIndexOutboxRepository,
)


class PostgreSQLEventIndexOutboxRepository(SQLiteEventIndexOutboxRepository):
    """PostgreSQL implementation using the shared SQL repository behavior."""
