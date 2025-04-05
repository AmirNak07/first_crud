import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.user import UserProfileAdd, UserProfilePatch
from app.services.user_service import UsersService
from app.utils.dependencies import users_service

router = APIRouter()


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserProfileAdd,
    user_service: Annotated[UsersService, Depends(users_service)],
):
    user_uuid = await user_service.add_user(user)
    return {"user_uuid": user_uuid}


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    user_service: Annotated[UsersService, Depends(users_service)],
):
    users = await user_service.find_all_users()
    return users


@router.get("/user/{uuid}", status_code=status.HTTP_200_OK)
async def get_user(
    uuid: uuid.UUID,
    user_service: Annotated[UsersService, Depends(users_service)],
):
    user = await user_service.find_user(uuid)
    return user


@router.patch("/user/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_user(
    user_uuid: uuid.UUID,
    user_update: UserProfilePatch,
    user_service: Annotated[UsersService, Depends(users_service)],
):
    await user_service.patch_user(user_uuid, user_update)
    return {"status": "ok"}


@router.delete("/user/{user_uuid}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_uuid: uuid.UUID,
    user_service: Annotated[UsersService, Depends(users_service)],
):
    await user_service.delete_user(user_uuid)
    return {"status": "ok"}
