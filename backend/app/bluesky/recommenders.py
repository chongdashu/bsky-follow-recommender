"""Module containing different recommendation strategies for Blue Sky users."""

from abc import ABC, abstractmethod
from typing import Protocol

from atproto import Client, models as bsky_models


class RecommenderProtocol(Protocol):
    """Protocol defining the interface for recommendation strategies."""

    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileView]:
        """Get recommended accounts for a user.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileView objects representing recommended accounts
        """
        ...


class BaseRecommender(ABC):
    """Abstract base class for recommendation strategies."""

    @abstractmethod
    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileView]:
        """Get recommended accounts for a user.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileView objects representing recommended accounts
        """
        pass


class BasicRecommender(BaseRecommender):
    """Basic recommendation strategy using Blue Sky's built-in suggestions."""

    async def get_recommendations(
        self, client: Client, actor: str
    ) -> list[bsky_models.AppBskyActorDefs.ProfileView]:
        """Get recommended accounts using Blue Sky's suggestion API.

        Args:
            client: Authenticated Blue Sky client
            actor: The user's handle or DID

        Returns:
            List of ProfileView objects representing recommended accounts
        """
        return client.app.bsky.actor.get_suggestions({"limit": 50}).actors
