"""Profile related routes."""

import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.bluesky.api import get_user_follows
from app.bluesky.auth import BlueskyAuthManager
from app.dependencies.bluesky import get_current_user
from app.models.auth import UserProfile
from app.models.profile import BlueskyProfileResponse


router = APIRouter(prefix="/v1", tags=["profile"])


class FollowRequest(BaseModel):
    """Request body for following a user."""

    handle: str = Field(..., description="Handle of the user to follow")


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


@router.get("/follows", response_model=list[BlueskyProfileResponse])
async def get_follows(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
) -> list[BlueskyProfileResponse]:
    """Get the list of accounts that the current user follows.

    Args:
        current_user: The authenticated user's profile from the JWT token

    Returns:
        List of BlueskyProfileResponse: The profiles of followed accounts
    """
    client = BlueskyAuthManager.get_client(current_user.did)
    if not client:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="No authenticated client found")

    follows = await get_user_follows(client, current_user.did)

    return [
        BlueskyProfileResponse(
            did=profile.did,
            handle=profile.handle,
            displayName=profile.display_name or profile.handle,
            description=profile.description,
            avatar=profile.avatar,
            followersCount=profile.followers_count or 0,
            followsCount=profile.follows_count or 0,
            postsCount=profile.posts_count or 0,
        )
        for profile in follows
    ]


@router.post("/follow", status_code=HTTPStatus.NO_CONTENT)
async def follow_user(
    follow_request: FollowRequest,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
) -> None:
    """Follow a user by their handle.

    Args:
        follow_request: Request containing the handle of the user to follow
        current_user: The authenticated user's profile from the JWT token

    Raises:
        HTTPException: If the client is not authenticated or if following fails
    """
    client = BlueskyAuthManager.get_client(current_user.did)
    if not client:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="No authenticated client found")

    try:
        # First resolve the handle to get the DID
        resolved = client.app.bsky.actor.get_profile({"actor": follow_request.handle})

        # Create the follow record with the required format
        follow_record = {
            "repo": current_user.did,
            "collection": "app.bsky.graph.follow",
            "record": {
                "subject": resolved.did,
                "createdAt": datetime.datetime.now(datetime.UTC).isoformat(),
            },
        }

        # Follow the user using the correct record format
        client.com.atproto.repo.create_record(follow_record)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Failed to follow user: {e!s}")
