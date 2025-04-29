from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import UserProfileCreate, UserProfilePatch, UserProfileRead
from app.services.factories import ServiceFactory
from app.utils.dependencies import get_service_factory
from app.utils.security import verify_jwt_token

router = APIRouter(dependencies=[Depends(verify_jwt_token)])


@router.post("/profiles", status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    user: UserProfileCreate,
    service_factory: ServiceFactory = Depends(get_service_factory),
) -> dict:
    """
    Create a new user profile.

    Args:
        user (UserProfileCreate): Data for creating the user.
        service_factory (ServiceFactory): Factory for creating services for handling user logic.

    Returns:
        dict: Telegram id of the created user.
    """
    user_service = service_factory.get_profiles_services()
    telegram_id = await user_service.add_user(user)
    return {"telegram_id": telegram_id}


@router.get("/profiles", status_code=status.HTTP_200_OK)
async def get_user_profiles(
    service_factory: ServiceFactory = Depends(get_service_factory),
) -> list[UserProfileRead]:
    """
    Get a list of all users.

    Args:
        service_factory (ServiceFactory): Factory for creating services for handling user logic.

    Returns:
        list[UserProfileRead]: List of user profiles.
    """
    user_service = service_factory.get_profiles_services()
    users = await user_service.find_all_users()
    return users


@router.get("/{telegram_id}/profiles", status_code=status.HTTP_200_OK)
async def get_user_profile(
    telegram_id: int,
    service_factory: ServiceFactory = Depends(get_service_factory),
) -> UserProfileRead:
    """
    Get a single user by Telegram id.

    Args:
        telegram_id (int): Unique identifier of the user.
        service_factory (ServiceFactory): Factory for creating services for handling user logic.

    Returns:
        UserProfileRead: User profile.
    """
    user_service = service_factory.get_profiles_services()
    user = await user_service.find_user(telegram_id)
    return user


@router.patch("/{telegram_id}/profiles", status_code=status.HTTP_200_OK)
async def update_user_profile(
    telegram_id: int,
    user_update: UserProfilePatch,
    service_factory: ServiceFactory = Depends(get_service_factory),
) -> dict:
    """
    Update an existing user profile.

    Args:
        telegram_id (int): Unique identifier of the user.
        user_update (UserProfilePatch): Fields to update.
        service_factory (ServiceFactory): Factory for creating services for handling user logic.

    Returns:
        dict: Status message.
    """
    user_service = service_factory.get_profiles_services()
    await user_service.patch_user(telegram_id, user_update)
    return {"status": "ok"}


@router.delete("/{telegram_id}/profiles", status_code=status.HTTP_200_OK)
async def delete_user_profile(
    telegram_id: int,
    service_factory: ServiceFactory = Depends(get_service_factory),
) -> dict:
    """
    Delete a user by Telegram id.

    Args:
        telegram_id (int): Unique identifier of the user.
        service_factory (ServiceFactory): Factory for creating services for handling user logic.

    Returns:
        dict: Status message.
    """
    user_service = service_factory.get_profiles_services()
    await user_service.delete_user(telegram_id)
    return {"status": "ok"}
