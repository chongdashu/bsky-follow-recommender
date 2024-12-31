/**
 * API client for interacting with the backend services
 */
class ApiClient {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    this.token = null;
  }

  /**
   * Sets the authentication token for subsequent requests
   */
  setToken(token: string): void {
    this.token = token;
    // Store token in cookie for persistence
    document.cookie = `auth_token=${token}; path=/; max-age=86400`; // 24 hours
  }

  /**
   * Clears the authentication token
   */
  clearToken(): void {
    this.token = null;
    document.cookie =
      "auth_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
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
   * Fetches recommendations based on selected seed users
   */
  async getRecommendations(
    seedUserDids: string[]
  ): Promise<RecommendationsResponse> {
    if (!this.token) {
      throw new Error("Not authenticated");
    }

    const response = await fetch(`${this.baseUrl}/v1/recommendations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.token}`,
      },
      body: JSON.stringify({ seed_users: seedUserDids }),
    });

    if (!response.ok) {
      throw new Error("Failed to fetch recommendations");
    }

    return response.json();
  }
}

export const api = new ApiClient();
