"""Blue Sky authentication utilities for creating and managing API clients."""

from datetime import datetime
from typing import Any

import httpx
from atproto import Client
from fastapi import HTTPException, status

from app.core.logger import setup_logger
from app.models.user import AuthResponse, UserProfile


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


async def authenticate_user(identifier: str, password: str) -> AuthResponse:
    """
    Authenticate user with Blue Sky credentials and return tokens.

    Args:
        identifier: Blue Sky identifier (handle or email)
        password: Blue Sky password

    Returns:
        AuthResponse containing JWT tokens and user profile

    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Blue Sky ATP authentication endpoint
        auth_url = "https://bsky.social/xrpc/com.atproto.server.createSession"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                auth_url,
                json={"identifier": identifier, "password": password},
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

            auth_data: dict[str, Any] = response.json()

            # Extract user profile data from response
            profile = UserProfile(
                did=auth_data["did"],
                handle=auth_data["handle"],
                display_name=auth_data.get("displayName"),
                avatar_url=auth_data.get("avatarUrl"),
                following_count=0,  # Need to fetch from profile API
                follower_count=0,  # Need to fetch from profile API
                created_at=datetime.now(),  # Need to fetch actual creation date
            )

            # Create auth response with tokens
            return AuthResponse(
                access_jwt=auth_data["accessJwt"],
                refresh_jwt=auth_data["refreshJwt"],
                profile=profile,
            )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error connecting to Blue Sky: {e!s}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {e!s}",
        )
