from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import RepositoryError
from app.repositories.preferences_repository import UserPreferenceRepository
from app.repositories.profile_repository import UserProfileRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profiles = UserProfileRepository(session)
        self.preferences = UserPreferenceRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            try:
                await self.session.rollback()
            except Exception:
                pass

            if issubclass(exc_type, SQLAlchemyError):
                raise RepositoryError("Database error occurred") from exc_val

            return False
        else:
            try:
                await self.session.commit()
            except SQLAlchemyError as commit_error:
                await self.session.rollback()
                raise RepositoryError(
                    "Database error occurred during commit"
                ) from commit_error
