"""Test script for end-to-end testing of authentication and recommendations endpoints."""

import asyncio
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

from app.core.logger import setup_logger


# Add the project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

# Load environment variables
load_dotenv()

logger = setup_logger(__name__)

# API configuration
API_BASE_URL = "http://localhost:8000"  # Adjust if your API runs on a different port
TIMEOUT_SECONDS = 30.0  # Increase timeout for API calls


async def test_auth_flow() -> tuple[str, str]:
    """Test authentication flow and return access token.

    Returns:
        tuple[str, str]: Tuple of (access_token, user_did)

    Raises:
        Exception: If authentication fails
    """
    auth_url = f"{API_BASE_URL}/auth/login"
    credentials = {
        "identifier": os.getenv("BLUESKY_IDENTIFIER"),
        "password": os.getenv("BLUESKY_PASSWORD"),
    }

    if not all(credentials.values()):
        raise ValueError(
            "Missing BLUESKY_IDENTIFIER or BLUESKY_PASSWORD in environment"
        )

    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        response = await client.post(auth_url, json=credentials)

        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.text}")

        auth_data = response.json()
        logger.info("Successfully authenticated with Blue Sky")

        return auth_data["access_jwt"], auth_data["profile"]["did"]


async def test_recommendations(access_token: str) -> None:
    """Test getting recommendations for authenticated user.

    Args:
        access_token: JWT access token from authentication

    Raises:
        Exception: If fetching recommendations fails
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    # Test basic recommendations
    basic_url = f"{API_BASE_URL}/recommendations/?strategy=basic&limit=5"
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        try:
            response = await client.get(basic_url, headers=headers)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            logger.info(f"Response body: {response.text}")

            if response.status_code != 200:
                raise Exception(f"Failed to get basic recommendations: {response.text}")

            recommendations = response.json()["recommendations"]

            if not recommendations:
                logger.warning("No recommendations returned")

            logger.info("\n=== Basic Recommendations ===")
            for i, rec in enumerate(recommendations, 1):
                logger.info(
                    f"{i}. {rec['display_name'] or 'No display name'} (@{rec['handle']})"
                    f"\n   Followers: {rec['follower_count']:,}"
                    f"\n   Reason: {rec['reason']}"
                )

        except Exception as e:
            logger.error(f"Error in basic recommendations: {e!s}")
            logger.error(f"Full error: {e!r}")
            raise

    # Test common followers recommendations
    common_url = f"{API_BASE_URL}/recommendations/?strategy=common_followers&limit=5"
    async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
        response = await client.get(common_url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"Failed to get common followers recommendations: {response.text}"
            )

        recommendations = response.json()["recommendations"]

        logger.info("\n=== Common Followers Recommendations ===")
        for i, rec in enumerate(recommendations, 1):
            logger.info(
                f"{i}. {rec['display_name'] or 'No display name'} (@{rec['handle']})"
                f"\n   Followers: {rec['follower_count']:,}"
                f"\n   Reason: {rec['reason']}"
            )


async def main() -> None:
    """Run end-to-end test of authentication and recommendations."""
    try:
        # Test authentication
        access_token, user_did = await test_auth_flow()
        logger.info(f"Authenticated as user: {user_did}")

        # Test recommendations
        await test_recommendations(access_token)

    except Exception as e:
        logger.error(f"Test failed: {e!s}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
