from src.schemas.users import UserProfileAdd
from src.utils.repository import AbstarctRepository


class UsersService:
    def __init__(self, tasks_repo: AbstarctRepository):
        self.tasks_repo: AbstarctRepository = tasks_repo()

    async def add_user(self, user: UserProfileAdd):
        user_dict = user.model_dump()
        user_uuid = await self.tasks_repo.add_one(user_dict)
        return user_uuid
