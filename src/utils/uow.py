from contextlib import asynccontextmanager

from src.database import async_session_maker


class UnitOfWork:
    def __init__(self):
        self.session = async_session_maker()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def aclose(self):
        await self.session.aclose()


@asynccontextmanager
async def unit_of_work():
    uow = UnitOfWork()
    try:
        yield uow
        await uow.commit()
    except Exception:
        await uow.rollback()
        raise
    finally:
        await uow.aclose()
