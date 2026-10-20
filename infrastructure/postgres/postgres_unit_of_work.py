from __future__ import annotations

from infrastructure.postgres.connection import PostgreSQLConnection, PostgreSQLConnectionFactory
from infrastructure.postgres.repositories import (
    PostgreSQLAlertRepository,
    PostgreSQLCaseRepository,
    PostgreSQLDetectionRepository,
    PostgreSQLEventRepository,
    PostgreSQLUserRepository,
)
from infrastructure.sqlite.exceptions import UnitOfWorkNotActiveError
from repositories.unit_of_work import UnitOfWork


class PostgreSQLUnitOfWork(UnitOfWork):
    """PostgreSQL Unit of Work with one shared connection and transaction."""

    def __init__(self, connection_factory: PostgreSQLConnectionFactory) -> None:
        self._connection_factory = connection_factory
        self._connection: PostgreSQLConnection | None = None
        self._events: PostgreSQLEventRepository | None = None
        self._detections: PostgreSQLDetectionRepository | None = None
        self._alerts: PostgreSQLAlertRepository | None = None
        self._cases: PostgreSQLCaseRepository | None = None
        self._users: PostgreSQLUserRepository | None = None

    def __enter__(self) -> PostgreSQLUnitOfWork:
        self._connection = self._connection_factory.connect()
        self._events = PostgreSQLEventRepository(self._connection)
        self._detections = PostgreSQLDetectionRepository(self._connection)
        self._alerts = PostgreSQLAlertRepository(self._connection)
        self._cases = PostgreSQLCaseRepository(self._connection)
        self._users = PostgreSQLUserRepository(self._connection)
        return self

    @property
    def events(self) -> PostgreSQLEventRepository:
        if self._events is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._events

    @property
    def detections(self) -> PostgreSQLDetectionRepository:
        if self._detections is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._detections

    @property
    def alerts(self) -> PostgreSQLAlertRepository:
        if self._alerts is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._alerts

    @property
    def cases(self) -> PostgreSQLCaseRepository:
        if self._cases is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._cases

    @property
    def users(self) -> PostgreSQLUserRepository:
        if self._users is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._users

    def commit(self) -> None:
        if self._connection is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        self._connection.commit()

    def rollback(self) -> None:
        if self._connection is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        self._connection.rollback()

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
        self._connection = None
        self._events = None
        self._detections = None
        self._alerts = None
        self._cases = None
        self._users = None
