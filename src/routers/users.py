import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.users import UserProfileAdd, UserProfilePatch
from src.services.exceptions import (
    BusinessValidationError,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from src.services.users import UsersService
from src.utils.dependencies import users_service

router = APIRouter()


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserProfileAdd, user_service: Annotated[UsersService, Depends(users_service)]
):
    try:
        user_uuid = await user_service.add_user(user)
        return {"user_uuid": user_uuid}
    except EntityAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        ) from None
    except BusinessValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Validation error."
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(user_service: Annotated[UsersService, Depends(users_service)]):
    try:
        users = await user_service.find_all_users()
        return users
    except BusinessValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.get("/user/{uuid}", status_code=status.HTTP_200_OK)
async def get_user(
    uuid: uuid.UUID, user_service: Annotated[UsersService, Depends(users_service)]
):
    try:
        user = await user_service.find_user(uuid)
        return user
    except EntityNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        ) from None
    except BusinessValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.patch("/user/{user_uuid}", status_code=status.HTTP_200_OK)
async def update_user(
    user_uuid: uuid.UUID,
    user_update: UserProfilePatch,
    user_service: Annotated[UsersService, Depends(users_service)],
):
    try:
        await user_service.patch_user(user_uuid, user_update)
        return {"status": "ok"}
    except EntityNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        ) from None
    except BusinessValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None


@router.delete("/user/{user_uuid}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_uuid: uuid.UUID, user_service: Annotated[UsersService, Depends(users_service)]
):
    try:
        deleted_user = await user_service.delte_user(user_uuid)
        if deleted_user:
            return {"status": "ok"}
    except EntityNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        ) from None
    except BusinessValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from None
