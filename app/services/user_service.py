from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base_repository import AbstarctRepository
from app.schemas.user import UserProfile, UserProfileAdd, UserProfilePatch
from app.services.exceptions import (
    BusinessValidationError,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


class UsersService:
    def __init__(self, tasks_repo: AbstarctRepository):
        self.tasks_repo: AbstarctRepository = tasks_repo()

    async def add_user(self, user: UserProfileAdd, session: AsyncSession):
        user_dict = user.model_dump()
        try:
            user_uuid = await self.tasks_repo.add_one(session, user_dict)
            await session.commit()
            return user_uuid
        except Exception as e:
            await session.rollback()
            raise EntityAlreadyExistsException(
                "The user with this ID already exists."
            ) from e

    async def find_all_users(self, session: AsyncSession) -> list[UserProfile]:
        try:
            users = await self.tasks_repo.find_all(session)
            return users
        except Exception as e:
            raise BusinessValidationError(
                "An error occurred while retrieving the list of users details."
            ) from e

    async def find_user(self, user_uuid: UUID, session: AsyncSession):
        try:
            user = await self.tasks_repo.find(session, user_uuid)
            if user is None:
                raise EntityNotFoundException("User not found.")
            return user
        except EntityNotFoundException:
            raise
        except Exception as e:
            raise BusinessValidationError(
                "An error occurred while retrieving the user details."
            ) from e

    async def patch_user(
        self, user_uuid: UUID, user_update: UserProfilePatch, session: AsyncSession
    ):
        user_update_dict = user_update.model_dump(exclude_defaults=True)
        try:
            user = await self.tasks_repo.find(session, user_uuid)
            if user is None:
                raise EntityNotFoundException("Пользователь не найден.")
            await self.tasks_repo.patch(session, user_uuid, user_update_dict)
            await session.commit()
        except EntityNotFoundException:
            raise
        except Exception as e:
            await session.rollback()
            raise BusinessValidationError(
                "An error occurred while patching the user details."
            ) from e

    async def delete_user(self, user_uuid: UUID, session: AsyncSession):
        try:
            user = await self.tasks_repo.find(session, user_uuid)
            if user is None:
                raise EntityNotFoundException("User not found.")
            res = await self.tasks_repo.delete(session, user_uuid)
            await session.commit()
            if res == 1:
                return True
            return False
        except EntityNotFoundException:
            raise
        except Exception as e:
            await session.rollback()
            raise BusinessValidationError(
                "An error occurred while deleting the user details."
            ) from e
