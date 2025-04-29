from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.uow import UnitOfWork
from app.services.user_service import UsersService


class ServiceFactory:
    def __init__(self, session: AsyncSession):
        self.uow = UnitOfWork(session)

    def get_profiles_services(self):
        return UsersService(uow=self.uow)
