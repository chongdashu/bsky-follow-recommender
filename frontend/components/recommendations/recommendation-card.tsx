import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { BlueskyProfile } from "@/types";
import { X } from "lucide-react";

interface RecommendationCardProps {
  profile: BlueskyProfile;
  onDismiss: () => void;
  onClick: () => void;
}

/**
 * Card component for displaying recommended profiles in a horizontal scroll
 */
export function RecommendationCard({
  profile,
  onDismiss,
  onClick,
}: RecommendationCardProps) {
  const handleDismiss = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDismiss();
  };

  return (
    <Card
      className="w-[300px] relative cursor-pointer hover:shadow-md transition-shadow"
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
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
          {profile.description}
        </p>
        <div className="flex gap-4 text-sm">
          <div>
            <span className="font-semibold">{profile.followersCount}</span>
            <span className="ml-1 text-muted-foreground">Followers</span>
          </div>
          <div>
            <span className="font-semibold">{profile.followsCount}</span>
            <span className="ml-1 text-muted-foreground">Following</span>
          </div>
          <div>
            <span className="font-semibold">{profile.postsCount}</span>
            <span className="ml-1 text-muted-foreground">Posts</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
