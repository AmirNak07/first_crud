from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UsersRepository
from app.schemas.user import UserProfile, UserProfileAdd, UserProfilePatch
from app.services.exceptions import (
    BusinessValidationError,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


class UsersService:
    def __init__(self, session: AsyncSession, tasks_repo: UsersRepository) -> None:
        self.tasks_repo: UsersRepository = tasks_repo()
        self.session: AsyncSession = session

    async def add_user(self, user: UserProfileAdd) -> UUID:
        user_dict = user.model_dump()
        try:
            new_user = await self.tasks_repo.add_one(self.session, user_dict)
            await self.session.flush()
            uuid = new_user.uuid
            await self.session.commit()
            return uuid
        except Exception as e:
            await self.session.rollback()
            raise EntityAlreadyExistsException(
                "The user with this ID already exists."
            ) from e

    async def find_all_users(self) -> list[UserProfile]:
        try:
            users = await self.tasks_repo.find_all(self.session)
            res = [UserProfile.model_validate(user[0]) for user in users]
            return res
        except Exception as e:
            raise BusinessValidationError(
                "An error occurred while retrieving the list of users details."
            ) from e

    async def find_user(self, user_uuid: UUID) -> UserProfile:
        try:
            user = await self.tasks_repo.find(self.session, user_uuid)
            if user is None:
                raise EntityNotFoundException("User not found.")
            return UserProfile.model_validate(user)
        except EntityNotFoundException:
            raise
        except Exception as e:
            raise BusinessValidationError(
                "An error occurred while retrieving the user details."
            ) from e

    async def patch_user(self, user_uuid: UUID, user_update: UserProfilePatch) -> None:
        user_update_dict = user_update.model_dump(exclude_defaults=True)
        try:
            user = await self.tasks_repo.find(self.session, user_uuid)
            if user is None:
                raise EntityNotFoundException("Пользователь не найден.")
            await self.tasks_repo.patch(self.session, user, user_update_dict)
            await self.session.commit()
        except EntityNotFoundException:
            await self.session.rollback()
            raise
        except Exception as e:
            await self.session.rollback()
            raise BusinessValidationError(
                "An error occurred while patching the user details."
            ) from e

    async def delete_user(self, user_uuid: UUID) -> None:
        try:
            user = await self.tasks_repo.find(self.session, user_uuid)
            if user is None:
                raise EntityNotFoundException("User not found.")
            await self.tasks_repo.delete(self.session, user)
            await self.session.commit()
        except EntityNotFoundException:
            raise
        except Exception as e:
            await self.session.rollback()
            raise BusinessValidationError(
                "An error occurred while deleting the user details."
            ) from e

    async def delete_all(self) -> None:
        try:
            await self.tasks_repo.delete_all(self.session)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
