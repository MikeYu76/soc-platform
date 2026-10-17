from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from alert.models import Alert
from common.alert_status import AlertStatus
from common.detection import Severity


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
        """
        Persist changes to an existing alert.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        id: UUID,
    ) -> Alert | None:
        raise NotImplementedError

    @abstractmethod
    def list_active(
        self,
    ) -> list[Alert]:
        raise NotImplementedError

    @abstractmethod
    def list_by_status(
        self,
        status: AlertStatus,
    ) -> list[Alert]:
        raise NotImplementedError

    @abstractmethod
    def list_by_severity(
        self,
        severity: Severity,
    ) -> list[Alert]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        id: UUID,
    ) -> None:
        raise NotImplementedError
