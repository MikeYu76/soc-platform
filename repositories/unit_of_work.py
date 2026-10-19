from abc import ABC, abstractmethod
from typing import Self

from repositories.alert_repository import AlertRepository
from repositories.case_repository import CaseRepository
from repositories.detection_repository import DetectionRepository
from repositories.event_repository import EventRepository
from repositories.user_repository import UserRepository


class UnitOfWork(ABC):
    """
    Coordinates repository access and transaction boundaries.

    A UnitOfWork groups related persistence operations into a
    single transaction, ensuring they either all succeed or
    all fail together.
    """

    @property
    @abstractmethod
    def events(self) -> EventRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def detections(self) -> DetectionRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def alerts(self) -> AlertRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def cases(self) -> CaseRepository:
        raise NotImplementedError

    @property
    @abstractmethod
    def users(self) -> UserRepository:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        """
        Persist all pending changes.
        """
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        """
        Roll back the current transaction.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        """
        Release any underlying resources.
        """
        raise NotImplementedError

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self.close()
