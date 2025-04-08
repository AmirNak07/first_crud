from enum import Enum

from sqlalchemy import BigInteger, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SexEnumDB(str, Enum):
    male = "Мужской"
    female = "Женский"


class UserProfileOrm(Base):
    __tablename__ = "user_profiles"
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    about_me: Mapped[str | None] = mapped_column(
        String(300), default=None, nullable=True
    )
    age: Mapped[int] = mapped_column(SmallInteger)
    city: Mapped[str] = mapped_column(String(50))
    sex: Mapped[SexEnumDB]

    repr_cols = ("telegram_id", "name", "telegram_id")
