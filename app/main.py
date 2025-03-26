from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api.v1.routers.users import router as user_router
from app.core.config import settings


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
