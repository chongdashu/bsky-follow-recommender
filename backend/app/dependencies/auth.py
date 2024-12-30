from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.models.user import UserProfile


security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> UserProfile:
    """
    Validates the JWT token and returns the current user profile.

    Args:
        credentials: The HTTP Authorization credentials containing the JWT token

    Returns:
        UserProfile: The authenticated user's profile

    Raises:
        HTTPException: If the token is invalid or expired
    """
    try:
        # Here you would implement JWT validation and user lookup
        # This is a placeholder - implement actual JWT validation
        if not credentials.credentials:
            raise ValueError("Invalid token")

        # Verify token and get user profile
        # Replace with actual JWT verification and user lookup
        user = UserProfile(
            did="placeholder",
            handle="placeholder",
            created_at=datetime.now(),
            display_name="placeholder",
            avatar_url="placeholder",
            following_count=0,
            follower_count=0,
        )
        return user

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
