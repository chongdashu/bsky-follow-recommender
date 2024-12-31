from pydantic import BaseModel, Field


class BlueskyProfileResponse(BaseModel):
    """Response model for Bluesky user profile."""

    did: str = Field(..., description="Decentralized identifier")
    handle: str = Field(..., description="User handle")
    displayName: str = Field(..., description="Display name")
    description: str | None = Field(None, description="Profile description")
    avatar: str | None = Field(None, description="Avatar URL")
    followersCount: int = Field(0, description="Number of followers")
    followsCount: int = Field(0, description="Number of follows")
    postsCount: int = Field(0, description="Number of posts")
