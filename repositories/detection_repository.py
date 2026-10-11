from abc import ABC, abstractmethod
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

    @abstractmethod
    def get(
        self,
        detection_id: str,
    ) -> Detection | None:
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