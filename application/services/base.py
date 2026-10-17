from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class ApplicationService(
    ABC,
    Generic[RequestT, ResponseT],
):
    """
    Base class for all application services.

    Application services coordinate domain objects,
    repositories, and infrastructure to execute a
    single application use case.
    """

    @abstractmethod
    def execute(
        self,
        request: RequestT,
    ) -> ResponseT:
        """
        Execute the application use case.
        """
        raise NotImplementedError
