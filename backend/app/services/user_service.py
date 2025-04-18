from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import RepositoryError
from app.repositories.user_repository import UserProfileRepository
from app.schemas.user_schema import UserProfileCreate, UserProfilePatch, UserProfileRead
from app.services.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


class UsersService:
    def __init__(
        self, session: AsyncSession, tasks_repo: UserProfileRepository
    ) -> None:
        self.session: AsyncSession = session
        self.tasks_repo: UserProfileRepository = tasks_repo

    async def add_user(self, user: UserProfileCreate) -> int:
        try:
            user_exists = await self.tasks_repo.find(user.telegram_id)
            if user_exists:
                raise EntityAlreadyExistsException("User already exists")
            user_dict = user.model_dump()
            new_user = await self.tasks_repo.add_one(user_dict)
            await self.session.flush()
            id = new_user.telegram_id
            await self.session.commit()
            return id
        except RepositoryError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError("Database error occurred during add_user") from e

    async def find_all_users(self) -> list[UserProfileRead]:
        try:
            users = await self.tasks_repo.find_all()
            res = [UserProfileRead.model_validate(user[0]) for user in users]
            return res
        except RepositoryError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError(
                "Database error occurred during find_all_users"
            ) from e

    async def find_user(self, user_id: int) -> UserProfileRead:
        try:
            user = await self.tasks_repo.find(user_id)
            if user is None:
                await self.session.rollback()
                raise EntityNotFoundException("User not found.")
            return UserProfileRead.model_validate(user)
        except RepositoryError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError("Database error occurred during find_user") from e

    async def patch_user(self, user_id: int, user_update: UserProfilePatch) -> None:
        try:
            user_update_dict = user_update.model_dump(exclude_defaults=True)
            user = await self.tasks_repo.find(user_id)
            if user is None:
                raise EntityNotFoundException("Пользователь не найден.")
            await self.tasks_repo.patch(user, user_update_dict)
            await self.session.commit()
        except RepositoryError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError("Database error occurred during patch_user") from e

    async def delete_user(self, user_id: int) -> None:
        try:
            user = await self.tasks_repo.find(user_id)
            if user is None:
                raise EntityNotFoundException("User not found.")
            await self.tasks_repo.delete(user)
            await self.session.commit()
        except RepositoryError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError("Database error occurred during delete_user") from e

    async def delete_all(self) -> None:
        try:
            await self.tasks_repo.delete_all()
            await self.session.commit()
        except RepositoryError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryError("Database error occurred during delete_all") from e
