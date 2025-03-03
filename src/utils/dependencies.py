from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.users import UsersService


def users_service() -> UsersService:
    return UsersService(UsersRepository)


async def get_session():
    async with async_session_maker() as session:
        yield session
