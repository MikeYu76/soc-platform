from __future__ import annotations

from datetime import UTC, datetime

from infrastructure.sqlite.base_repository import SQLiteRepository
from repositories.event_index_outbox import (
    EventIndexOutboxRepository,
    EventIndexOutboxStatus,
    PendingEventIndex,
)


class SQLiteEventIndexOutboxRepository(SQLiteRepository, EventIndexOutboxRepository):
    """SQL implementation compatible with SQLite and PostgreSQL adapters."""

    TABLE = "event_index_outbox"

    def enqueue(self, event_id: str) -> None:
        now = datetime.now(UTC).isoformat()
        self._connection.execute(
            f"""
            INSERT INTO {self.TABLE}
                (event_id, created_at, attempts, next_attempt_at, last_error)
            VALUES (?, ?, 0, ?, NULL)
            ON CONFLICT(event_id) DO NOTHING
            """,
            (event_id, now, now),
        )

    def get_pending(self, limit: int) -> list[PendingEventIndex]:
        now = datetime.now(UTC).isoformat()
        rows = self._fetch_all(
            f"""
            SELECT event_id, attempts
            FROM {self.TABLE}
            WHERE next_attempt_at <= ?
            ORDER BY created_at, event_id
            LIMIT ?
            """,
            (now, limit),
        )
        return [
            PendingEventIndex(
                event_id=str(row["event_id"]),
                attempts=int(row["attempts"]),
            )
            for row in rows
        ]

    def get_status(self) -> EventIndexOutboxStatus:
        now = datetime.now(UTC).isoformat()
        row = self._fetch_one(
            f"""
            SELECT
                COUNT(*) AS pending_count,
                COALESCE(SUM(CASE WHEN next_attempt_at <= ? THEN 1 ELSE 0 END), 0)
                    AS ready_count,
                COALESCE(SUM(CASE WHEN next_attempt_at > ? THEN 1 ELSE 0 END), 0)
                    AS retry_wait_count,
                COALESCE(SUM(CASE WHEN attempts > 0 THEN 1 ELSE 0 END), 0)
                    AS retrying_count,
                MIN(created_at) AS oldest_created_at,
                COALESCE(MAX(attempts), 0) AS max_attempts
            FROM {self.TABLE}
            """,
            (now, now),
        )
        if row is None:
            return EventIndexOutboxStatus(
                pending_count=0,
                ready_count=0,
                retry_wait_count=0,
                retrying_count=0,
                oldest_created_at=None,
                max_attempts=0,
            )
        return EventIndexOutboxStatus(
            pending_count=int(row["pending_count"]),
            ready_count=int(row["ready_count"]),
            retry_wait_count=int(row["retry_wait_count"]),
            retrying_count=int(row["retrying_count"]),
            oldest_created_at=(
                str(row["oldest_created_at"])
                if row["oldest_created_at"] is not None
                else None
            ),
            max_attempts=int(row["max_attempts"]),
        )

    def mark_delivered(self, event_id: str) -> None:
        self._connection.execute(
            f"DELETE FROM {self.TABLE} WHERE event_id = ?",
            (event_id,),
        )

    def schedule_retry(
        self,
        event_id: str,
        next_attempt_at: str,
        error_type: str,
    ) -> None:
        self._connection.execute(
            f"""
            UPDATE {self.TABLE}
            SET attempts = attempts + 1,
                next_attempt_at = ?,
                last_error = ?
            WHERE event_id = ?
            """,
            (next_attempt_at, error_type[:200], event_id),
        )
