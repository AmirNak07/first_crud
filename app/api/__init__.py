from contextlib import asynccontextmanager

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.users import router as users_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: APIRouter):
    app.state.engine = create_async_engine(settings.DATABASE_URL, echo=False)
    app.state.async_session_maker = async_sessionmaker(app.state.engine)
    yield
    await app.state.engine.dispose()


main_router = APIRouter(lifespan=lifespan)
main_router.include_router(users_router, tags=["User"])


@main_router.get("/ping", tags=["Test"])
async def ping():
    return {"status": "OK"}
