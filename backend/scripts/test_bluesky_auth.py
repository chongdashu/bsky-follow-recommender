import sys
from pathlib import Path

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from app.bluesky.auth import create_bluesky_client
from app.core.logger import setup_logger

logger = setup_logger(__name__)


def test_auth() -> None:
    """Test Blue Sky authentication."""
    try:
        client = create_bluesky_client()
        logger.info("Authentication test successful")

        # Test getting profile info
        profile = client.app.bsky.actor.get_profile(
            {
                "actor": client.me.did,
            }
        )
        logger.info(f"Retrieved profile for: {profile.display_name}")

    except Exception as e:
        logger.error(f"Authentication test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    test_auth()