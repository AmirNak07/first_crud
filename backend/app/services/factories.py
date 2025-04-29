from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.uow import UnitOfWork
from app.services.preferences_service import UserPreferencesService
from app.services.profile_service import UserProfilesService


class ServiceFactory:
    def __init__(self, session: AsyncSession):
        self.uow = UnitOfWork(session)

    def get_profiles_services(self):
        return UserProfilesService(uow=self.uow)

    def get_preferences_services(self):
        return UserPreferencesService(uow=self.uow)
