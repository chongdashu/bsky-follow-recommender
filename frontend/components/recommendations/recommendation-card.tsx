import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { BlueskyProfile } from "@/types";
import { UserPlus, X } from "lucide-react";

interface RecommendationCardProps {
  profile: BlueskyProfile;
  onDismiss: () => void;
  onClick: () => void;
  onFollow: () => void;
  isFollowing?: boolean;
}

/**
 * Card component for displaying recommended profiles in a horizontal scroll
 */
export function RecommendationCard({
  profile,
  onDismiss,
  onClick,
  onFollow,
  isFollowing = false,
}: RecommendationCardProps) {
  const handleDismiss = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDismiss();
  };

  const handleFollow = (e: React.MouseEvent) => {
    e.stopPropagation();
    onFollow();
  };

  return (
    <Card
      className="w-[350px] h-[400px] relative cursor-pointer hover:shadow-md transition-shadow flex flex-col"
      onClick={onClick}
    >
      <Button
        variant="ghost"
        size="icon"
        className="absolute top-2 right-2 h-8 w-8 rounded-full"
        onClick={handleDismiss}
      >
        <X className="h-4 w-4" />
      </Button>
      <CardHeader className="flex flex-row items-center gap-4">
        <Avatar className="h-12 w-12">
          <AvatarImage src={profile.avatar || ""} alt={profile.displayName} />
          <AvatarFallback>
            {(profile.displayName || profile.handle)[0].toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <div className="flex flex-col">
          <h3 className="font-semibold">{profile.displayName}</h3>
          <p className="text-sm text-muted-foreground">@{profile.handle}</p>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col flex-1">
        <div className="grid grid-cols-3 gap-2 text-sm mb-4">
          <div className="text-center">
            <div className="font-semibold">{profile.followersCount}</div>
            <div className="text-muted-foreground text-xs">Followers</div>
          </div>
          <div className="text-center">
            <div className="font-semibold">{profile.followsCount}</div>
            <div className="text-muted-foreground text-xs">Following</div>
          </div>
          <div className="text-center">
            <div className="font-semibold">{profile.postsCount}</div>
            <div className="text-muted-foreground text-xs">Posts</div>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto">
          <p className="text-sm text-muted-foreground whitespace-pre-wrap">
            {profile.description}
          </p>
        </div>
        <div className="pt-4">
          <Button
            className="w-full"
            variant={isFollowing ? "secondary" : "default"}
            onClick={handleFollow}
          >
            <UserPlus className="h-4 w-4 mr-2" />
            {isFollowing ? "Following" : "Follow"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
