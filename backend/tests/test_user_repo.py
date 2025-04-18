import pytest
from app.models.user_model import UserProfileOrm
from app.repositories.user_repository import UserProfileRepository
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
async def repo(async_test_session: AsyncSession) -> UserProfileRepository:
    return UserProfileRepository(async_test_session)


@pytest.fixture
async def new_user(
    async_test_session: AsyncSession, repo: UserProfileRepository
) -> UserProfileOrm:
    user = {
        "name": "Адам",
        "about_me": "Первый человек",
        "age": 99,
        "city": "Эдем",
        "sex": "Мужской",
    }

    new_user = await repo.add_one(user)
    await async_test_session.flush()
    return new_user


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.usefixtures("clear_db")
class TestUserProfileRepository:
    async def test_add_one_success(
        self,
        new_user: UserProfileOrm,
    ) -> None:
        assert new_user.name == "Адам"
        assert new_user.about_me == "Первый человек"
        assert new_user.age == 99
        assert new_user.city == "Эдем"
        assert new_user.sex == "Мужской"

    async def test_find_all(self, repo: UserProfileRepository) -> None:
        users = [
            {
                "name": "Адам",
                "about_me": "Первый человек",
                "age": 99,
                "city": "Эдем",
                "sex": "Мужской",
            },
            {
                "name": "Ева",
                "about_me": "Человек из ребра Адама",
                "age": 98,
                "city": "Эдем",
                "sex": "Женский",
            },
        ]

        for user in users:
            await repo.add_one(user)

        res = await repo.find_all()
        assert res[0][0].name == "Адам"
        assert res[0][0].about_me == "Первый человек"
        assert res[0][0].age == 99
        assert res[0][0].city == "Эдем"
        assert res[0][0].sex == "Мужской"

        assert res[1][0].name == "Ева"
        assert res[1][0].about_me == "Человек из ребра Адама"
        assert res[1][0].age == 98
        assert res[1][0].city == "Эдем"
        assert res[1][0].sex == "Женский"

    async def test_find_success(
        self,
        repo: UserProfileRepository,
        new_user: UserProfileOrm,
    ) -> None:
        telegram_id = new_user.telegram_id

        res = await repo.find(telegram_id)
        assert res.name == "Адам"
        assert res.about_me == "Первый человек"
        assert res.age == 99
        assert res.city == "Эдем"
        assert res.sex == "Мужской"

    async def test_find_not_found(self, repo: UserProfileRepository) -> None:
        user = await repo.find(0)
        assert user is None

    async def test_patch_success(
        self,
        repo: UserProfileRepository,
        new_user: UserProfileOrm,
    ) -> None:
        telegram_id = new_user.telegram_id

        user = await repo.find(telegram_id)
        new_data = {"name": "Новый юзер"}
        await repo.patch(user, new_data)

        assert user.name == "Новый юзер"

    async def test_delete_success(
        self,
        async_test_session: AsyncSession,
        repo: UserProfileRepository,
        new_user: UserProfileOrm,
    ) -> None:
        await repo.delete(new_user)
        await async_test_session.flush()
        assert inspect(new_user).deleted is True
