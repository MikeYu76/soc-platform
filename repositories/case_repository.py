from abc import ABC, abstractmethod
from collections.abc import Iterable
from uuid import UUID

from case.models import Case
from repositories.queries.case_query import CaseQuery


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
    def search(
        self,
        query: CaseQuery,
    ) -> list[Case]:
        """
        Search for cases using query criteria.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        id: UUID,
    ) -> None:
        raise NotImplementedError
