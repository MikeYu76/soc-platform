from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt

from application.composition.settings import Settings
from common.user_role import UserRole

ALGORITHM = "HS256"


class TokenConfigurationError(RuntimeError):
    pass


def _signing_key(settings: Settings) -> str:
    secret = settings.jwt_secret.get_secret_value()
    if len(secret.encode("utf-8")) < 32 or secret.lower().startswith("replace"):
        raise TokenConfigurationError(
            "SOC_JWT_SECRET must be a random secret of at least 32 characters."
        )
    return secret


def create_access_token(
    username: str,
    role: UserRole,
    settings: Settings,
) -> str:
    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode(
        {
            "sub": username,
            "role": role.value,
            "iat": now,
            "exp": expires_at,
        },
        _signing_key(settings),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str, settings: Settings) -> dict[str, object]:
    return jwt.decode(
        token,
        _signing_key(settings),
        algorithms=[ALGORITHM],
        options={"require": ["sub", "role", "iat", "exp"]},
    )
