from abc import ABC, abstractmethod

from alert.models import Alert

from case.models import Case


class CaseRule(ABC):
    """
    Base interface for case creation policies.
    """

    @abstractmethod
    def generate(
        self,
        alerts: list[Alert],
    ) -> list[Case]:
        raise NotImplementedError