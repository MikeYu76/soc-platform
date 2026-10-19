from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from identity.user import User
from infrastructure.sqlite.mappers.base_mapper import BaseMapper


class UserMapper(BaseMapper):
    @classmethod
    def to_record(cls, user: User) -> dict[str, Any]:
        return {
            "id": str(user.user_id),
            "username": user.username,
            "role": user.role.value,
            "is_active": int(user.is_active),
            "created_at": user.created_at.isoformat(),
            "data": cls.serialize(user),
        }

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> User:
        return cls.deserialize(User, record["data"])
