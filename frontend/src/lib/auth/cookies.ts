/** Shared auth cookie names — used by middleware, session, API client, and route handlers. */

export const ACCESS_TOKEN_COOKIE = "gso_access_token";
export const SESSION_COOKIE = "frontend_session";

/** 12 hours — long enough for local ops sessions. */
export const AUTH_COOKIE_MAX_AGE_SEC = 60 * 60 * 12;

export type SessionCookieUser = {
  id: string;
  organization_id: string;
  email: string;
  name: string;
  role: string;
};

export function toSessionCookieUser(user: Record<string, unknown>, fallbackEmail = ""): SessionCookieUser {
  return {
    id: String(user.id || "user"),
    organization_id: String(user.organization_id || "org_default"),
    email: String(user.email || fallbackEmail),
    name: String(user.name || user.email || fallbackEmail || "User"),
    role: String(user.role || "viewer"),
  };
}

/** Parse session cookie whether Next already decoded it or it is still percent-encoded. */
export function parseSessionCookieValue(raw: string | undefined | null): SessionCookieUser | null {
  if (!raw) return null;
  const candidates = [raw];
  try {
    const decoded = decodeURIComponent(raw);
    if (decoded !== raw) candidates.push(decoded);
  } catch {
    // ignore bad encoding
  }
  for (const candidate of candidates) {
    try {
      const parsed = JSON.parse(candidate) as Record<string, unknown>;
      if (parsed && typeof parsed === "object" && parsed.email) {
        return toSessionCookieUser(parsed, String(parsed.email));
      }
    } catch {
      // try next candidate
    }
  }
  return null;
}
