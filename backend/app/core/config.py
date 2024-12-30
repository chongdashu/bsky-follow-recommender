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
    """

    API_V1_STR: str
    BLUESKY_API_URL: str
    BLUESKY_IDENTIFIER: str
    BLUESKY_PASSWORD: str
    DEBUG: bool = False
    CORS_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
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
