"""Test script for Blue Sky user follows and recommendations functionality."""

import asyncio
import os
from pathlib import Path
import sys

from atproto import Client
from dotenv import load_dotenv

from app.bluesky.auth import create_bluesky_client
from app.core.logger import setup_logger
from app.services.recommenders.basic import BasicRecommender
from app.services.recommenders.common_followers import CommonFollowersRecommender


# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)


async def test_basic_recommender(client: Client) -> None:
    """Test the basic recommender that uses Blue Sky's built-in suggestions.

    Args:
        client: The authenticated Bluesky client
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


async def test_common_followers_recommender(client: Client) -> None:
    """Test the common followers recommender.

    Args:
        client: The authenticated Bluesky client
    """
    try:
        # Use some popular tech accounts as seed accounts
        seed_accounts = [
            "hamel.bsky.social",
            "togelius.bsky.social",
            "karpathy.bsky.social",
            "howard.fm",
        ]

        recommender = CommonFollowersRecommender(
            seed_accounts=seed_accounts, min_common_follows=2
        )
        recommendations = await recommender.get_recommendations(client, client.me.did)

        logger.info("\n=== Common Followers Recommender Results ===")
        logger.info(f"Found {len(recommendations)} recommendations")

        # Print first 5 recommendations
        for i, rec in enumerate(recommendations[:5], 1):
            logger.info(
                f"{i}. {rec.display_name or 'No display name'} (@{rec.handle})"
                f"\n   Followers: {rec.followers_count:,}"
            )

    except Exception as e:
        logger.error(f"Common followers recommender test failed: {e!s}")
        raise


async def main() -> None:
    """Run the recommendation tests."""
    try:
        client = create_bluesky_client(
            login=os.getenv("BLUESKY_IDENTIFIER"),
            password=os.getenv("BLUESKY_PASSWORD"),
        )

        await test_basic_recommender(client)
        await test_common_followers_recommender(client)

    except Exception as e:
        logger.error(f"Test failed: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
