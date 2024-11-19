from atproto import Client, models
from typing import List, Dict, Any
from ...core.config import get_settings
from ...core.exceptions import BlueskyAuthError, BlueskyAPIError
from ...models.schemas.responses import UserProfile


class BlueskyClient:
    """
    Client for interacting with the Bluesky (ATProto) API.
    """

    def __init__(self):
        """Initialize the Bluesky client."""
        self.settings = get_settings()
        self.client = Client()
        self._session: Dict[str, Any] | None = None

    async def connect(self) -> None:
        """
        Connects to Bluesky and creates a session.

        Raises:
            BlueskyAuthError: If authentication fails
            BlueskyAPIError: If connection fails
        """
        try:
            self._session = await self.client.login(
                self.settings.BLUESKY_IDENTIFIER, self.settings.BLUESKY_PASSWORD
            )
        except Exception as e:
            if "authentication" in str(e).lower():
                raise BlueskyAuthError()
            raise BlueskyAPIError(f"Failed to connect: {str(e)}")

    async def get_user_suggestions(self, limit: int = 10) -> List[UserProfile]:
        """
        Gets user suggestions based on the authenticated user's network.

        Args:
            limit: Maximum number of suggestions to return

        Returns:
            List[UserProfile]: List of suggested users with their profiles

        Raises:
            BlueskyAPIError: If fetching suggestions fails
        """
        if not self._session:
            await self.connect()

        try:
            suggestions = await self.client.get_suggested_follows(limit=limit)

            return [
                UserProfile(
                    did=user.did,
                    handle=user.handle,
                    display_name=user.display_name,
                    description=user.description,
                    avatar=user.avatar,
                    followers_count=user.followers_count,
                    following_count=user.following_count,
                )
                for user in suggestions
            ]
        except Exception as e:
            raise BlueskyAPIError(f"Failed to get suggestions: {str(e)}")
