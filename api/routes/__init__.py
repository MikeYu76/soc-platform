from api.routes.alerts import router as alerts_router
from api.routes.auth import router as auth_router
from api.routes.cases import router as cases_router
from api.routes.events import router as events_router

__all__ = [
    "alerts_router",
    "auth_router",
    "cases_router",
    "events_router",
]
