"""Module containing different recommendation strategies for Blue Sky users."""

from abc import ABC, abstractmethod
from collections import Counter
from typing import Protocol

from atproto import Client, models as bsky_models


class RecommenderProtocol(Protocol):
    """Protocol defining the interface for recommendation strategies."""

    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileViewDetailed]:
        """Get recommended accounts for a user.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileViewDetailed objects representing recommended accounts
        """
        ...


class BaseRecommender(ABC):
    """Abstract base class for recommendation strategies."""

    @abstractmethod
    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileViewDetailed]:
        """Get recommended accounts for a user.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileViewDetailed objects representing recommended accounts
        """
        pass


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
        suggestions = client.app.bsky.actor.get_suggestions({"limit": 50}).actors
        # Convert suggestions to detailed profiles
        detailed_profiles = []
        for actor in suggestions:
            try:
                profile = client.app.bsky.actor.get_profile({"actor": actor.did})
                detailed_profiles.append(profile)
            except Exception:
                continue
        return detailed_profiles


class CommonFollowersRecommender(BaseRecommender):
    """Recommender that analyzes common followers among seed accounts."""

    def __init__(self, seed_accounts: list[str], min_common_follows: int = 2):
        """Initialize the CommonFollowersRecommender.

        Args:
            seed_accounts: List of handles or DIDs to analyze for common followers
            min_common_follows: Minimum number of seed accounts that must follow a user
                              for them to be recommended
        """
        if len(seed_accounts) < 2:
            raise ValueError("At least 2 seed accounts are required")
        self.seed_accounts = seed_accounts
        self.min_common_follows = min_common_follows

    async def _get_follows(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileView]:
        """Get the list of accounts that an actor follows.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileView objects representing accounts followed by the actor
        """
        cursor = None
        follows = []

        while True:
            response = client.app.bsky.graph.get_follows(
                params={"actor": actor, "limit": 100, "cursor": cursor}
            )
            follows.extend(response.follows)

            if not response.cursor:
                break
            cursor = response.cursor

        return follows

    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileViewDetailed]:
        """Get recommended accounts based on common followers among seed accounts.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID (used to exclude accounts already followed)

        Returns:
            List of ProfileViewDetailed objects representing recommended accounts,
            sorted by number of seed accounts following them
        """
        # Get current user's follows to exclude them from recommendations
        user_follows = {f.did for f in await self._get_follows(client, actor)}

        # Get follows for each seed account
        all_follows = []
        for seed in self.seed_accounts:
            follows = await self._get_follows(client, seed)
            all_follows.extend(follow.did for follow in follows)

        # Count how many seed accounts follow each account
        follow_counts = Counter(all_follows)

        # Filter for accounts followed by minimum number of seed accounts
        # and not already followed by the user
        recommended_dids = {
            did
            for did, count in follow_counts.items()
            if count >= self.min_common_follows and did not in user_follows
        }

        # Fetch detailed profiles for recommended accounts
        recommendations = []
        for did in recommended_dids:
            try:
                profile = client.app.bsky.actor.get_profile(params={"actor": did})
                recommendations.append(profile)
            except Exception:
                continue

        # Sort by number of seed accounts following
        recommendations.sort(key=lambda x: follow_counts[x.did], reverse=True)

        return recommendations
