from app.models.user import UserProfileOrm
from app.repositories.base_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UserProfileOrm
