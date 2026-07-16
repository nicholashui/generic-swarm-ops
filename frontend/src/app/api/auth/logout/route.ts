import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { ACCESS_TOKEN_COOKIE } from "@/lib/auth/cookies";
import { clearAuthCookies, resolveCookieSecure } from "@/lib/auth/session-cookies";
import { backendApiBaseUrl } from "@/lib/config/env";

/**
 * Sign-out: revoke token on backend when possible, then clear session cookies.
 */
export async function POST(request: Request) {
  const cookieStore = await cookies();
  const token = cookieStore.get(ACCESS_TOKEN_COOKIE)?.value;

  if (token) {
    try {
      await fetch(`${backendApiBaseUrl()}/auth/logout`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: "application/json",
        },
        cache: "no-store",
      });
    } catch {
      // Still clear local cookies even if backend is down.
    }
  }

  const response = NextResponse.json({ ok: true });
  // Match Secure flag from the request so browsers clear the same cookie jar entry.
  clearAuthCookies(response, { secure: resolveCookieSecure(request.url) });
  return response;
}
