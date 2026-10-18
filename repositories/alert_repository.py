from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from alert.models import Alert
from repositories.queries.alert_query import AlertQuery


class AlertRepository(ABC):
    """
    Repository interface for Alert persistence.
    """

    @abstractmethod
    def save(
        self,
        alert: Alert,
    ) -> None:
        raise NotImplementedError

    def save_all(
        self,
        alerts: Iterable[Alert],
    ) -> None:
        """
        Persist multiple alerts.

        Repositories may override this with a more efficient
        implementation.
        """
        for alert in alerts:
            self.save(alert)

    @abstractmethod
    def update(
        self,
        alert: Alert,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        id: UUID,
    ) -> Alert | None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: AlertQuery,
    ) -> list[Alert]:
        """
        Search for alerts using query criteria.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        id: UUID,
    ) -> None:
        raise NotImplementedError
