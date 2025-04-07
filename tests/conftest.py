import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.database import Base
from app.models.user_model import UserProfileOrm  # noqa: F401

TEST_DATABASE_URL = settings.DATABASE_URL
pytest_plugins = ("pytest_asyncio",)


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    print(TEST_DATABASE_URL)
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_test_session(async_engine: AsyncEngine):
    async_session = async_sessionmaker(async_engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
        await session.commit()


@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown_db(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def clear_db(repo: Base) -> None:
    await repo.delete_all()


@pytest.fixture(scope="session", autouse=True)
async def test_env() -> None:
    assert settings.MODE == "TEST"
