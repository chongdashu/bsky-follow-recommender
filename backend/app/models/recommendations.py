"""Models for recommendation-related data."""

from pydantic import BaseModel, Field


class RecommendedUser(BaseModel):
    """Recommended user to follow."""

    did: str = Field(..., description="Decentralized identifier")
    handle: str = Field(..., description="User handle")
    display_name: str | None = Field(None, description="Display name")
    avatar_url: str | None = Field(None, description="Avatar URL")
    follower_count: int = Field(0, description="Number of followers")
    following_count: int = Field(0, description="Number of users being followed")
    reason: str = Field(..., description="Reason for recommendation")


class RecommendationsResponse(BaseModel):
    """Response containing recommended users to follow."""

    recommendations: list[RecommendedUser] = Field(
        ..., description="List of recommended users"
    )
