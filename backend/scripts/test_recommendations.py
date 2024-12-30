"""Test script for Blue Sky user follows and recommendations functionality."""

import asyncio
import sys
from pathlib import Path

from app.bluesky.api import get_user_follows, get_user_recommendations
from app.bluesky.auth import create_bluesky_client
from app.core.logger import setup_logger


# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)


logger = setup_logger(__name__)


async def test_recommendations() -> None:
    """Test getting follows and recommendations."""
    try:
        client = create_bluesky_client()
        if not client.me:
            raise ValueError("Client not authenticated - no user information available")

        # Get user's follows
        follows = await get_user_follows(client, client.me.did)
        logger.info(f"Found {len(follows)} follows")

        # Get recommendations
        recommendations = await get_user_recommendations(client, client.me.did)
        logger.info(f"Found {len(recommendations)} recommendations")

        # Print first 5 recommendations
        for rec in recommendations[:5]:
            display_name = rec.display_name or "No display name"
            handle = rec.handle
            logger.info(f"Recommended: {display_name} (@{handle})")

    except Exception as e:
        logger.error(f"Recommendation test failed: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_recommendations())
