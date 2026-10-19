from __future__ import annotations

from pydantic import BaseModel

from common.user_role import UserRole
from identity.user import User, UserPublic


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserPublic


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: UserRole


class CreateUserResponse(BaseModel):
    user: UserPublic

    @classmethod
    def from_user(cls, user: User) -> CreateUserResponse:
        return cls(user=UserPublic.from_user(user))
