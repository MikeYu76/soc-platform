from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from case.models import Case

from common.case_priority import CasePriority
from common.case_status import CaseStatus


class CaseRepository(ABC):
    """
    Repository interface for Case persistence.
    """

    @abstractmethod
    def save(
        self,
        case: Case,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        case: Case,
    ) -> None:
        raise NotImplementedError

    def save_all(
        self,
        cases: Iterable[Case],
    ) -> None:
        """
        Persist multiple cases.

        Repositories may override this with a more efficient
        implementation.
        """
        for case in cases:
            self.save(case)

    @abstractmethod
    def get(
        self,
        id: UUID,
    ) -> Case | None:
        raise NotImplementedError

    @abstractmethod
    def list_active(
        self,
    ) -> list[Case]:
        raise NotImplementedError

    @abstractmethod
    def list_by_status(
        self,
        status: CaseStatus,
    ) -> list[Case]:
        raise NotImplementedError

    @abstractmethod
    def list_by_priority(
        self,
        priority: CasePriority,
    ) -> list[Case]:
        raise NotImplementedError

    @abstractmethod
    def list_assigned_to(
        self,
        team: str,
    ) -> list[Case]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        id: UUID,
    ) -> None:
        raise NotImplementedError