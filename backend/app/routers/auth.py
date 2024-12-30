"""Router for Blue Sky authentication endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.bluesky.auth import verify_credentials


router = APIRouter()


class BlueskyCredentials(BaseModel):
    """Credentials for Blue Sky authentication.

    Attributes:
        identifier: Blue Sky account identifier (handle or email)
        password: Blue Sky account password
    """

    identifier: str
    password: str


class AuthResponse(BaseModel):
    """Response model for authentication attempts.

    Attributes:
        is_valid: Whether the credentials are valid
        error: Error message if authentication failed
    """

    is_valid: bool
    error: str | None = None


@router.post("/auth/verify", response_model=AuthResponse)
async def verify_auth(credentials: BlueskyCredentials) -> AuthResponse:
    """Verify Blue Sky credentials.

    Args:
        credentials: Blue Sky authentication credentials

    Returns:
        Authentication response indicating if credentials are valid

    Raises:
        HTTPException: If the authentication service is unavailable
    """
    try:
        is_valid, error = await verify_credentials(
            credentials.identifier, credentials.password
        )
        return AuthResponse(is_valid=is_valid, error=error)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Authentication service unavailable",
        ) from e
