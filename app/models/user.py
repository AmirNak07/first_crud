from uuid import UUID as UUID_type
from uuid import uuid4

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.schemas.user import UserProfile


class UserProfileOrm(Base):
    __tablename__ = "users"
    uuid: Mapped[UUID_type] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String)
    about_me: Mapped[str | None] = mapped_column(String, default=None)
    age: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String)
    sex: Mapped[str] = mapped_column(String)

    repr_cols = ("uuid", "name")

    def to_read_model(self) -> UserProfile:
        return UserProfile(
            name=self.name,
            about_me=self.about_me,
            age=self.age,
            city=self.city,
            sex=self.sex,
            uuid=self.uuid,
        )
