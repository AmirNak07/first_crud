from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api import main_router
from app.core.exceptions import RepositoryError
from app.services.exceptions import EntityNotFoundException
from app.utils.middlewares import ErrorHandlingMiddleware

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


app.add_middleware(ErrorHandlingMiddleware)
