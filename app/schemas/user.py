from enum import Enum

from pydantic import UUID4, BaseModel, ConfigDict, Field


class SexEnum(str, Enum):
    male = "Мужской"
    female = "Женский"


class UserProfileAdd(BaseModel):
    name: str
    about_me: str | None = Field(default=None)
    age: int = Field(gt=0, le=120)
    city: str
    sex: SexEnum

    model_config = ConfigDict(from_attributes=True)


class UserProfile(UserProfileAdd):
    uuid: UUID4


class UserProfilePatch(BaseModel):
    name: str | None = Field(default=None)
    about_me: str | None = Field(default=None)
    age: int | None = Field(gt=0, le=120, default=None)
    city: str | None = Field(default=None)
    sex: SexEnum | None = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
