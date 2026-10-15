from fastapi import FastAPI

from api.exception_handlers import (
    register_exception_handlers,
)

from api.routes import (
    alerts_router,
    cases_router,
    events_router,
)

app = FastAPI(
    title="SOC Platform",
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(cases_router)


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