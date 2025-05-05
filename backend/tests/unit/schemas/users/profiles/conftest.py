import pytest


@pytest.fixture
def profile_data():
    user_data = {
        "name": "Юзер",
        "about_me": "Какие-нибудь данные",
        "age": 18,
        "city": "Москва",
        "sex": "Мужской",
    }

    return user_data


@pytest.fixture
def preference_data():
    preference_data = {"sex": "Мужской"}

    return preference_data
