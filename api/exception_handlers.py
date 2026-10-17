from fastapi import FastAPI
from fastapi.responses import JSONResponse

from application.exceptions.not_found import ResourceNotFoundError


def register_exception_handlers(
    app: FastAPI,
) -> None:
    @app.exception_handler(ResourceNotFoundError)
    async def resource_not_found_handler(
        request,
        exc: ResourceNotFoundError,
    ):
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc),
            },
        )
