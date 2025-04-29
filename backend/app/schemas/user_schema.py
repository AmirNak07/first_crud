from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class SexEnum(str, Enum):
    male = "Мужской"
    female = "Женский"


class UserProfileCreate(BaseModel):
    name: str = Field(max_length=100)
    about_me: str | None = Field(default=None, max_length=300)
    age: int = Field(gt=0, le=120)
    city: str = Field(max_length=50)
    sex: SexEnum

    model_config = ConfigDict(from_attributes=True)


class UserProfileRead(UserProfileCreate):
    telegram_id: int


class UserProfilePatch(BaseModel):
    name: str | None = Field(default=None)
    about_me: str | None = Field(default=None)
    age: int | None = Field(gt=0, le=120, default=None)
    city: str | None = Field(default=None)
    sex: SexEnum | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)


class UserPreferencesCreate(BaseModel):
    sex: SexEnum


class UserPreferencesRead(UserPreferencesCreate):
    telegram_id: int
