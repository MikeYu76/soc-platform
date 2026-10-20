from api.routes.alerts import router as alerts_router
from api.routes.auth import router as auth_router
from api.routes.cases import router as cases_router
from api.routes.events import router as events_router
from api.routes.operations import router as operations_router

__all__ = [
    "alerts_router",
    "auth_router",
    "cases_router",
    "events_router",
    "operations_router",
]
