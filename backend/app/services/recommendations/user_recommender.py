from typing import list
from app.models.schemas.responses import UserProfile, RecommendationResponse
from app.services.bluesky.client import BlueskyClient


class UserRecommender:
    """
    Service for generating user recommendations based on various signals.
    """

    def __init__(self, client: BlueskyClient):
        """
        Initialize the recommender with a Bluesky client.

        Args:
            client: Initialized BlueskyClient instance
        """
        self.client = client

    async def get_recommendations(
        self, limit: int = 10
    ) -> list[RecommendationResponse]:
        """
        Generate user recommendations based on multiple signals.

        Args:
            limit: Maximum number of recommendations to return

        Returns:
            list[RecommendationResponse]: List of recommended users with scores and reasons

        Raises:
            BlueskyAPIError: If fetching user data fails
        """
        # Get suggested users from Bluesky
        users = await self.client.get_user_suggestions(
            limit=limit * 2
        )  # Get more users than needed for filtering

        # Score and rank users based on multiple factors
        scored_users = []
        for user in users:
            score = self._calculate_user_score(user)
            reason = self._generate_recommendation_reason(user, score)

            scored_users.append((user, score, reason))

        # Sort by score and take top N
        scored_users.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = scored_users[:limit]

        # Convert to recommendation responses
        return [
            RecommendationResponse(user=user, score=score, reason=reason)
            for user, score, reason in top_recommendations
        ]

    def _calculate_user_score(self, user: UserProfile) -> float:
        """
        Calculate a recommendation score for a user based on various factors.

        Args:
            user: User profile to score

        Returns:
            float: Recommendation score between 0 and 1
        """
        # Initialize base score
        score = 0.0

        # Factor 1: Engagement ratio (followers to following ratio)
        if user.following_count > 0:
            engagement_ratio = user.followers_count / user.following_count
            engagement_score = min(engagement_ratio / 3.0, 1.0)  # Cap at 1.0
            score += engagement_score * 0.4  # 40% weight

        # Factor 2: Profile completeness
        profile_score = 0.0
        if user.display_name:
            profile_score += 0.3
        if user.description:
            profile_score += 0.4
        if user.avatar:
            profile_score += 0.3
        score += profile_score * 0.3  # 30% weight

        # Factor 3: Activity level (using followers as a proxy)
        activity_score = min(user.followers_count / 1000.0, 1.0)  # Cap at 1.0
        score += activity_score * 0.3  # 30% weight

        return score

    def _generate_recommendation_reason(self, user: UserProfile, score: float) -> str:
        """
        Generate a human-readable reason for the recommendation.

        Args:
            user: User profile
            score: Calculated recommendation score

        Returns:
            str: Recommendation reason
        """
        reasons = []

        if user.followers_count > 1000:
            reasons.append("popular in the community")

        if user.description and len(user.description) > 50:
            reasons.append("active content creator")

        if user.followers_count > user.following_count * 2:
            reasons.append("highly engaged")

        if not reasons:
            reasons.append("matches your interests")

        return "This user is " + " and ".join(reasons)
