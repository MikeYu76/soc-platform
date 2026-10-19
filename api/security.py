from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from application.composition.dependencies import settings, unit_of_work_factory
from common.user_role import UserRole
from identity.tokens import TokenConfigurationError, decode_access_token
from identity.user import User

_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    try:
        claims = decode_access_token(credentials.credentials, settings)
    except TokenConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except InvalidTokenError as exc:
        raise unauthorized from exc

    username = claims.get("sub")
    role_claim = claims.get("role")
    if not isinstance(username, str) or not isinstance(role_claim, str):
        raise unauthorized
    try:
        UserRole(role_claim)
    except ValueError as exc:
        raise unauthorized from exc

    with unit_of_work_factory() as uow:
        user = uow.users.get_by_username(username)

    if user is None or not user.is_active:
        raise unauthorized
    return user


def require_roles(*allowed_roles: UserRole) -> Callable[..., User]:
    def role_guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )
        return user

    return role_guard
