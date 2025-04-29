from app.repositories.uow import UnitOfWork
from app.schemas.user_schema import UserPreferencesCreate
from app.services.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)


class UserPreferencesService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def add_preference(self, telegram_id: int, preference: UserPreferencesCreate):
        async with self.uow:
            user_exists = await self.uow.profiles.find(telegram_id)
            if user_exists is None:
                raise EntityNotFoundException("User not found.")

            preference_exists = await self.uow.preferences.find(telegram_id)
            if preference_exists:
                raise EntityAlreadyExistsException("Preference already exists.")

            preference_dict = preference.model_dump()
            new_preference = await self.uow.preferences.add_one(preference_dict)

            return new_preference.telegram_id
