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
    request: RecommendationRequest,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
) -> RecommendationsResponse:
    """Get recommended accounts based on seed accounts.

    Args:
        request: The recommendation request containing seed handles
        current_user: The authenticated user's profile

    Returns:
        RecommendationsResponse: List of recommended accounts
    """
    client = BlueskyAuthManager.get_client(current_user.did)
    if not client:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No authenticated client found")

    try:
        recommender = CommonFollowersRecommender(request.seed_handles)
        recommendations = await recommender.get_recommendations(client, current_user.did)

        return RecommendationsResponse(
            recommendations=[
                RecommendedUser(
                    did=profile.did,
                    handle=profile.handle,
                    displayName=profile.display_name or profile.handle,
                    description=profile.description,
                    avatar=profile.avatar,
                    followersCount=profile.followers_count or 0,
                    followsCount=profile.follows_count or 0,
                    postsCount=profile.posts_count or 0,
                    reason="Followed by multiple accounts you selected",
                )
                for profile in recommendations
            ]
        )
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e!s}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get recommendations")
