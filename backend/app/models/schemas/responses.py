from pydantic import BaseModel, HttpUrl
from typing import Optional


class UserProfile(BaseModel):
    """
    Schema for user profile information.
    """

    did: str
    handle: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    followers_count: int = 0
    following_count: int = 0


class RecommendationResponse(BaseModel):
    """
    Schema for recommendation response.
    """

    user: UserProfile
    score: float
    reason: str
