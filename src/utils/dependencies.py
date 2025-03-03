from fastapi import Request

from src.repositories.users import UsersRepository
from src.services.users import UsersService


def users_service() -> UsersService:
    return UsersService(UsersRepository)


async def get_session(request: Request):
    async_session_maker = request.app.state.async_session_maker
    async with async_session_maker() as session:
        yield session
