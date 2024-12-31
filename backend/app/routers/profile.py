"""Profile related routes."""

from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.bluesky.auth import BlueskyAuthManager
from app.dependencies.bluesky import get_current_user
from app.models.auth import UserProfile
from app.models.profile import BlueskyProfileResponse


router = APIRouter(prefix="/v1", tags=["profile"])


@router.get("/profile", response_model=BlueskyProfileResponse)
async def get_current_profile(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
) -> BlueskyProfileResponse:
    """Get the current user's profile.

    Args:
        current_user: The authenticated user's profile from the JWT token

    Returns:
        BlueskyProfileResponse: The user's profile information
    """
    # Get the client for the current user
    client = BlueskyAuthManager.get_client(current_user.did)
    if not client:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="No authenticated client found")

    # Get detailed profile info
    profile = client.app.bsky.actor.get_profile({"actor": current_user.did})

    return BlueskyProfileResponse(
        did=profile.did,
        handle=profile.handle,
        displayName=profile.display_name or profile.handle,
        description=profile.description,
        avatar=profile.avatar,
        followersCount=profile.followers_count or 0,
        followsCount=profile.follows_count or 0,
        postsCount=profile.posts_count or 0,
    )
