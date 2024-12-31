"""Base classes and protocols for recommendation services."""

from abc import ABC, abstractmethod
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
