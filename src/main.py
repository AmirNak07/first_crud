from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import Settings
from src.routers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = Settings.get_settings()
    app.state.engine = create_async_engine(app.state.settings.DATABASE_URL)
    app.state.async_session_maker = async_sessionmaker(
        app.state.engine, expire_on_commit=False
    )
    yield
    await app.state.engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def ping():
    return {"status": "OK"}


app.include_router(user_router)
