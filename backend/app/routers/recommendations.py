from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.bluesky.auth import BlueskyAuthManager
from app.bluesky.recommenders import BasicRecommender, CommonFollowersRecommender
from app.core.logger import setup_logger
from app.dependencies.auth import get_current_user
from app.models.user import UserProfile


logger = setup_logger(__name__)


class RecommendedUser(BaseModel):
    """Recommended user to follow."""

    did: str
    handle: str
    display_name: str | None = None
    avatar_url: str | None = None
    follower_count: int
    following_count: int
    reason: str


class RecommendationsResponse(BaseModel):
    """Response containing recommended users to follow."""

    recommendations: list[RecommendedUser]


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=RecommendationsResponse)
async def get_recommendations(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    strategy: str = "basic",
    limit: int = 10,
) -> RecommendationsResponse:
    """Get personalized user recommendations.

    Args:
        current_user: The authenticated user's profile
        strategy: Recommendation strategy ('basic' or 'common_followers')
        limit: Maximum number of recommendations to return

    Returns:
        RecommendationsResponse containing list of recommended users

    Raises:
        HTTPException: If fetching recommendations fails
    """
    try:
        # Get cached client
        client = BlueskyAuthManager.get_client(current_user.did)
        logger.info(f"Retrieved client for user: {current_user.did}")
        if not client:
            logger.error(f"No client found for user: {current_user.did}")
            raise ValueError("No authenticated client found")

        # Add timeout to the client's session if needed
        if hasattr(client, "_session") and client._session:
            client._session.timeout = 30.0

        # Choose recommender based on strategy
        if strategy == "basic":
            recommender = BasicRecommender()
        elif strategy == "common_followers":
            # Use some popular tech accounts as seeds
            recommender = CommonFollowersRecommender(
                seed_accounts=[
                    "togelius.bsky.social",
                    "hamel.bsky.social",
                    "karpathy.bsky.social",
                ],
                min_common_follows=2,
            )
        else:
            raise ValueError(f"Invalid recommendation strategy: {strategy}")

        # Get recommendations
        profiles = await recommender.get_recommendations(client, current_user.did)

        # Convert to response format
        recommendations = [
            RecommendedUser(
                did=profile.did,
                handle=profile.handle,
                display_name=profile.display_name,
                avatar_url=profile.avatar,
                follower_count=profile.followers_count or -1,
                following_count=profile.follows_count or -1,
                reason="Popular in your network"
                if strategy == "basic"
                else "Common connections",
            )
            for profile in profiles[:limit]
        ]

        return RecommendationsResponse(recommendations=recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {e!s}",
        )
