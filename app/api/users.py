import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import UserProfile, UserProfileAdd, UserProfilePatch
from app.services.user_service import UsersService
from app.utils.dependencies import users_service

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserProfileAdd,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> dict:
    """
    Create a new user profile.

    Args:
        user (UserProfileAdd): Data for creating the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        dict: UUID of the created user.
    """
    user_uuid = await user_service.add_user(user)
    return {"user_uuid": user_uuid}


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    user_service: Annotated[UsersService, Depends(users_service)],
) -> list[UserProfile]:
    """
    Get a list of all users.

    Args:
        user_service (UsersService): Service for handling user logic.

    Returns:
        list[UserProfile]: List of user profiles.
    """
    users = await user_service.find_all_users()
    return users


@router.get("/users/{uuid}", status_code=status.HTTP_200_OK)
async def get_user(
    uuid: uuid.UUID,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> UserProfile:
    """
    Get a single user by UUID.

    Args:
        uuid (UUID): Unique identifier of the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        UserProfile: User profile.
    """
    user = await user_service.find_user(uuid)
    return user


@router.patch("/users/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_user(
    user_uuid: uuid.UUID,
    user_update: UserProfilePatch,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> dict:
    """
    Update an existing user profile.

    Args:
        user_uuid (UUID): Unique identifier of the user.
        user_update (UserProfilePatch): Fields to update.
        user_service (UsersService): Service for handling user logic.

    Returns:
        dict: Status message.
    """
    await user_service.patch_user(user_uuid, user_update)
    return {"status": "ok"}


@router.delete("/users/{user_uuid}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_uuid: uuid.UUID,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> dict:
    """
    Delete a user by UUID.

    Args:
        user_uuid (UUID): Unique identifier of the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        dict: Status message.
    """
    await user_service.delete_user(user_uuid)
    return {"status": "ok"}
