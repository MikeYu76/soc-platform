import pytest
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from api.main import app
from api.routes.operations import get_opensearch_indexing_status
from api.security import require_roles
from application.services.get_event_index_outbox_status import (
    GetEventIndexOutboxStatusService,
)
from common.user_role import UserRole
from identity.user import User
from infrastructure.sqlite.connection import SQLiteConnectionFactory
from infrastructure.sqlite.sqlite_unit_of_work import SQLiteUnitOfWork


def test_administrator_can_read_opensearch_indexing_status() -> None:
    service = GetEventIndexOutboxStatusService(
        lambda: SQLiteUnitOfWork(SQLiteConnectionFactory(":memory:")),
        enabled=True,
    )
    administrator = User(
        username="test-admin",
        password_hash="unused",
        role=UserRole.ADMINISTRATOR,
    )

    response = get_opensearch_indexing_status(
        service=service,
        _administrator=administrator,
    )

    assert jsonable_encoder(response) == {
        "enabled": True,
        "pending_count": 0,
        "ready_count": 0,
        "retry_wait_count": 0,
        "retrying_count": 0,
        "oldest_pending_at": None,
        "oldest_pending_age_seconds": None,
        "max_attempts": 0,
    }
    assert "/operations/opensearch-indexing" in app.openapi()["paths"]


def test_non_administrator_is_denied_opensearch_indexing_status() -> None:
    analyst = User(
        username="test-analyst",
        password_hash="unused",
        role=UserRole.ANALYST,
    )
    administrator_guard = require_roles(UserRole.ADMINISTRATOR)

    with pytest.raises(HTTPException) as error:
        administrator_guard(user=analyst)

    assert error.value.status_code == 403
