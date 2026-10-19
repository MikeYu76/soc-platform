from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from common.user_role import UserRole


class User(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    username: str
    password_hash: str
    role: UserRole
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserPublic(BaseModel):
    user_id: UUID
    username: str
    role: UserRole
    is_active: bool

    @classmethod
    def from_user(cls, user: User) -> UserPublic:
        return cls(
            user_id=user.user_id,
            username=user.username,
            role=user.role,
            is_active=user.is_active,
        )
