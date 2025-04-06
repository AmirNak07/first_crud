from uuid import UUID as UUID_type
from uuid import uuid4

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserProfileOrm(Base):
    __tablename__ = "users"
    uuid: Mapped[UUID_type] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    about_me: Mapped[str | None] = mapped_column(
        String(300), default=None, nullable=True
    )
    age: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(50))
    sex: Mapped[str] = mapped_column(String(8))

    repr_cols = ("uuid", "name")
