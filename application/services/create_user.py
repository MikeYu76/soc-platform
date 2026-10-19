from __future__ import annotations

import re
from collections.abc import Callable

from application.dto.auth import CreateUserRequest, CreateUserResponse
from application.exceptions.auth import UserAlreadyExistsError
from application.services.base import ApplicationService
from identity.passwords import hash_password
from identity.user import User
from repositories.unit_of_work import UnitOfWork

_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9._-]{3,64}$")


class CreateUserService(
    ApplicationService[CreateUserRequest, CreateUserResponse],
):
    def __init__(self, unit_of_work_factory: Callable[[], UnitOfWork]) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        username = request.username.strip()
        if _USERNAME_PATTERN.fullmatch(username) is None:
            raise ValueError(
                "Username must be 3 to 64 characters and use only letters, "
                "numbers, dots, underscores, or hyphens."
            )

        with self._unit_of_work_factory() as uow:
            if uow.users.get_by_username(username) is not None:
                raise UserAlreadyExistsError(
                    f"Username '{username}' is already registered."
                )

            user = User(
                username=username,
                password_hash=hash_password(request.password),
                role=request.role,
            )
            uow.users.add(user)
            uow.commit()

        return CreateUserResponse.from_user(user)
