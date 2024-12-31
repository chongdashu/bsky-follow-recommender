"use client";

import { FollowCard } from "@/components/recommendations/follow-card";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { UserProfile } from "@/types";
import { useState } from "react";

export default function RecommendationsPage() {
  const [existingFollows, setExistingFollows] = useState<UserProfile[]>([]);
  const [recommendations, setRecommendations] = useState<UserProfile[]>([]);
  const [selectedUsers, setSelectedUsers] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);

  async function handleGetRecommendations() {
    setLoading(true);
    try {
      const response = await api.getRecommendations(Array.from(selectedUsers));
      setRecommendations(response.recommendations);
    } catch (error) {
      console.error("Failed to fetch recommendations:", error);
    } finally {
      setLoading(false);
    }
  }

  function handleUserSelect(did: string) {
    setSelectedUsers((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(did)) {
        newSet.delete(did);
      } else {
        newSet.add(did);
      }
      return newSet;
    });
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-8">Find People to Follow</h1>

      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Select People You Follow</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {existingFollows.map((user) => (
            <FollowCard
              key={user.did}
              user={user}
              selectable
              selected={selectedUsers.has(user.did)}
              onSelect={handleUserSelect}
            />
          ))}
        </div>
        <Button
          className="mt-4"
          onClick={handleGetRecommendations}
          disabled={loading || selectedUsers.size === 0}
        >
          {loading ? "Getting Recommendations..." : "Get Recommendations"}
        </Button>
      </section>

      {recommendations.length > 0 && (
        <section>
          <h2 className="text-xl font-semibold mb-4">Recommended Follows</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommendations.map((user) => (
              <FollowCard key={user.did} user={user} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
