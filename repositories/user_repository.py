from __future__ import annotations

from abc import ABC, abstractmethod

from identity.user import User


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError
