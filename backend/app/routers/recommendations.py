from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.bluesky.auth import BlueskyAuthManager
from app.core.logger import setup_logger
from app.dependencies.bluesky import get_current_user
from app.models.auth import UserProfile
from app.models.recommendations import RecommendationsResponse, RecommendedUser
from app.services.recommenders.common_followers import (
    CommonFollowersRecommender,
)


logger = setup_logger(__name__)


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


# Add request model for seed handles
class RecommendationRequest(BaseModel):
    seed_handles: list[str]


@router.post("/", response_model=RecommendationsResponse)
async def get_recommendations(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    request: RecommendationRequest,  # Change to use request body
    limit: int = 10,
) -> RecommendationsResponse:
    """Get personalized user recommendations based on seed accounts.

    Args:
        current_user: The authenticated user's profile
        request: Request containing seed handles
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

        # Use common followers recommender with provided seed accounts
        recommender = CommonFollowersRecommender(
            seed_accounts=request.seed_handles,  # Use handles from request
            min_common_follows=2,
        )

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
                reason="Common connections",
            )
            for profile in profiles[:limit]
        ]

        return RecommendationsResponse(recommendations=recommendations)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {e!s}",
        )
