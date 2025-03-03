from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.users import UserProfileAdd
from src.services.users import UsersService
from src.utils.dependencies import users_service

router = APIRouter()


@router.post("/create_user")
async def create_user(
    user: UserProfileAdd, user_service: Annotated[UsersService, Depends(users_service)]
):
    user_uuid = await user_service.add_user(user)
    return {"user_uuid": user_uuid}
