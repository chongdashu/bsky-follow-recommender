"""Application configuration management using Pydantic settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        API_V1_STR: API version 1 string prefix
        BLUESKY_API_URL: Blue Sky API base URL
        BLUESKY_IDENTIFIER: Blue Sky user identifier
        BLUESKY_PASSWORD: Blue Sky user password
        DEBUG: Debug mode flag
        CORS_ORIGINS: List of allowed CORS origins
        JWT_SECRET_KEY: JWT secret key
        JWT_ALGORITHM: JWT algorithm
        ACCESS_TOKEN_EXPIRE_MINUTES: Access token expiration minutes
        REFRESH_TOKEN_EXPIRE_MINUTES: Refresh token expiration minutes
    """

    API_V1_STR: str
    BLUESKY_API_URL: str
    BLUESKY_IDENTIFIER: str
    BLUESKY_PASSWORD: str
    DEBUG: bool = False
    CORS_ORIGINS: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow",
    )

    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS_ORIGINS string into list.

        Returns:
            list[str]: List of allowed CORS origins
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings instance
    """
    return Settings()
