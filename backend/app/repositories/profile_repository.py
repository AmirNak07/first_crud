from app.models.user_model import UserProfileOrm
from app.repositories.base_repository import SQLAlchemyRepository


class UserProfileRepository(SQLAlchemyRepository[UserProfileOrm]):
    model = UserProfileOrm
