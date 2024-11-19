from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings and environment variables configuration.

    Attributes:
        PROJECT_NAME: Name of the project
        VERSION: API version
        API_PREFIX: Prefix for all API endpoints
        DEBUG: Debug mode flag
        BLUESKY_IDENTIFIER: Bluesky account identifier (email)
        BLUESKY_PASSWORD: Bluesky account password
        BLUESKY_SERVICE: Bluesky service URL
        ALLOWED_HOSTS: List of allowed hosts for CORS
    """

    PROJECT_NAME: str = "Bluesky Recommendations API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Bluesky Configuration
    BLUESKY_IDENTIFIER: str
    BLUESKY_PASSWORD: str
    BLUESKY_SERVICE: str = "https://bsky.social"

    # CORS Configuration
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Creates and caches the settings instance.

    Returns:
        Settings: Application settings instance
    """
    return Settings()
