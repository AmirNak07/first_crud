from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration class for loading environment variables.
    """

    POSTGRES_USER: str  # PostgreSQL username
    POSTGRES_PASSWORD: str  # PostgreSQL password
    POSTGRES_HOST: str  # PostgreSQL host
    POSTGRES_PORT: int  # PostgreSQL port
    POSTGRES_DB: str  # PostgreSQL database name

    SECRET_API_KEY: str  # Secret key for API

    MODE: str  # Application mode (e.g. DEV, TEST, PROD)

    # Configuration to load .env file with UTF-8 encoding
    model_config = SettingsConfigDict(env_file="./.env", env_file_encoding="utf-8")

    @property
    def DATABASE_URL(self) -> str:
        """
        Generates a PostgreSQL connection string for asyncpg.

        Returns:
            str: The PostgreSQL connection URL for asyncpg.
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
