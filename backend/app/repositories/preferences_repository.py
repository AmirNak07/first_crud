from app.models.user_model import UserPreferenceOrm
from app.repositories.base_repository import SQLAlchemyRepository


class UserPreferenceRepository(SQLAlchemyRepository[UserPreferenceOrm]):
    model = UserPreferenceOrm
