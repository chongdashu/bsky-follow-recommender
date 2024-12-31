import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { UserProfile } from "@/types";

interface FollowCardProps {
  user: UserProfile;
  selectable?: boolean;
  selected?: boolean;
  onSelect?: (did: string) => void;
}

/**
 * Card component to display user profile information
 */
export function FollowCard({
  user,
  selectable = false,
  selected = false,
  onSelect,
}: FollowCardProps) {
  return (
    <Card className={`relative ${selected ? "ring-2 ring-primary" : ""}`}>
      {selectable && (
        <div className="absolute top-2 right-2">
          <Checkbox
            checked={selected}
            onCheckedChange={() => onSelect?.(user.did)}
          />
        </div>
      )}
      <CardHeader className="flex flex-row items-center gap-4">
        <Avatar className="h-12 w-12">
          <AvatarImage
            src={user.avatar}
            alt={user.displayName || user.handle}
          />
          <AvatarFallback>
            {(user.displayName || user.handle).substring(0, 2).toUpperCase()}
          </AvatarFallback>
        </Avatar>
        <div>
          <h3 className="font-semibold">{user.displayName || user.handle}</h3>
          <p className="text-sm text-muted-foreground">@{user.handle}</p>
        </div>
      </CardHeader>
      {user.description && (
        <CardContent>
          <p className="text-sm">{user.description}</p>
          <div className="mt-2 flex gap-4 text-sm text-muted-foreground">
            <span>{user.followersCount || 0} followers</span>
            <span>{user.followingCount || 0} following</span>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
