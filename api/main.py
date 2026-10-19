from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.exception_handlers import register_exception_handlers
from api.routes import alerts_router, auth_router, cases_router, events_router
from application.composition.authentication import ensure_bootstrap_administrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not getattr(app.state, "testing", False):
        ensure_bootstrap_administrator()
    yield


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
