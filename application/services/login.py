from __future__ import annotations

from collections.abc import Callable

from application.composition.settings import Settings
from application.dto.auth import LoginRequest, LoginResponse
from application.exceptions.auth import (
    AuthenticationConfigurationError,
    InvalidCredentialsError,
)
from application.services.base import ApplicationService
from identity.passwords import verify_password
from identity.tokens import TokenConfigurationError, create_access_token
from identity.user import UserPublic
from repositories.unit_of_work import UnitOfWork


class LoginService(ApplicationService[LoginRequest, LoginResponse]):
    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWork],
        settings: Settings,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory
        self._settings = settings

    def execute(self, request: LoginRequest) -> LoginResponse:
        username = request.username.strip()
        with self._unit_of_work_factory() as uow:
            user = uow.users.get_by_username(username)

        if (
            user is None
            or not user.is_active
            or not verify_password(request.password, user.password_hash)
        ):
            raise InvalidCredentialsError("Invalid username or password.")

        try:
            token = create_access_token(
                username=user.username,
                role=user.role,
                settings=self._settings,
            )
        except TokenConfigurationError as exc:
            raise AuthenticationConfigurationError(str(exc)) from exc

        return LoginResponse(
            access_token=token,
            expires_in=self._settings.access_token_expire_minutes * 60,
            user=UserPublic.from_user(user),
        )
