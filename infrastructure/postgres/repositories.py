from infrastructure.sqlite.sqlite_alert_repository import SQLiteAlertRepository
from infrastructure.sqlite.sqlite_case_repository import SQLiteCaseRepository
from infrastructure.sqlite.sqlite_detection_repository import SQLiteDetectionRepository
from infrastructure.sqlite.sqlite_event_repository import SQLiteEventRepository
from infrastructure.sqlite.sqlite_user_repository import SQLiteUserRepository


class PostgreSQLEventRepository(SQLiteEventRepository):
    """Event repository using PostgreSQL."""


class PostgreSQLDetectionRepository(SQLiteDetectionRepository):
    """Detection repository using PostgreSQL."""


class PostgreSQLAlertRepository(SQLiteAlertRepository):
    """Alert repository using PostgreSQL."""


class PostgreSQLCaseRepository(SQLiteCaseRepository):
    """Case repository using PostgreSQL."""


class PostgreSQLUserRepository(SQLiteUserRepository):
    """User repository using PostgreSQL."""
