"""Basic recommendation service using Blue Sky's built-in suggestions."""

from atproto import Client, models as bsky_models

from app.core.logger import setup_logger
from app.services.recommenders.base import BaseRecommender


logger = setup_logger(__name__)


class BasicRecommender(BaseRecommender):
    """Basic recommendation strategy using Blue Sky's built-in suggestions."""

    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileViewDetailed]:
        """Get recommended accounts using Blue Sky's suggestion API.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileViewDetailed objects representing recommended accounts
        """
        try:
            suggestions = client.app.bsky.actor.get_suggestions({"limit": 50}).actors
            # Convert suggestions to detailed profiles
            detailed_profiles = []
            for actor in suggestions:
                try:
                    profile = client.app.bsky.actor.get_profile({"actor": actor.did})
                    detailed_profiles.append(profile)
                except Exception as e:
                    logger.warning(f"Failed to fetch profile for {actor.did}: {e!s}")
                    continue
            return detailed_profiles
        except Exception as e:
            logger.error(f"Failed to get suggestions: {e!s}")
            return []
