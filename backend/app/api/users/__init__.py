from fastapi import APIRouter

from app.api.users.user_preferences import router as preferences_router
from app.api.users.user_profile import router as profile_router

users_router = APIRouter()

users_router.include_router(profile_router, tags=["User Profile"])
users_router.include_router(preferences_router, tags=["User Preference"])
