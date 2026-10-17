from abc import ABC, abstractmethod

from case.models import Case


class CaseProcessor(ABC):
    """
    Base interface for post-creation case processors.

    Case processors modify or enrich cases after they have
    been created by the CaseEngine.
    """

    @abstractmethod
    def process(
        self,
        cases: list[Case],
    ) -> list[Case]:
        raise NotImplementedError
