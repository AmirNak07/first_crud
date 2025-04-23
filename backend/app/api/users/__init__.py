from fastapi import APIRouter

from app.api.users.user_profile import router as profile_router

users_router = APIRouter()

users_router.include_router(profile_router, tags=["User Profile"])
