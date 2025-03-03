from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now())]]
    updated_at: Mapped[
        Annotated[
            datetime,
            mapped_column(server_default=func.now(), server_onupdate=func.now()),
        ]
    ]

    repr_cols_num = 0
    repr_cols = ()

    def __repr__(self):
        """Relationship не используется в repr(), т.к. могут привести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
