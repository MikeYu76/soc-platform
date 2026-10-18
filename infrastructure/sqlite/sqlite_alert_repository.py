from __future__ import annotations

from uuid import UUID

from alert.models import Alert
from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.alert_mapper import AlertMapper
from repositories.alert_repository import AlertRepository
from repositories.queries.alert_query import AlertQuery


class SQLiteAlertRepository(
    SQLiteRepository,
    AlertRepository,
):
    """
    SQLite implementation of AlertRepository.
    """

    TABLE = "alerts"

    def save(
        self,
        alert: Alert,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=AlertMapper.to_record(alert),
        )

    def update(
        self,
        alert: Alert,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=AlertMapper.to_record(alert),
        )

    def get(
        self,
        id: UUID,
    ) -> Alert | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM alerts
            WHERE id = ?
            """,
            (str(id),),
        )

        if row is None:
            return None

        return AlertMapper.from_record(
            self._row_to_dict(row),
        )

    def search(
        self,
        query: AlertQuery,
    ) -> list[Alert]:
        sql = """
            SELECT *
            FROM alerts
            WHERE 1 = 1
        """

        parameters: list[object] = []

        if query.status is not None:
            sql += " AND status = ?"
            parameters.append(query.status.value)

        if query.severity is not None:
            sql += " AND severity = ?"
            parameters.append(query.severity.value)

        rows = self._fetch_all(
            sql,
            tuple(parameters),
        )

        return [
            AlertMapper.from_record(
                self._row_to_dict(row),
            )
            for row in rows
        ]

    def delete(
        self,
        id: UUID,
    ) -> None:
        self._delete(
            table=self.TABLE,
            id_column="id",
            id_value=str(id),
        )
