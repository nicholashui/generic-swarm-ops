import type { NextResponse } from "next/server";
import {
  ACCESS_TOKEN_COOKIE,
  AUTH_COOKIE_MAX_AGE_SEC,
  SESSION_COOKIE,
  type SessionCookieUser,
} from "@/lib/auth/cookies";

export type CookieSecureMode = {
  /**
   * Only set Secure when the browser is actually on HTTPS.
   * Forcing Secure under next start (NODE_ENV=production) on http://127.0.0.1
   * makes browsers drop cookies → login every time.
   */
  secure?: boolean;
};

/** Prefer request URL protocol; allow AUTH_COOKIE_SECURE=true|false override. */
export function resolveCookieSecure(requestUrl?: string): boolean {
  const forced = process.env.AUTH_COOKIE_SECURE?.toLowerCase();
  if (forced === "true") return true;
  if (forced === "false") return false;
  if (requestUrl) {
    try {
      return new URL(requestUrl).protocol === "https:";
    } catch {
      // fall through
    }
  }
  return false;
}

const baseCookie = (secure: boolean) => ({
  path: "/",
  sameSite: "lax" as const,
  maxAge: AUTH_COOKIE_MAX_AGE_SEC,
  secure,
});

/** Attach httpOnly bearer + session cookies after login / accept-invite. */
export function applyAuthCookies(
  response: NextResponse,
  accessToken: string,
  sessionUser: SessionCookieUser,
  options: CookieSecureMode = {},
): void {
  const secure = options.secure ?? false;
  const base = baseCookie(secure);

  response.cookies.set(ACCESS_TOKEN_COOKIE, accessToken, {
    ...base,
    httpOnly: true,
  });
  response.cookies.set(SESSION_COOKIE, JSON.stringify(sessionUser), {
    ...base,
    // Readable by middleware + optional client display helpers (not the bearer secret).
    httpOnly: false,
  });
}

/** Clear both auth cookies (logout). Match Secure flag so the browser actually clears them. */
export function clearAuthCookies(
  response: NextResponse,
  options: CookieSecureMode = {},
): void {
  const secure = options.secure ?? false;
  response.cookies.set(ACCESS_TOKEN_COOKIE, "", {
    path: "/",
    maxAge: 0,
    httpOnly: true,
    sameSite: "lax",
    secure,
  });
  response.cookies.set(SESSION_COOKIE, "", {
    path: "/",
    maxAge: 0,
    httpOnly: false,
    sameSite: "lax",
    secure,
  });
}
