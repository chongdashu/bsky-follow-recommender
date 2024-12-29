from atproto import Client

from app.core.config import settings
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def create_bluesky_client() -> Client:
    """Create an authenticated Blue Sky client.

    Returns:
        An authenticated Blue Sky client instance

    Raises:
        Exception: If authentication fails
    """
    try:
        client = Client()
        client.login(settings.bluesky_identifier, settings.bluesky_password)
        logger.info("Successfully authenticated with Blue Sky")
        return client
    except Exception as e:
        logger.error(f"Failed to authenticate with Blue Sky: {str(e)}")
        raise
