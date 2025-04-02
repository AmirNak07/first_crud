import uuid
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import RepositoryException
from app.models.user import UserProfileOrm


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


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add_one(self, session: AsyncSession, data: Any):
        try:
            session.add(data)
        except IntegrityError as e:
            raise RepositoryException(
                "Data integrity error when adding a record."
            ) from e
        except SQLAlchemyError as e:
            raise RepositoryException("Database error when adding a record.") from e

    async def find_all(self, session: AsyncSession):
        stmt = select(self.model)
        try:
            res = await session.execute(stmt)
            return res.all()
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when getting a list of records."
            ) from e

    async def find(self, session: AsyncSession, uuid: uuid.UUID):
        stmt = select(self.model).where(self.model.uuid == uuid)
        try:
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            return res
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when searching for a record by UUID."
            ) from e

    async def patch(
        self, session: AsyncSession, user: UserProfileOrm, user_update: dict
    ):
        try:
            for field, value in user_update.items():
                setattr(user, field, value)
            await session.flush()
            return user
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when changing a record by UUID."
            ) from e

    async def delete(self, session: AsyncSession, user: UserProfileOrm):
        try:
            await session.delete(user)
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when deleting a record by UUID."
            ) from e

    async def delete_all(self, session: AsyncSession):
        try:
            stmt = delete(self.model)
            await session.execute(stmt)
        except SQLAlchemyError as e:
            raise RepositoryException("Database error when deleting all records") from e
        except Exception:
            raise
