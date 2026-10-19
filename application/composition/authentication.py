from __future__ import annotations

import re

from application.composition.dependencies import settings, unit_of_work_factory
from common.user_role import UserRole
from identity.passwords import hash_password
from identity.tokens import TokenConfigurationError, _signing_key
from identity.user import User


def ensure_bootstrap_administrator() -> None:
    username = settings.bootstrap_admin_username
    configured_password = settings.bootstrap_admin_password

    if username is None and configured_password is None:
        return
    if not username or configured_password is None:
        raise RuntimeError(
            "Set both SOC_BOOTSTRAP_ADMIN_USERNAME and "
            "SOC_BOOTSTRAP_ADMIN_PASSWORD, or leave both unset."
        )

    password = configured_password.get_secret_value()
    if len(password) < 12 or password.lower().startswith("replace"):
        raise RuntimeError(
            "SOC_BOOTSTRAP_ADMIN_PASSWORD must be at least 12 characters "
            "and must not be a placeholder."
        )

    try:
        _signing_key(settings)
    except TokenConfigurationError as exc:
        raise RuntimeError(str(exc)) from exc

    normalized_username = username.strip()
    if re.fullmatch(r"[A-Za-z0-9._-]{3,64}", normalized_username) is None:
        raise RuntimeError(
            "SOC_BOOTSTRAP_ADMIN_USERNAME must be 3 to 64 characters and "
            "use only letters, numbers, dots, underscores, or hyphens."
        )
    with unit_of_work_factory() as uow:
        if uow.users.get_by_username(normalized_username) is None:
            uow.users.add(
                User(
                    username=normalized_username,
                    password_hash=hash_password(password),
                    role=UserRole.ADMINISTRATOR,
                )
            )
            uow.commit()
