/**
 * Authentication related types
 */
export interface LoginCredentials {
  identifier: string; // BlueSky identifier
  password: string; // BlueSky app password
}

export interface LoginResponse {
  access_jwt: string;
  refresh_jwt: string;
  profile: {
    did: string;
    handle: string;
    displayName?: string;
    avatar?: string;
  };
}

/**
 * User profile related types
 */
export interface UserProfile {
  did: string;
  handle: string;
  displayName: string;
  description: string | null;
  avatar: string | null;
  followersCount: number;
  followsCount: number;
  postsCount: number;
}

/**
 * Recommendation related types
 */
export interface RecommendationsResponse {
  recommendations: BlueskyProfile[];
}

export interface BlueskyProfile {
  did: string;
  handle: string;
  displayName: string;
  description: string | null;
  avatar: string | null;
  followersCount: number;
  followsCount: number;
  postsCount: number;
}
