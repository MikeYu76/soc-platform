class UnitOfWorkNotActiveError(RuntimeError):
    """Raised when a UnitOfWork is used outside an active context."""

    def __init__(
        self,
        message: str = (
            "UnitOfWork has not been entered. "
            "Use 'with SQLiteUnitOfWork(...) as uow:' before "
            "accessing repositories or transaction methods."
        ),
    ) -> None:
        super().__init__(message)