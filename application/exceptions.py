class ApplicationError(Exception):
    """
    Base exception for application services.
    """


class ValidationError(ApplicationError):
    """
    Raised when application input is invalid.
    """


class UseCaseError(ApplicationError):
    """
    Raised when a use case cannot be completed.
    """
