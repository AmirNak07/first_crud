import pytest
from pydantic import ConfigDict, ValidationError

from app.schemas.user_schema import (
    UserPreferencesCreate,
    UserPreferencesRead,
    UserProfileCreate,
    UserProfilePatch,
    UserProfileRead,
)


class TestProfile:
    # UserProfileCreate
    def test_create_valid(self, profile_data):
        user = UserProfileCreate(**profile_data)
        assert user.name == profile_data["name"]
        assert user.about_me == profile_data["about_me"]
        assert user.age == profile_data["age"]
        assert user.city == profile_data["city"]
        assert user.sex == profile_data["sex"]

    def test_create_invalid_name(self, profile_data):
        profile_data["name"] = (
            "Юзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерюзерр"
        )

        with pytest.raises(ValidationError):
            UserProfileCreate(**profile_data)

    def test_create_invalid_about_me(self, profile_data):
        profile_data["about_me"] = (
            "Какие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данныеКакие-нибудь данные"
        )

        with pytest.raises(ValidationError):
            UserProfileCreate(**profile_data)

    def test_create_invalid_negative_age(self, profile_data):
        profile_data["age"] = -1

        with pytest.raises(ValidationError):
            UserProfileCreate(**profile_data)

    def test_create_invalid_greater_age(self, profile_data):
        profile_data["age"] = 121

        with pytest.raises(ValidationError):
            UserProfileCreate(**profile_data)

    def test_create_invalid_sex(self, profile_data):
        profile_data["sex"] = "Тебе какая разница?"

        with pytest.raises(ValidationError):
            UserProfileCreate(**profile_data)

    def test_create_default_values(self, profile_data):
        del profile_data["about_me"]
        del profile_data["sex"]
        user = UserProfileCreate(**profile_data)

        assert user.about_me is None
        assert user.model_config == ConfigDict(from_attributes=True)
        assert user.sex == "Не указан"

    def test_create_with_age_string(self, profile_data):
        profile_data["age"] = "18"

        user = UserProfileCreate(**profile_data)
        assert user.age == 18

    def test_create_invalid_with_age_float(self, profile_data):
        profile_data["age"] = 18.8

        with pytest.raises(ValidationError):
            UserProfileCreate(**profile_data)

    # UserProfileRead
    def test_read_valid(self, profile_data):
        profile_data["telegram_id"] = 100

        user = UserProfileRead(**profile_data)
        assert user.telegram_id == 100

    def test_read_invalid(self, profile_data):
        profile_data["telegram_id"] = -1

        with pytest.raises(ValidationError):
            UserProfileRead(**profile_data)

    # UserProfilePatch
    def test_patch_valid(self, profile_data):
        user = UserProfilePatch(**profile_data)
        assert user.name == profile_data["name"]
        assert user.about_me == profile_data["about_me"]
        assert user.age == profile_data["age"]
        assert user.city == profile_data["city"]
        assert user.sex == profile_data["sex"]

    def test_patch_default(self):
        user = UserProfilePatch()
        assert user.name is None
        assert user.about_me is None
        assert user.age is None
        assert user.city is None
        assert user.sex is None
        assert user.model_config == ConfigDict(from_attributes=True)

    def test_patch_defaule(self, profile_data):
        profile_data["age"] = 121

        with pytest.raises(ValidationError):
            UserProfilePatch(**profile_data)


class TestPreferences:
    # UserPreferecesCreate
    def test_create_valid(self, preference_data):
        preference = UserPreferencesCreate(**preference_data)

        assert preference.sex == "Мужской"

    def test_create_invalid(self, preference_data):
        preference_data["sex"] = "Тебе какая разница?"

        with pytest.raises(ValidationError):
            UserProfilePatch(**preference_data)

    def test_create_default(self):
        preference = UserPreferencesCreate()

        assert preference.sex == "Не указан"
        assert preference.model_config == ConfigDict(from_attributes=True)

    # UserPreferencesRead
    def test_read_valid(self, preference_data):
        preference_data["telegram_id"] = 123

        preference = UserPreferencesRead(**preference_data)

        assert preference.telegram_id == preference_data["telegram_id"]
        assert preference.sex == preference_data["sex"]

    def test_read_invalid_negative_telegram_id(self, preference_data):
        preference_data["telegram_id"] = -1

        with pytest.raises(ValidationError):
            UserPreferencesRead(**preference_data)
