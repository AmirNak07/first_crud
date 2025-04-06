from uuid import uuid4

import pytest
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_model import UserProfileOrm
from app.repositories.user_repository import UsersRepository


@pytest.fixture
async def repo() -> UsersRepository:
    return UsersRepository()


@pytest.fixture
async def clear_db(async_test_session: AsyncSession, repo: UsersRepository) -> None:
    await repo.delete_all(async_test_session)


@pytest.fixture
async def new_user(
    async_test_session: AsyncSession, repo: UsersRepository
) -> UserProfileOrm:
    user = {
        "name": "Адам",
        "about_me": "Первый человек",
        "age": 99,
        "city": "Эдем",
        "sex": "Мужской",
    }

    new_user = await repo.add_one(async_test_session, user)
    await async_test_session.flush()
    return new_user


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.usefixtures("clear_db")
class TestUsersRepository:
    async def test_add_one_success(
        self,
        new_user: UserProfileOrm,
    ) -> None:
        assert new_user.name == "Адам"
        assert new_user.about_me == "Первый человек"
        assert new_user.age == 99
        assert new_user.city == "Эдем"
        assert new_user.sex == "Мужской"

    async def test_find_all(
        self, async_test_session: AsyncSession, repo: UsersRepository
    ) -> None:
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
            await repo.add_one(async_test_session, user)

        res = await repo.find_all(async_test_session)
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
        async_test_session: AsyncSession,
        repo: UsersRepository,
        new_user: UserProfileOrm,
    ) -> None:
        uuid = new_user.uuid

        res = await repo.find(async_test_session, uuid)
        assert res.name == "Адам"
        assert res.about_me == "Первый человек"
        assert res.age == 99
        assert res.city == "Эдем"
        assert res.sex == "Мужской"

    async def test_find_not_found(
        self, async_test_session: AsyncSession, repo: UsersRepository
    ) -> None:
        user = await repo.find(async_test_session, uuid4())
        assert user is None

    async def test_patch_success(
        self,
        async_test_session: AsyncSession,
        repo: UsersRepository,
        new_user: UserProfileOrm,
    ) -> None:
        uuid = new_user.uuid

        user = await repo.find(async_test_session, uuid)
        new_data = {"name": "Новый юзер"}
        await repo.patch(async_test_session, user, new_data)

        assert user.name == "Новый юзер"

    async def test_delete_success(
        self,
        async_test_session: AsyncSession,
        repo: UsersRepository,
        new_user: UserProfileOrm,
    ) -> None:
        await repo.delete(async_test_session, new_user)
        await async_test_session.flush()
        assert inspect(new_user).deleted is True
