import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { BlueskyProfile } from "@/types";

interface ProfileCardProps {
  profile: BlueskyProfile;
  size?: "sm" | "lg";
}

/**
 * A card component that displays a Bluesky user's profile information
 */
export function ProfileCard({ profile, size = "sm" }: ProfileCardProps) {
  return (
    <Card className={`${size === "lg" ? "max-w-2xl" : "max-w-sm"} w-full`}>
      <CardHeader className="flex flex-row items-center gap-4">
        <Avatar className={size === "lg" ? "h-20 w-20" : "h-12 w-12"}>
          <AvatarImage src={profile.avatar} alt={profile.displayName} />
          <AvatarFallback>{profile.displayName[0]}</AvatarFallback>
        </Avatar>
        <div className="flex flex-col">
          <h3 className="font-semibold">{profile.displayName}</h3>
          <p className="text-sm text-muted-foreground">@{profile.handle}</p>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{profile.description}</p>
        <div className="mt-4 flex gap-4 text-sm">
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
