"""Test script for validating Blue Sky authentication and profile retrieval."""

import os
from pathlib import Path
import sys

from atproto import Client
from dotenv import load_dotenv

from app.bluesky.auth import create_bluesky_client
from app.core.logger import setup_logger


# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)


def get_following(client: Client) -> None:
    """
    Retrieve and log information about accounts the user follows.

    Args:
        client: The authenticated Bluesky client
    """
    try:
        # Ensure we have authenticated user information
        if not client.me:
            raise ValueError("No authenticated user found")

        # Get the list of accounts the user follows
        following = client.app.bsky.graph.get_follows(
            {
                "actor": client.me.did,
                "limit": 100,  # Adjust limit as needed
            }
        )

        logger.info(f"Found {len(following.follows)} followed accounts:")

        for account in following.follows:
            logger.info(
                f"DID: {account.did}, "
                f"Display Name: {account.display_name}, "
                f"Handle: {account.handle}"
            )

    except Exception as e:
        logger.error(f"Error fetching following list: {e!s}")


def test_auth() -> None:
    """Test Blue Sky authentication and fetch user profile and following list."""
    try:
        # Get credentials from environment
        identifier = os.getenv("BLUESKY_IDENTIFIER")
        password = os.getenv("BLUESKY_PASSWORD")

        if not identifier or not password:
            raise ValueError(
                "Missing BLUESKY_IDENTIFIER or BLUESKY_PASSWORD in environment"
            )

        client = create_bluesky_client(login=identifier, password=password)
        logger.info("Authentication test successful")

        # Ensure we have authenticated user information
        if not client.me:
            raise ValueError("No authenticated user found")

        # Test getting profile info
        profile = client.app.bsky.actor.get_profile(
            {
                "actor": client.me.did,
            }
        )
        logger.info(f"Retrieved profile for: {profile.display_name}")

        # Get and log following information
        get_following(client)

    except Exception as e:
        logger.error(f"Authentication test failed: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    test_auth()
