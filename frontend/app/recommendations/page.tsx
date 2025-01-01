"use client";

import { ProfileCard } from "@/components/recommendations/profile-card";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { api } from "@/lib/api";
import { BlueskyProfile } from "@/types";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function RecommendationsPage() {
  const [profile, setProfile] = useState<BlueskyProfile | null>(null);
  const [follows, setFollows] = useState<BlueskyProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { toast } = useToast();

  useEffect(() => {
    async function loadData() {
      try {
        setError(null);
        const [userProfile, userFollows] = await Promise.all([
          api.getCurrentProfile(),
          api.getFollows(),
        ]);
        setProfile(userProfile);
        setFollows(userFollows);
      } catch (error) {
        const errorMessage =
          "Failed to load profile. Please try logging in again.";
        setError(errorMessage);
        toast({
          variant: "destructive",
          title: "Error",
          description: errorMessage,
        });
        router.push("/login");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, [router, toast]);

  const handleProfileClick = (handle: string) => {
    window.open(`https://bsky.app/profile/${handle}`, "_blank");
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center text-destructive">{error}</div>
      </div>
    );
  }

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
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 max-h-[600px] overflow-y-auto">
          {follows.map((follow) => (
            <div
              key={follow.did}
              onClick={() => handleProfileClick(follow.handle)}
              className="cursor-pointer transition-transform hover:scale-[1.02]"
            >
              <ProfileCard profile={follow} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
