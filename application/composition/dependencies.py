from __future__ import annotations

from collections.abc import Callable

from alert.factory import AlertFactory

from application.composition.settings import Settings

from case.factory import CaseFactory

from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork

from repositories.unit_of_work import UnitOfWork


class Dependencies:
    """
    Shared application dependencies.

    This class owns infrastructure components and reusable
    factories. Higher-level services compose these dependencies
    into complete application services.
    """

    def __init__(
        self,
        settings: Settings | None = None,
    ) -> None:
        self.settings = settings or Settings()

        self.connection_factory = SQLiteConnectionFactory(
            str(self.settings.database_path),
        )

        self.alert_factory = AlertFactory()

        self.case_factory = CaseFactory()

    def unit_of_work_factory(
        self,
    ) -> UnitOfWork:
        """
        Create a new Unit of Work.
        """
        return SQLiteUnitOfWork(
            self.connection_factory,
        )