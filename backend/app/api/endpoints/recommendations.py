from fastapi import APIRouter, Depends
from typing import List
from app.services.bluesky.client import BlueskyClient
from app.models.schemas.responses import UserProfile, RecommendationResponse
from app.core.exceptions import BlueskyAPIError
from app.services.recommendations.user_recommender import UserRecommender

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


async def get_bluesky_client() -> BlueskyClient:
    """
    Dependency to get Bluesky client instance.

    Returns:
        BlueskyClient: Initialized Bluesky client
    """
    client = BlueskyClient()
    await client.connect()
    return client


@router.get("/users", response_model=List[RecommendationResponse])
async def get_recommended_users(
    limit: int = 10, client: BlueskyClient = Depends(get_bluesky_client)
) -> List[RecommendationResponse]:
    """
    Get recommended users to follow.

    Args:
        limit: Maximum number of recommendations to return
        client: Bluesky client instance

    Returns:
        List[RecommendationResponse]: List of recommended users with scores
    """
    recommender = UserRecommender(client)
    return await recommender.get_recommendations(limit=limit)
