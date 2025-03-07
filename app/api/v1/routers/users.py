import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserProfileAdd, UserProfilePatch
from app.services.exceptions import (
    BusinessValidationError,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from app.services.user_service import UsersService
from app.utils.dependencies import get_session, users_service

router = APIRouter()


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserProfileAdd,
    user_service: Annotated[UsersService, Depends(users_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        user_uuid = await user_service.add_user(user, session)
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
async def get_users(
    user_service: Annotated[UsersService, Depends(users_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        users = await user_service.find_all_users(session)
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
    uuid: uuid.UUID,
    user_service: Annotated[UsersService, Depends(users_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        user = await user_service.find_user(uuid, session)
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
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        await user_service.patch_user(user_uuid, user_update, session)
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
    user_uuid: uuid.UUID,
    user_service: Annotated[UsersService, Depends(users_service)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        deleted_user = await user_service.delete_user(user_uuid, session)
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
