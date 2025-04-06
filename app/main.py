from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api import main_router
from app.core.exceptions import RepositoryError
from app.services.exceptions import EntityNotFoundException

app = FastAPI(title="My Tinder")
app.include_router(main_router)


@app.exception_handler(EntityNotFoundException)
async def entity_not_found_exception_handler(
    request: Request, exc: EntityNotFoundException
):
    """
    Handles EntityNotFoundException and returns a 404 response.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(RepositoryError)
async def repository_error_exception_handler(request: Request, exc: RepositoryError):
    """
    Handles RepositoryError and returns a 500 response.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error"},
            )


app.add_middleware(ErrorHandlingMiddleware)
