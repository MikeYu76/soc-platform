from contextlib import asynccontextmanager
from threading import Event, Thread

from fastapi import FastAPI

from api.exception_handlers import register_exception_handlers
from api.routes import (
    alerts_router,
    auth_router,
    cases_router,
    events_router,
    operations_router,
)
from application.composition.authentication import ensure_bootstrap_administrator
from application.composition.dependencies import (
    event_index_outbox_monitor,
    event_indexer,
    unit_of_work_factory,
)
from infrastructure.opensearch.outbox_worker import run_event_index_outbox_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    is_testing = getattr(app.state, "testing", False)
    if not is_testing:
        ensure_bootstrap_administrator()

    worker_stop = Event()
    worker_thread: Thread | None = None
    if not is_testing and event_indexer is not None:
        worker_thread = Thread(
            target=run_event_index_outbox_worker,
            args=(unit_of_work_factory, event_indexer, worker_stop),
            kwargs={"monitor": event_index_outbox_monitor},
            name="opensearch-outbox-worker",
            daemon=True,
        )
        worker_thread.start()

    try:
        yield
    finally:
        if worker_thread is not None:
            worker_stop.set()
            worker_thread.join(timeout=20)


app = FastAPI(
    title="SOC Platform",
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(cases_router)
app.include_router(auth_router)
app.include_router(operations_router)


@app.get("/health")
def health() -> dict[str, str]:
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "SOC Platform",
        "version": "0.1.0",
    }
