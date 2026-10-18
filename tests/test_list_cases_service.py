from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from application.dto.case import ListCasesRequest
from application.services.list_cases import ListCasesService
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork
from repositories.queries.case_query import CaseQuery
from tests.test_sqlite_persistence_roundtrip import make_case


@pytest.fixture
def connection_factory() -> SQLiteConnectionFactory:
    with tempfile.TemporaryDirectory() as tmpdir:
        database = Path(tmpdir) / "test.db"
        yield SQLiteConnectionFactory(str(database))


def test_list_active_cases(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = make_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    service = ListCasesService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
    )

    response = service.execute(
        ListCasesRequest(
            query=CaseQuery(),
        )
    )

    assert len(response.cases) == 1
    assert response.cases[0] == case
