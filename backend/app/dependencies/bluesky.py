"""Dependencies for Blue Sky client management."""

from typing import Annotated

from atproto import Client
from fastapi import Depends, HTTPException, status

from app.bluesky.auth import create_bluesky_client
from app.dependencies.auth import get_current_user
from app.models.user import UserAuth


async def get_bluesky_client(
    current_user: Annotated[UserAuth, Depends(get_current_user)],
) -> Client:
    """
    FastAPI dependency that creates an authenticated Blue Sky client for the current user.

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
