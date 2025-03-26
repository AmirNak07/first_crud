import uuid
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import RepositoryException
from app.models.user import UserProfileOrm


class AbstarctRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def find_all():
        raise NotImplementedError

    @abstractmethod
    async def find():
        raise NotImplementedError

    @abstractmethod
    async def patch():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError


class SQLAlchemyRepository(AbstarctRepository):
    model = None

    @classmethod
    async def add_one(cls, session: AsyncSession, data: Any):
        try:
            session.add(data)
        except IntegrityError as e:
            raise RepositoryException(
                "Data integrity error when adding a record."
            ) from e
        except SQLAlchemyError as e:
            raise RepositoryException("Database error when adding a record.") from e

    @classmethod
    async def find_all(cls, session: AsyncSession):
        stmt = select(cls.model)
        try:
            res = await session.execute(stmt)
            res = [row[0].to_read_model() for row in res.all()]
            return res
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when getting a list of records."
            ) from e

    @classmethod
    async def find(cls, session: AsyncSession, uuid: uuid.UUID):
        stmt = select(cls.model).where(cls.model.uuid == uuid)
        try:
            res = await session.execute(stmt)
            res = res.scalar_one_or_none()
            return res
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when searching for a record by UUID."
            ) from e

    @classmethod
    async def patch(
        cls, session: AsyncSession, user: UserProfileOrm, user_update: dict
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

    @classmethod
    async def delete(cls, session: AsyncSession, user: UserProfileOrm):
        try:
            await session.delete(user)
        except SQLAlchemyError as e:
            raise RepositoryException(
                "Database error when deleting a record by UUID."
            ) from e
