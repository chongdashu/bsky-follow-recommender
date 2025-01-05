"""Models for recommendation-related data."""

from pydantic import BaseModel, Field


class RecommendedUser(BaseModel):
    """Recommended user to follow."""

    did: str = Field(..., description="Decentralized identifier")
    handle: str = Field(..., description="User handle")
    displayName: str | None = Field(None, description="Display name")
    description: str | None = Field(None, description="User bio")
    avatar: str | None = Field(None, description="Avatar URL")
    followersCount: int = Field(0, description="Number of followers")
    followsCount: int = Field(0, description="Number of follows")
    postsCount: int = Field(0, description="Number of posts")
    reason: str = Field(..., description="Reason for recommendation")


class RecommendationsResponse(BaseModel):
    """Response containing recommended users to follow."""

    recommendations: list[RecommendedUser] = Field(..., description="List of recommended users")
