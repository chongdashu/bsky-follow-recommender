"""Test script for Blue Sky user follows and recommendations functionality."""

import asyncio
import sys
from pathlib import Path

from app.bluesky.api import get_user_follows
from app.bluesky.auth import create_bluesky_client
from app.bluesky.recommenders import BasicRecommender, CommonFollowersRecommender
from app.core.logger import setup_logger


# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)


logger = setup_logger(__name__)


async def test_basic_recommender(client) -> None:
    """Test the basic recommender that uses Blue Sky's built-in suggestions.

    Args:
        client: Authenticated Blue Sky client
    """
    try:
        recommender = BasicRecommender()
        recommendations = await recommender.get_recommendations(client, client.me.did)

        logger.info("\n=== Basic Recommender Results ===")
        logger.info(f"Found {len(recommendations)} recommendations")

        # Print first 5 recommendations
        for i, rec in enumerate(recommendations[:5], 1):
            logger.info(
                f"{i}. {rec.display_name or 'No display name'} (@{rec.handle})"
                f"\n   Followers: {rec.followers_count:,}"
            )

    except Exception as e:
        logger.error(f"Basic recommender test failed: {e!s}")
        raise


async def test_common_followers_recommender(client) -> None:
    """Test the common followers recommender with seed accounts.

    Args:
        client: Authenticated Blue Sky client
    """
    try:
        # Test with some popular tech accounts as seeds
        seed_accounts = [
            "togelius.bsky.social",
            "hamel.bsky.social",
            "karpathy.bsky.social",
        ]

        recommender = CommonFollowersRecommender(
            seed_accounts=seed_accounts, min_common_follows=2
        )

        logger.info("\n=== Common Followers Recommender Results ===")
        logger.info(f"Using {len(seed_accounts)} seed accounts")

        recommendations = await recommender.get_recommendations(client, client.me.did)
        logger.info(f"Found {len(recommendations)} recommendations")

        # Print first 5 recommendations
        for i, rec in enumerate(recommendations[:5], 1):
            logger.info(
                f"{i}. {rec.display_name or 'No display name'} (@{rec.handle})"
                f"\n   Followers: {rec.followers_count:,}"
                f"\n   Description: {rec.description[:100]}..."
                if rec.description
                else ""
            )

    except Exception as e:
        logger.error(f"Common followers recommender test failed: {e!s}")
        raise


async def test_recommendations() -> None:
    """Test both recommendation strategies."""
    try:
        client = create_bluesky_client()
        if not client.me:
            raise ValueError("Client not authenticated - no user information available")

        # Get user's follows as baseline
        follows = await get_user_follows(client, client.me.did)
        logger.info(f"User currently follows {len(follows)} accounts")

        # Test both recommenders
        # await test_basic_recommender(client)
        await test_common_followers_recommender(client)

    except Exception as e:
        logger.error(f"Recommendation tests failed: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_recommendations())
