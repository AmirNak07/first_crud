from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    preference: Mapped["UserPreferenceOrm"] = relationship(back_populates="profile")

    repr_cols = ("telegram_id", "name", "telegram_id")


# Add tables: "user_preferences" and "profile_photos"


class UserPreferenceOrm(Base):
    __tablename__ = "user_preferences"
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user_profiles.telegram_id", ondelete="CASCADE"),
        primary_key=True,
    )
    sex: Mapped[SexEnumDB]

    profile: Mapped["UserProfileOrm"] = relationship(back_populates="preference")
