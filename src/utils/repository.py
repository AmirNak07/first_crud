from abc import ABC, abstractmethod

from sqlalchemy import insert, select

from src.database import async_session_maker


class AbstarctRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstarctRepository):
    model = None

    @classmethod
    async def add_one(cls, data: dict):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model.uuid)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            stmt = select(cls.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res
