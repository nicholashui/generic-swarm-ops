import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { ACCESS_TOKEN_COOKIE, SESSION_COOKIE } from "@/lib/auth/cookies";

export function middleware(request: NextRequest) {
  // Demo is opt-in; default product path requires a live session + API token for /app.
  if (process.env.NEXT_PUBLIC_DEMO_MODE === "true") return NextResponse.next();
  if (!request.nextUrl.pathname.startsWith("/app")) return NextResponse.next();

  const hasSession = Boolean(request.cookies.get(SESSION_COOKIE)?.value);
  const hasToken = Boolean(request.cookies.get(ACCESS_TOKEN_COOKIE)?.value);
  if (!hasSession || !hasToken) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("next", request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}

export const config = { matcher: ["/app/:path*"] };
