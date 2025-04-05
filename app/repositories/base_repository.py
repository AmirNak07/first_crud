import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.core.exceptions import RepositoryError

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find(self):
        raise NotImplementedError

    @abstractmethod
    async def patch(self):
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository, Generic[T]):
    model: type[T] = None

    async def add_one(self, session: AsyncSession, data: dict) -> T:
        try:
            instance = self.model(**data)
            session.add(instance)
            return instance
        except SQLAlchemyError as e:
            raise RecursionError("Database error when adding a record.") from e

    async def find_all(self, session: AsyncSession) -> list[T]:
        try:
            stmt = select(self.model)
            res = await session.execute(stmt)
            return res.all()
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when getting a list of records."
            ) from e

    async def find(self, session: AsyncSession, uuid: uuid.UUID) -> T:
        try:
            stmt = select(self.model).where(self.model.uuid == uuid)
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            return res
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when searching for a record by UUID."
            ) from e

    async def patch(self, session: AsyncSession, user: T, user_update: dict) -> None:
        try:
            for field, value in user_update.items():
                setattr(user, field, value)
            await session.flush()
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when changing a record by UUID."
            ) from e

    async def delete(self, session: AsyncSession, user: T) -> None:
        try:
            await session.delete(user)
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when deleting a record by UUID."
            ) from e

    async def delete_all(self, session: AsyncSession) -> None:
        try:
            stmt = delete(self.model)
            await session.execute(stmt)
        except SQLAlchemyError as e:
            raise RepositoryError("Database error when deleting all records") from e
        except Exception:
            raise
