"""Authentication-related models."""

from datetime import datetime

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile data from Blue Sky"""

    did: str = Field(..., description="Decentralized identifier")
    handle: str = Field(..., description="User handle")
    display_name: str | None = Field(None, description="Display name")
    avatar_url: str | None = Field(None, description="Avatar URL")
    following_count: int = Field(0, description="Number of users being followed")
    follower_count: int = Field(0, description="Number of followers")
    created_at: datetime = Field(..., description="Account creation timestamp")


class UserAuth(BaseModel):
    """Authentication data for a Blue Sky user"""

    identifier: str = Field(..., description="Blue Sky identifier (handle or email)")
    password: str = Field(..., description="Blue Sky password")


class AuthResponse(BaseModel):
    """Response containing authentication tokens and user profile"""

    access_jwt: str = Field(..., description="JWT access token")
    refresh_jwt: str = Field(..., description="JWT refresh token")
    profile: "UserProfile" = Field(..., description="User profile information")
