from fastapi import Depends, Request

from app.services.factories import ServiceFactory


async def get_session(request: Request):
    async_session_maker = request.app.state.async_session_maker
    async with async_session_maker() as session:
        yield session


async def get_service_factory(session=Depends(get_session)) -> ServiceFactory:
    return ServiceFactory(session)
