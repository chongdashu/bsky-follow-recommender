"use client";

import { ProfileCard } from "@/components/recommendations/profile-card";
import { Separator } from "@/components/ui/separator";
import { BlueskyProfile } from "@/types";
import { useEffect, useState } from "react";

export default function RecommendationsPage() {
  const [profile, setProfile] = useState<BlueskyProfile | null>(null);
  const [follows, setFollows] = useState<BlueskyProfile[]>([]);

  useEffect(() => {
    // TODO: Replace with actual API calls
    setProfile({
      did: "did:plc:123",
      handle: "alice.bsky.social",
      displayName: "Alice",
      description: "Just a girl in a Bluesky world",
      avatar: "https://example.com/avatar.jpg",
      followersCount: 1234,
      followsCount: 567,
      postsCount: 890,
    });

    setFollows([
      {
        did: "did:plc:456",
        handle: "bob.bsky.social",
        displayName: "Bob",
        description: "Software developer and coffee enthusiast",
        avatar: "https://example.com/bob-avatar.jpg",
        followersCount: 2345,
        followsCount: 678,
        postsCount: 901,
      },
      {
        did: "did:plc:789",
        handle: "carol.bsky.social",
        displayName: "Carol",
        description: "Digital artist • Photography • Design",
        avatar: "https://example.com/carol-avatar.jpg",
        followersCount: 3456,
        followsCount: 789,
        postsCount: 912,
      },
      {
        did: "did:plc:012",
        handle: "dave.bsky.social",
        displayName: "Dave",
        description: "Tech writer and blockchain enthusiast",
        avatar: null,
        followersCount: 4567,
        followsCount: 890,
        postsCount: 923,
      },
    ]);
  }, []);

  if (!profile) return null;

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8">
        <h2 className="mb-4 text-2xl font-bold">Your Profile</h2>
        <ProfileCard profile={profile} size="lg" />
      </div>

      <Separator className="my-8" />

      <div>
        <h2 className="mb-4 text-2xl font-bold">People You Follow</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {follows.map((follow) => (
            <ProfileCard key={follow.did} profile={follow} />
          ))}
        </div>
      </div>
    </div>
  );
}
