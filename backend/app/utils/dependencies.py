from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserProfileRepository
from app.services.user_service import UsersService


async def get_session(request: Request):
    async_session_maker = request.app.state.async_session_maker
    async with async_session_maker() as session:
        yield session


async def users_service(session: AsyncSession = Depends(get_session)) -> UsersService:
    return UsersService(session, UserProfileRepository(session))
