from src.models.users import UserProfileOrm
from src.utils.repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UserProfileOrm
