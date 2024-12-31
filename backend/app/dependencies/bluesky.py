"""Dependencies for Blue Sky authentication and client management."""

from datetime import datetime
from typing import Annotated

from atproto import Client
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.bluesky.auth import BlueskyAuthManager, create_bluesky_client
from app.core.config import get_settings
from app.models.auth import UserAuth, UserProfile


security = HTTPBearer()
settings = get_settings()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UserProfile:
    """Validate JWT token and return current user profile.

    Args:
        credentials: The HTTP Authorization credentials containing the JWT token

    Returns:
        UserProfile: The authenticated user's profile

    Raises:
        HTTPException: If the token is invalid or expired
    """
    try:
        # Decode JWT token
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        did: str = payload.get("sub")
        if not did:
            raise ValueError("Invalid token payload")

        # Get cached client
        client = BlueskyAuthManager.get_client(did)
        if not client:
            raise ValueError("No authenticated client found")

        # Get current profile
        profile = client.app.bsky.actor.get_profile({"actor": did})

        return UserProfile(
            did=did,
            handle=profile.handle,
            display_name=profile.display_name,
            avatar_url=profile.avatar,
            following_count=profile.follows_count or -1,
            follower_count=profile.followers_count or -1,
            created_at=datetime.now(),  # Use actual creation date if available
        )

    except (JWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_bluesky_client(
    current_user: Annotated[UserAuth, Depends(get_current_user)],
) -> Client:
    """Create authenticated Blue Sky client for current user.

    Args:
        current_user: The authenticated user's credentials

    Returns:
        Authenticated Blue Sky client

    Raises:
        HTTPException: If client creation or authentication fails
    """
    try:
        client = create_bluesky_client(
            login=current_user.identifier,
            password=current_user.password,
        )
        return client
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to authenticate with Blue Sky. Please check your credentials.",
        ) from e
