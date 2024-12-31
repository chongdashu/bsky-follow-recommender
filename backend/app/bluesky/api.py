"""Blue Sky API client functions for fetching user data and recommendations."""

from atproto import Client, models as bsky_models
from backend.app.services.recommenders.base import RecommenderProtocol
from backend.app.services.recommenders.basic import BasicRecommender

from app.core.logger import setup_logger


logger = setup_logger(__name__)


async def get_user_follows(client: Client, actor: str) -> list[bsky_models.AppBskyActorDefs.ProfileView]:
    """Get list of accounts that a user follows.

    Args:
        client: Authenticated Blue Sky client
        actor: The user's handle or DID

    Returns:
        List of ProfileView objects representing followed accounts
    """
    try:
        response = client.app.bsky.graph.get_follows({"actor": actor})
        return response.follows
    except Exception as e:
        logger.error(f"Failed to get follows for {actor}: {e!s}")
        raise


async def get_user_recommendations(
    client: Client,
    actor: str,
    recommender: RecommenderProtocol | None = None,
) -> list[bsky_models.AppBskyActorDefs.ProfileViewDetailed]:
    """Get recommended accounts for a user using the specified recommendation strategy.

    Args:
        client: Authenticated Blue Sky client
        actor: The user's handle or DID
        recommender: Strategy to use for recommendations. Defaults to BasicRecommender

    Returns:
        List of ProfileView objects representing recommended accounts
    """
    try:
        recommender = recommender or BasicRecommender()
        return await recommender.get_recommendations(client, actor)
    except Exception as e:
        logger.error(f"Failed to get recommendations for {actor}: {e!s}")
        raise
