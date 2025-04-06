from app.models.user_model import UserProfileOrm
from app.repositories.base_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository[UserProfileOrm]):
    model = UserProfileOrm
