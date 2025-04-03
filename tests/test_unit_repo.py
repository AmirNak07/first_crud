import pytest

from app.repositories.user_repository import UsersRepository


@pytest.mark.asyncio(loop_scope="session")
async def test_create_user(async_test_session):
    repo = UsersRepository()
    await repo.delete_all(async_test_session)

    user_data = {"name": "string", "age": 10, "city": "Москва", "sex": "Мужской"}
    new_user = await repo.add_one(async_test_session, user_data)

    assert new_user.name == "string"
    assert new_user.age == 10
    assert new_user.about_me is None
    assert new_user.city == "Москва"
    assert new_user.sex == "Мужской"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_users(async_test_session):
    repo = UsersRepository()
    await repo.delete_all(async_test_session)

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
