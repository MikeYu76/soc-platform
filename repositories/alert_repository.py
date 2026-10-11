from abc import ABC, abstractmethod
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

    @abstractmethod
    def get(
        self,
        alert_id: UUID,
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
        alert_id: UUID,
    ) -> None:
        raise NotImplementedError