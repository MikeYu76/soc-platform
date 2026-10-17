from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

import pytest

from application.dto.identifier import IdentifierRequest
from application.exceptions.not_found import ResourceNotFoundError
from application.services.get_case import GetCaseService
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork
from tests.test_sqlite_persistence_roundtrip import make_case


@pytest.fixture
def connection_factory() -> SQLiteConnectionFactory:
    with tempfile.TemporaryDirectory() as tmpdir:
        database = Path(tmpdir) / "test.db"
        yield SQLiteConnectionFactory(str(database))


def test_get_existing_case(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    case = make_case()

    with SQLiteUnitOfWork(connection_factory) as uow:
        uow.cases.save(case)
        uow.commit()

    service = GetCaseService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
    )

    response = service.execute(
        IdentifierRequest(
            id=str(case.id),
        )
    )

    assert response.case == case


def test_get_missing_case(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    service = GetCaseService(
        unit_of_work_factory=lambda: SQLiteUnitOfWork(
            connection_factory,
        ),
    )

    with pytest.raises(ResourceNotFoundError):
        service.execute(
            IdentifierRequest(
                id=str(uuid4()),
            )
        )
