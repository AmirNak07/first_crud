from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import UserPreferencesCreate, UserPreferencesRead
from app.services.factories import ServiceFactory
from app.utils.dependencies import get_service_factory

router = APIRouter()


@router.post("/{telegram_id}/preferences", status_code=status.HTTP_201_CREATED)
async def create_preferences(
    telegram_id: int,
    preferences: UserPreferencesCreate,
    service_factory: ServiceFactory = Depends(get_service_factory),
):
    preferences_data = UserPreferencesRead(
        telegram_id=telegram_id, **preferences.model_dump()
    )
    user_service = service_factory.get_preferences_services()
    telegram_id = await user_service.add_preference(
        telegram_id=telegram_id, preference=preferences_data
    )
    return {"telegram_id": telegram_id}
