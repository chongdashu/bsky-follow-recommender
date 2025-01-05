"use client";

import { ProfileCard } from "@/components/recommendations/profile-card";
import { RecommendationCard } from "@/components/recommendations/recommendation-card";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { useToast } from "@/hooks/use-toast";
import { api } from "@/lib/api";
import { BlueskyProfile } from "@/types";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function RecommendationsPage() {
  const [profile, setProfile] = useState<BlueskyProfile | null>(null);
  const [follows, setFollows] = useState<BlueskyProfile[]>([]);
  const [recommendations, setRecommendations] = useState<BlueskyProfile[]>([]);
  const [selectedSeeds, setSelectedSeeds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [fetchingRecommendations, setFetchingRecommendations] = useState(false);
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

  const handleSeedToggle = (handle: string) => {
    setSelectedSeeds((prev) => {
      const newSeeds = new Set(prev);
      if (newSeeds.has(handle)) {
        newSeeds.delete(handle);
      } else {
        newSeeds.add(handle);
      }
      return newSeeds;
    });
  };

  const handleGetRecommendations = async () => {
    if (selectedSeeds.size < 2) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Please select at least 2 accounts as seeds",
      });
      return;
    }

    setFetchingRecommendations(true);
    try {
      const recommendations = await api.getRecommendations(
        Array.from(selectedSeeds)
      );
      setRecommendations(recommendations);
      toast({
        title: "Success",
        description: `Found ${recommendations.length} recommendations`,
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch recommendations",
      });
    } finally {
      setFetchingRecommendations(false);
    }
  };

  const handleDismissRecommendation = (did: string) => {
    setRecommendations((prev) => prev.filter((rec) => rec.did !== did));
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

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Recommended Accounts</h2>
        {recommendations.length === 0 ? (
          <Card className="bg-muted">
            <CardContent className="py-8">
              <div className="text-center">
                <h3 className="font-semibold mb-2">No Recommendations Yet</h3>
                <p className="text-sm text-muted-foreground">
                  Select at least 2 seed accounts below to get personalized
                  recommendations
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="relative">
            <ScrollArea className="w-full whitespace-nowrap rounded-md border">
              <div className="flex w-max space-x-4 p-4">
                {recommendations.map((recommendation) => (
                  <RecommendationCard
                    key={recommendation.did}
                    profile={recommendation}
                    onDismiss={() =>
                      handleDismissRecommendation(recommendation.did)
                    }
                    onClick={() => handleProfileClick(recommendation.handle)}
                  />
                ))}
              </div>
              <ScrollBar orientation="horizontal" />
            </ScrollArea>
          </div>
        )}
      </div>

      <Separator className="my-8" />

      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold">Select Seed Accounts</h2>
          <Button
            onClick={handleGetRecommendations}
            disabled={selectedSeeds.size < 2 || fetchingRecommendations}
          >
            {fetchingRecommendations ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-foreground mr-2" />
                Getting Recommendations...
              </>
            ) : (
              "Get Recommendations"
            )}
          </Button>
        </div>
        <p className="text-sm text-muted-foreground mb-4">
          Select at least 2 accounts you follow to find similar accounts
        </p>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 max-h-[600px] overflow-y-auto">
          {follows.map((follow) => (
            <ProfileCard
              key={follow.did}
              profile={follow}
              selectable
              selected={selectedSeeds.has(follow.handle)}
              onSelect={() => handleSeedToggle(follow.handle)}
              onClick={() => handleProfileClick(follow.handle)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
