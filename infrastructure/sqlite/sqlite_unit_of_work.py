from __future__ import annotations

import sqlite3
from typing import Self

from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.exceptions import UnitOfWorkNotActiveError
from infrastructure.sqlite.sqlite_alert_repository import SQLiteAlertRepository
from infrastructure.sqlite.sqlite_case_repository import SQLiteCaseRepository
from infrastructure.sqlite.sqlite_detection_repository import (
    SQLiteDetectionRepository,
)
from infrastructure.sqlite.sqlite_event_repository import SQLiteEventRepository
from infrastructure.sqlite.sqlite_user_repository import SQLiteUserRepository
from repositories.alert_repository import AlertRepository
from repositories.case_repository import CaseRepository
from repositories.detection_repository import DetectionRepository
from repositories.event_repository import EventRepository
from repositories.unit_of_work import UnitOfWork
from repositories.user_repository import UserRepository


class SQLiteUnitOfWork(UnitOfWork):
    """
    SQLite implementation of the UnitOfWork pattern.

    A database connection is opened when entering the UnitOfWork
    and closed when leaving it. All repositories share the same
    connection, ensuring operations participate in the same
    transaction.
    """

    def __init__(
        self,
        connection_factory: SQLiteConnectionFactory,
    ) -> None:
        self._connection_factory = connection_factory

        self._connection: sqlite3.Connection | None = None

        self._events: SQLiteEventRepository | None = None
        self._detections: SQLiteDetectionRepository | None = None
        self._alerts: SQLiteAlertRepository | None = None
        self._cases: SQLiteCaseRepository | None = None
        self._users: SQLiteUserRepository | None = None

    def __enter__(self) -> Self:
        self._connection = self._connection_factory.connect()

        self._events = SQLiteEventRepository(self._connection)
        self._detections = SQLiteDetectionRepository(self._connection)
        self._alerts = SQLiteAlertRepository(self._connection)
        self._cases = SQLiteCaseRepository(self._connection)
        self._users = SQLiteUserRepository(self._connection)

        return self

    @property
    def events(self) -> EventRepository:
        if self._events is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._events

    @property
    def detections(self) -> DetectionRepository:
        if self._detections is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._detections

    @property
    def alerts(self) -> AlertRepository:
        if self._alerts is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._alerts

    @property
    def cases(self) -> CaseRepository:
        if self._cases is None:
            raise UnitOfWorkNotActiveError("UnitOfWork has not been entered.")
        return self._cases

    @property
    def users(self) -> UserRepository:
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
