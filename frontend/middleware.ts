import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

/**
 * Middleware to protect routes that require authentication
 */
export function middleware(request: NextRequest) {
  // Get token from localStorage (client-side only)
  if (request.nextUrl.pathname.startsWith("/recommendations")) {
    // If accessing recommendations without being logged in, redirect to login
    if (!request.cookies.get("auth_token")) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  // If accessing login while already authenticated, redirect to recommendations
  if (request.nextUrl.pathname === "/login") {
    if (request.cookies.get("auth_token")) {
      return NextResponse.redirect(new URL("/recommendations", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/recommendations/:path*", "/login"],
};
