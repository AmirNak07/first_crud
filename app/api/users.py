from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import UserProfile, UserProfileAdd, UserProfilePatch
from app.services.user_service import UsersService
from app.utils.dependencies import users_service
from app.utils.security import verify_hmac_signature

router = APIRouter(dependencies=[Depends(verify_hmac_signature)])


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
        dict: Telegram id of the created user.
    """
    telegram_id = await user_service.add_user(user)
    return {"telegram_id": telegram_id}


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


@router.get("/users/{telegram_id}", status_code=status.HTTP_200_OK)
async def get_user(
    telegram_id: int,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> UserProfile:
    """
    Get a single user by Telegram id.

    Args:
        telegram_id (int): Unique identifier of the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        UserProfile: User profile.
    """
    user = await user_service.find_user(telegram_id)
    return user


@router.patch("/users/{telegram_id}", status_code=status.HTTP_200_OK)
async def update_user(
    telegram_id: int,
    user_update: UserProfilePatch,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> dict:
    """
    Update an existing user profile.

    Args:
        telegram_id (int): Unique identifier of the user.
        user_update (UserProfilePatch): Fields to update.
        user_service (UsersService): Service for handling user logic.

    Returns:
        dict: Status message.
    """
    await user_service.patch_user(telegram_id, user_update)
    return {"status": "ok"}


@router.delete("/users/{telegram_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    telegram_id: int,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> dict:
    """
    Delete a user by Telegram id.

    Args:
        telegram_id (int): Unique identifier of the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        dict: Status message.
    """
    await user_service.delete_user(telegram_id)
    return {"status": "ok"}
