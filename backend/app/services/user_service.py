from app.repositories.uow import UnitOfWork
from app.schemas.user_schema import UserProfileCreate, UserProfilePatch, UserProfileRead
from app.services.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


class UsersService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def add_user(self, user: UserProfileCreate) -> int:
        async with self.uow:
            user_exists = await self.uow.profiles.find(user.telegram_id)
            if user_exists:
                raise EntityAlreadyExistsException("User already exists")

            user_dict = user.model_dump()
            new_user = await self.uow.profiles.add_one(user_dict)

            return new_user.telegram_id

    async def find_all_users(self) -> list[UserProfileRead]:
        async with self.uow:
            users = await self.uow.profiles.find_all()
            res = [UserProfileRead.model_validate(user[0]) for user in users]
            return res

    async def find_user(self, user_id: int) -> UserProfileRead:
        async with self.uow:
            user = await self.uow.profiles.find(user_id)
            if user is None:
                raise EntityNotFoundException("User not found.")
            return UserProfileRead.model_validate(user)

    async def patch_user(self, user_id: int, user_update: UserProfilePatch) -> None:
        async with self.uow:
            user_update_dict = user_update.model_dump(exclude_defaults=True)
            user = await self.uow.profiles.find(user_id)
            if user is None:
                raise EntityNotFoundException("Пользователь не найден.")
            await self.uow.profiles.patch(user, user_update_dict)

    async def delete_user(self, user_id: int) -> None:
        async with self.uow:
            user = await self.uow.profiles.find(user_id)
            if user is None:
                raise EntityNotFoundException("User not found.")
            await self.uow.profiles.delete(user)

    async def delete_all(self) -> None:
        async with self.uow:
            await self.uow.profiles.delete_all()
            await self.session.commit()
