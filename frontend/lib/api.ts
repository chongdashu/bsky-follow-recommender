/**
 * API client for interacting with the backend services
 */
class ApiClient {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    this.token = this.getTokenFromCookie();
  }

  /**
   * Gets the authentication token from cookies
   */
  private getTokenFromCookie(): string | null {
    if (typeof document === "undefined") return null; // Guard for SSR
    const cookies = document.cookie.split(";");
    const tokenCookie = cookies.find((cookie) =>
      cookie.trim().startsWith("auth_token=")
    );
    return tokenCookie ? tokenCookie.split("=")[1] : null;
  }

  /**
   * Sets the authentication token for subsequent requests
   */
  setToken(token: string): void {
    this.token = token;
    document.cookie = `auth_token=${token}; path=/; max-age=86400; SameSite=Strict`;
  }

  /**
   * Clears the authentication token
   */
  clearToken(): void {
    this.token = null;
    // Properly clear the cookie by setting an expired date
    document.cookie =
      "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Strict";
    // Force reload to trigger middleware
    window.location.href = "/login";
  }

  /**
   * Authenticates a user with their Blue Sky credentials
   */
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    return response.json();
  }

  /**
   * Get recommended accounts based on selected seed accounts
   */
  async getRecommendations(seedHandles: string[]): Promise<BlueskyProfile[]> {
    if (!this.token) {
      throw new Error("Not authenticated");
    }

    const response = await fetch(`${this.baseUrl}/recommendations`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ seed_handles: seedHandles }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch recommendations");
    }

    const data = await response.json();
    return data.recommendations;
  }

  /**
   * Fetches the current user's profile
   */
  async getCurrentProfile(): Promise<BlueskyProfile> {
    if (!this.token) {
      throw new Error("Not authenticated");
    }

    const response = await fetch(`${this.baseUrl}/v1/profile`, {
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch profile");
    }

    return response.json();
  }

  /**
   * Fetches the list of accounts the current user follows
   */
  async getFollows(): Promise<BlueskyProfile[]> {
    if (!this.token) {
      throw new Error("Not authenticated");
    }

    const response = await fetch(`${this.baseUrl}/v1/follows`, {
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch follows");
    }

    return response.json();
  }
}

export const api = new ApiClient();
