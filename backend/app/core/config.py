"""Application configuration management using Pydantic settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.

    Attributes:
        app_name: Name of the application
        debug: Debug mode flag
        bluesky_identifier: Blue Sky account identifier
        bluesky_password: Blue Sky account password
    """

    app_name: str = "Blue Sky Recommender"
    debug: bool = False
    bluesky_identifier: str
    bluesky_password: str

    class Config:
        """Configuration settings for environment variables.

        Attributes:
            env_file: Path to the environment file
        """

        env_file = ".env"


settings = Settings()
