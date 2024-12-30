"""Blue Sky authentication utilities for creating and managing API clients."""

from atproto import Client

from app.core.logger import setup_logger


logger = setup_logger(__name__)


async def verify_credentials(identifier: str, password: str) -> tuple[bool, str | None]:
    """Verify Blue Sky credentials by attempting to authenticate.

    Args:
        identifier: Blue Sky account identifier (handle or email)
        password: Blue Sky account password

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        client = Client()
        client.login(identifier, password)
        return True, None
    except Exception as e:
        logger.error(f"Authentication failed: {e!s}")
        return False, str(e)


def create_bluesky_client(identifier: str, password: str) -> Client:
    """Create an authenticated Blue Sky client.

    Args:
        identifier: Blue Sky account identifier (handle or email)
        password: Blue Sky account password

    Returns:
        An authenticated Blue Sky client instance

    Raises:
        Exception: If authentication fails
    """
    try:
        client = Client()
        client.login(identifier, password)
        logger.info("Successfully authenticated with Blue Sky")
        return client
    except Exception as e:
        logger.error(f"Failed to authenticate with Blue Sky: {e!s}")
        raise
