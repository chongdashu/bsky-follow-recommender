"use client";

import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useState } from "react";

/**
 * Login form component that handles BlueSky authentication
 */
export function LoginForm() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const formData = new FormData(event.currentTarget);

    try {
      const response = await api.login({
        identifier: formData.get("identifier") as string,
        password: formData.get("password") as string,
      });

      api.setToken(response.token);
      router.push("/recommendations");
    } catch (err) {
      setError("Failed to login. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card className="w-[400px] mx-auto mt-20">
      <CardHeader className="text-center">
        <h1 className="text-2xl font-bold">Login to BlueSky</h1>
        <p className="text-sm text-muted-foreground">
          Enter your BlueSky credentials to continue
        </p>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="identifier">
              Identifier
            </label>
            <Input
              id="identifier"
              name="identifier"
              type="text"
              required
              placeholder="your.handle.bsky.social"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="password">
              App Password
            </label>
            <Input
              id="password"
              name="password"
              type="password"
              required
              placeholder="Enter your app password"
            />
          </div>
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
