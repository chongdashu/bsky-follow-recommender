"""Blue Sky authentication utilities for creating and managing API clients."""

from datetime import datetime, timedelta

from atproto import Client
from fastapi import HTTPException, status
from jose import jwt

from app.core.config import get_settings
from app.core.logger import setup_logger
from app.models.auth import AuthResponse, UserProfile


logger = setup_logger(__name__)
settings = get_settings()


class BlueskyAuthManager:
    """Manages Bluesky authentication and client instances."""

    _clients: dict[str, Client] = {}

    @classmethod
    def get_client(cls, did: str) -> Client | None:
        """Get cached client for user DID.

        Args:
            did: User's decentralized identifier

        Returns:
            Cached client instance or None if not found
        """
        return cls._clients.get(did)

    @classmethod
    def store_client(cls, did: str, client: Client) -> None:
        """Store client instance for user DID.

        Args:
            did: User's decentralized identifier
            client: Authenticated client instance
        """
        cls._clients[did] = client

    @classmethod
    def remove_client(cls, did: str) -> None:
        """Remove stored client for user DID.

        Args:
            did: User's decentralized identifier
        """
        cls._clients.pop(did, None)


def create_bluesky_client(login: str, password: str) -> Client:
    """Create an authenticated Blue Sky client.

    Args:s
        login: Blue Sky account identifier (handle or email)
        password: Blue Sky account password

    Returns:
        An authenticated Client instance

    Raises:
        HTTPException: If authentication fails
    """
    try:
        client = Client()
        client.login(login=login, password=password)
        logger.info("Successfully created authenticated Blue Sky client")
        return client
    except Exception as e:
        logger.error(f"Failed to create Blue Sky client: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token.

    Args:
        data: Data to encode in the token

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(identifier: str, password: str) -> AuthResponse:
    """Authenticate user with Blue Sky credentials and return tokens.

    Args:
        identifier: Blue Sky identifier (handle or email)
        password: Blue Sky password

    Returns:
        AuthResponse containing JWT tokens and user profile

    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Create and authenticate client
        client = create_bluesky_client(login=identifier, password=password)

        if not client.me:
            raise ValueError("No authenticated user found")

        # Get full profile info
        profile = client.app.bsky.actor.get_profile({"actor": client.me.did})

        # Store client for later use
        BlueskyAuthManager.store_client(client.me.did, client)

        # Create user profile
        user_profile = UserProfile(
            did=client.me.did,
            handle=profile.handle,
            display_name=profile.display_name,
            avatar_url=profile.avatar,
            following_count=profile.follows_count or -1,
            follower_count=profile.followers_count or -1,
            created_at=datetime.now(),  # Use actual creation date if available
        )

        # Create JWT tokens
        token_data = {"sub": client.me.did}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        # Create auth response with tokens and profile
        return AuthResponse(
            access_jwt=access_token,
            refresh_jwt=refresh_token,
            profile=user_profile,
        )

    except Exception as e:
        logger.error(f"Authentication failed: {e!s}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
