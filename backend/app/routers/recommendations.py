from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.dependencies.auth import get_current_user
from app.models.user import UserProfile


class RecommendedUser(BaseModel):
    """Recommended user to follow"""

    did: str
    handle: str
    display_name: str | None = None
    avatar_url: str | None = None
    follower_count: int
    following_count: int
    reason: str


class RecommendationsResponse(BaseModel):
    """Response containing recommended users to follow"""

    recommendations: list[RecommendedUser]


router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", response_model=RecommendationsResponse)
async def get_recommendations(
    current_user: Annotated[UserProfile, Depends(get_current_user)], limit: int = 10
) -> RecommendationsResponse:
    """
    Get personalized user recommendations based on the authenticated user's profile

    Args:
        current_user: The authenticated user's profile
        limit: Maximum number of recommendations to return

    Returns:
        RecommendationsResponse containing list of recommended users
    """
    # Implement recommendation logic here
    # This is a placeholder implementation
    recommendations = [
        RecommendedUser(
            did="example.did",
            handle="example.user",
            display_name="Example User",
            follower_count=100,
            following_count=50,
            reason="Popular in your network",
        )
    ]

    return RecommendationsResponse(recommendations=recommendations)
