"""Router for Blue Sky authentication endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.bluesky.auth import authenticate_user
from app.models.user import AuthResponse, UserAuth


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse)
async def login(credentials: UserAuth) -> AuthResponse:
    """
    Authenticate user with Blue Sky credentials and return tokens

    Args:
        credentials: User authentication credentials

    Returns:
        AuthResponse containing JWT tokens and user profile

    Raises:
        HTTPException: If authentication fails
    """
    try:
        auth_data = await authenticate_user(
            identifier=credentials.identifier,
            password=credentials.password,
        )
        return auth_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
