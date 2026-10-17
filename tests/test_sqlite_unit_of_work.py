import pytest

from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.exceptions import UnitOfWorkNotActiveError
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


@pytest.fixture
def connection_factory() -> SQLiteConnectionFactory:
    return SQLiteConnectionFactory(":memory:")


def test_repositories_unavailable_before_enter(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    uow = SQLiteUnitOfWork(connection_factory)

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.events

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.detections

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.alerts

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.cases


def test_repositories_available_inside_context(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    with SQLiteUnitOfWork(connection_factory) as uow:
        assert uow.events is not None
        assert uow.detections is not None
        assert uow.alerts is not None
        assert uow.cases is not None


def test_repositories_unavailable_after_exit(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    uow = SQLiteUnitOfWork(connection_factory)

    with uow:
        pass

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.events

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.detections

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.alerts

    with pytest.raises(UnitOfWorkNotActiveError):
        _ = uow.cases


def test_commit_outside_context_raises(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    uow = SQLiteUnitOfWork(connection_factory)

    with pytest.raises(UnitOfWorkNotActiveError):
        uow.commit()


def test_rollback_outside_context_raises(
    connection_factory: SQLiteConnectionFactory,
) -> None:
    uow = SQLiteUnitOfWork(connection_factory)

    with pytest.raises(UnitOfWorkNotActiveError):
        uow.rollback()
