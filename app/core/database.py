from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Base class for all database models.

    Provides default `created_at` and `updated_at` timestamps.
    Custom `__repr__` method to avoid loading relationships and unnecessary queries.
    """

    __abstract__ = True

    # Timestamps for creation and last update
    created_at: Mapped[Annotated[datetime, mapped_column(server_default=func.now())]]
    updated_at: Mapped[
        Annotated[
            datetime,
            mapped_column(server_default=func.now(), server_onupdate=func.now()),
        ]
    ]

    repr_cols_num = 0  # Number of columns to include in the repr by default
    repr_cols = ()  # Specific columns to include in the repr

    def __repr__(self) -> str:
        """
        Custom repr method, avoids loading relationships to prevent unexpected queries.

        Returns:
            str: A string in the format "<ClassName col1=val1, col2=val2, ...>".
        """

        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
