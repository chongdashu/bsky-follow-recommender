from fastapi import APIRouter, Depends
from typing import List
from ...services.bluesky.client import BlueskyClient
from ...models.schemas.responses import UserProfile, RecommendationResponse
from ...core.exceptions import BlueskyAPIError

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
    users = await client.get_user_suggestions(limit=limit)

    # Convert to recommendation responses with mock scores
    return [
        RecommendationResponse(
            user=user,
            score=0.95,  # This would be replaced with actual recommendation logic
            reason="Based on your interests and network",
        )
        for user in users
    ]
