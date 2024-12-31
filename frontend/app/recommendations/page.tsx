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
  const router = useRouter();
  const { toast } = useToast();

  useEffect(() => {
    async function loadProfile() {
      try {
        const userProfile = await api.getCurrentProfile();
        setProfile(userProfile);
      } catch (error) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to load profile. Please try logging in again.",
        });
        // Redirect to login if unauthorized
        router.push("/login");
      } finally {
        setLoading(false);
      }
    }

    loadProfile();
  }, [router, toast]);

  if (loading) {
    return <div className="container mx-auto py-8">Loading...</div>;
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
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {follows.map((follow) => (
            <ProfileCard key={follow.did} profile={follow} />
          ))}
        </div>
      </div>
    </div>
  );
}
