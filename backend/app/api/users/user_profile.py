from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import UserProfileCreate, UserProfilePatch, UserProfileRead
from app.services.user_service import UsersService
from app.utils.dependencies import users_service
from app.utils.security import verify_hmac_signature

router = APIRouter(dependencies=[Depends(verify_hmac_signature)])


@router.post("/profiles", status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    user: UserProfileCreate,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> dict:
    """
    Create a new user profile.

    Args:
        user (UserProfileCreate): Data for creating the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        dict: Telegram id of the created user.
    """
    telegram_id = await user_service.add_user(user)
    return {"telegram_id": telegram_id}


@router.get("/profiles", status_code=status.HTTP_200_OK)
async def get_user_profiles(
    user_service: Annotated[UsersService, Depends(users_service)],
) -> list[UserProfileRead]:
    """
    Get a list of all users.

    Args:
        user_service (UsersService): Service for handling user logic.

    Returns:
        list[UserProfileRead]: List of user profiles.
    """
    users = await user_service.find_all_users()
    return users


@router.get("/{telegram_id}/profiles", status_code=status.HTTP_200_OK)
async def get_user_profile(
    telegram_id: int,
    user_service: Annotated[UsersService, Depends(users_service)],
) -> UserProfileRead:
    """
    Get a single user by Telegram id.

    Args:
        telegram_id (int): Unique identifier of the user.
        user_service (UsersService): Service for handling user logic.

    Returns:
        UserProfileRead: User profile.
    """
    user = await user_service.find_user(telegram_id)
    return user


@router.patch("/{telegram_id}/profiles", status_code=status.HTTP_200_OK)
async def update_user_profile(
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


@router.delete("/{telegram_id}/profiles", status_code=status.HTTP_200_OK)
async def delete_user_profile(
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
