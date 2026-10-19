class InvalidCredentialsError(Exception):
    """Raised when a login name or password is invalid."""


class UserAlreadyExistsError(Exception):
    """Raised when a requested username is already registered."""


class AuthenticationConfigurationError(Exception):
    """Raised when authentication settings are missing or invalid."""
