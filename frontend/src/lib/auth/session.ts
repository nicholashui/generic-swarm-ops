import { cookies } from "next/headers";
import { env } from "@/lib/config/env";
import type { SessionUser } from "@/types/domain";
import type { AppRole } from "@/types/permissions";

const demoUser: SessionUser = {
  id: "user_admin",
  organization_id: "org_default",
  email: "ops@example.com",
  name: "Alex Morgan",
  role: "admin",
};

export async function getSessionUser(): Promise<SessionUser | null> {
  if (env.demoMode) return demoUser;
  const cookieStore = await cookies();
  const raw = cookieStore.get("frontend_session")?.value;
  if (!raw) return null;
  try {
    const parsed = JSON.parse(decodeURIComponent(raw)) as SessionUser;
    if (parsed?.id && parsed?.email) {
      return {
        id: parsed.id,
        organization_id: parsed.organization_id || "org_default",
        email: parsed.email,
        name: parsed.name || parsed.email,
        role: (parsed.role as AppRole) || "viewer",
      };
    }
  } catch {
    // legacy cookie: non-empty means "signed in" with demo-shaped user for compatibility
    return {
      ...demoUser,
      email: "admin@example.com",
      name: "Admin",
    };
  }
  return null;
}

export function sessionCookieValue(user: SessionUser): string {
  return encodeURIComponent(JSON.stringify(user));
}
