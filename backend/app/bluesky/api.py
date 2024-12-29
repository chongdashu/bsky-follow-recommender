"""Blue Sky API client functions for fetching user data and recommendations."""

from typing import Any

from atproto import Client

from app.core.logger import setup_logger


logger = setup_logger(__name__)


async def get_user_follows(client: Client, actor: str) -> list[dict[str, Any]]:
    """Get list of accounts that a user follows.

    Args:
        client: Authenticated Blue Sky client
        actor: The user's handle or DID

    Returns:
        List of follow records
    """
    try:
        response = client.app.bsky.graph.getFollows({"actor": actor})
        return response.follows
    except Exception as e:
        logger.error(f"Failed to get follows for {actor}: {e!s}")
        raise


async def get_user_recommendations(client: Client, actor: str) -> list[dict[str, Any]]:
    """Get recommended accounts for a user.

    Args:
        client: Authenticated Blue Sky client
        actor: The user's handle or DID

    Returns:
        List of recommended accounts
    """
    try:
        response = client.app.bsky.actor.getSuggestions({"limit": 50})
        return response.actors
    except Exception as e:
        logger.error(f"Failed to get recommendations for {actor}: {e!s}")
        raise
