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

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> T:
        try:
            instance = self.model(**data)
            self.session.add(instance)
            return instance
        except SQLAlchemyError as e:
            raise RecursionError("Database error when adding a record.") from e

    async def find_all(self) -> list[T]:
        try:
            stmt = select(self.model)
            res = await self.session.execute(stmt)
            return res.all()
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when getting a list of records."
            ) from e

    async def find(self, id: int) -> T:
        try:
            stmt = select(self.model).where(self.model.telegram_id == id)
            res = await self.session.execute(stmt)
            res = res.scalar_one_or_none()
            return res
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when searching for a record by Telegram id."
            ) from e

    async def patch(self, user: T, user_update: dict) -> None:
        try:
            for field, value in user_update.items():
                setattr(user, field, value)
            await self.session.flush()
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when changing a record by Telegram id."
            ) from e

    async def delete(self, user: T) -> None:
        try:
            await self.session.delete(user)
        except SQLAlchemyError as e:
            raise RepositoryError(
                "Database error when deleting a record by Telegram id."
            ) from e

    async def delete_all(self) -> None:
        try:
            stmt = delete(self.model)
            await self.session.execute(stmt)
        except SQLAlchemyError as e:
            raise RepositoryError("Database error when deleting all records") from e
        except Exception:
            raise

# Add normal type hints
