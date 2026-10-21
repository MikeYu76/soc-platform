from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from api.dependencies import (
    get_event_index_outbox_monitor,
    get_get_event_index_outbox_status_service,
)
from api.security import require_roles
from application.dto.event_index_outbox import (
    GetEventIndexOutboxStatusResponse,
)
from application.services.get_event_index_outbox_status import (
    GetEventIndexOutboxStatusService,
)
from common.user_role import UserRole
from identity.user import User
from infrastructure.opensearch.outbox_monitor import EventIndexOutboxMonitor

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get(
    "/opensearch-indexing",
    response_model=GetEventIndexOutboxStatusResponse,
    summary="Get OpenSearch indexing queue status",
    description=(
        "Returns aggregate indexing queue counts and the age of the oldest "
        "pending event. Administrator access is required."
    ),
)
def get_opensearch_indexing_status(
    service: GetEventIndexOutboxStatusService = Depends(
        get_get_event_index_outbox_status_service
    ),
    _administrator: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> GetEventIndexOutboxStatusResponse:
    return service.execute()


@router.get(
    "/opensearch-indexing/metrics",
    response_class=PlainTextResponse,
    summary="Get OpenSearch indexing metrics",
    description=(
        "Returns Prometheus-format aggregate queue metrics. "
        "Administrator access is required."
    ),
)
def get_opensearch_indexing_metrics(
    monitor: EventIndexOutboxMonitor = Depends(get_event_index_outbox_monitor),
    _administrator: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> PlainTextResponse:
    return PlainTextResponse(
        monitor.to_prometheus_text(),
        media_type="text/plain; version=0.0.4; charset=utf-8",
    )
