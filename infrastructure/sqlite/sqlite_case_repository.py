from __future__ import annotations

from uuid import UUID

from case.models import Case
from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.case_mapper import CaseMapper
from infrastructure.sqlite.queries.case_query_builder import (
    CaseQueryBuilder,
)
from repositories.case_repository import CaseRepository
from repositories.queries.case_query import CaseQuery


class SQLiteCaseRepository(
    SQLiteRepository,
    CaseRepository,
):
    """
    SQLite implementation of CaseRepository.
    """

    TABLE = "cases"

    def save(
        self,
        case: Case,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=CaseMapper.to_record(case),
        )

    def update(
        self,
        case: Case,
    ) -> None:
        self._upsert(
            table=self.TABLE,
            values=CaseMapper.to_record(case),
        )

    def get(
        self,
        id: UUID,
    ) -> Case | None:
        row = self._fetch_one(
            """
            SELECT *
            FROM cases
            WHERE id = ?
            """,
            (str(id),),
        )

        if row is None:
            return None

        return CaseMapper.from_record(
            self._row_to_dict(row),
        )

    def search(
        self,
        query: CaseQuery,
    ) -> list[Case]:
        sql, parameters = CaseQueryBuilder.build(
            query,
        )

        rows = self._fetch_all(
            sql,
            parameters,
        )

        return [
            CaseMapper.from_record(
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
