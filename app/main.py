from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.v1.routers.users import router as user_router
from app.core.config import settings
from app.core.exceptions import RepositoryError
from app.services.exceptions import EntityNotFoundException


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.engine = create_async_engine(settings.DATABASE_URL, echo=False)
    app.state.async_session_maker = async_sessionmaker(app.state.engine)
    yield
    await app.state.engine.dispose()


app = FastAPI(lifespan=lifespan, title="My Tinder")


@app.get("/ping", tags=["Test"])
async def ping():
    return {"status": "OK"}


app.include_router(user_router, tags=["User"])


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
