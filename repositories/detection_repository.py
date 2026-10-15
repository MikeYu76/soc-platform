from abc import ABC, abstractmethod
from collections.abc import Iterable
from datetime import datetime

from common.detection import Detection, Severity


class DetectionRepository(ABC):
    """
    Repository interface for Detection persistence.
    """

    @abstractmethod
    def save(
        self,
        detection: Detection,
    ) -> None:
        raise NotImplementedError

    def save_all(
        self,
        detections: Iterable[Detection],
    ) -> None:
        """
        Persist multiple detections.

        Repositories may override this with a more efficient
        implementation.
        """
        for detection in detections:
            self.save(detection)

    @abstractmethod
    def get(
        self,
        id: str,
    ) -> Detection | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Detection]:
        raise NotImplementedError

    @abstractmethod
    def list_by_rule(
        self,
        rule_id: str,
    ) -> list[Detection]:
        raise NotImplementedError

    @abstractmethod
    def list_by_severity(
        self,
        severity: Severity,
    ) -> list[Detection]:
        raise NotImplementedError

    @abstractmethod
    def list_since(
        self,
        since: datetime,
    ) -> list[Detection]:
        raise NotImplementedError