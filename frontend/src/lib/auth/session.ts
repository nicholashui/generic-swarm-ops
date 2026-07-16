import { cookies } from "next/headers";
import { env } from "@/lib/config/env";
import { parseSessionCookieValue, SESSION_COOKIE } from "@/lib/auth/cookies";
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
  const raw = cookieStore.get(SESSION_COOKIE)?.value;
  const parsed = parseSessionCookieValue(raw);
  if (!parsed) return null;

  return {
    id: parsed.id,
    organization_id: parsed.organization_id,
    email: parsed.email,
    name: parsed.name,
    role: (parsed.role as AppRole) || "viewer",
  };
}

export function sessionCookieValue(user: SessionUser): string {
  return JSON.stringify(user);
}
