from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.users import router as users_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: APIRouter) -> AsyncGenerator[None]:
    """
    Set up and tear down application resources like the database engine.

    Args:
        app (APIRouter): An object of the APIRouter class.

    Yields:
        None:
    """

    # Set up the async database engine and session factory
    app.state.engine = create_async_engine(settings.DATABASE_URL, echo=False)
    app.state.async_session_maker = async_sessionmaker(app.state.engine)

    yield  # App is running

    # Clean up the database engine on shutdown
    await app.state.engine.dispose()


# Create the main application router and attach the lifespan handler
main_router = APIRouter(lifespan=lifespan)


@main_router.get("/ping", tags=["Test"])
async def ping() -> dict:
    """
    Health check endpoint.

    Returns:
        dict: Simple status message to indicate the service is running.
    """
    return {"status": "OK"}


# Include the user-related routes under the "User" tag
main_router.include_router(users_router, tags=["Users Profile"])
