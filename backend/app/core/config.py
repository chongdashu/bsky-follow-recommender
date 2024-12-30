"""Application configuration management using Pydantic settings."""

from typing import list

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        app_name: Name of the application
        debug: Debug mode flag
        cors_origins: List of allowed CORS origins
    """

    app_name: str = "Blue Sky Recommender"
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]  # Add your frontend URL

    class Config:
        """Configuration settings for environment variables.

        Attributes:
            env_file: Path to the environment file
        """

        env_file = ".env"


settings = Settings()
