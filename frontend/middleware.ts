import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

/**
 * Middleware to protect routes that require authentication
 */
export function middleware(request: NextRequest) {
  const authToken = request.cookies.get("auth_token");

  // If accessing recommendations without being logged in, redirect to login
  if (request.nextUrl.pathname.startsWith("/recommendations")) {
    if (!authToken?.value) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  // If accessing login while already authenticated, redirect to recommendations
  if (request.nextUrl.pathname === "/login") {
    if (authToken?.value) {
      return NextResponse.redirect(new URL("/recommendations", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/recommendations/:path*", "/login"],
};
