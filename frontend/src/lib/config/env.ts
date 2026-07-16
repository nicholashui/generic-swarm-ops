/** Absolute backend base for server-side fetches (RSC, route handlers). */
export function backendApiBaseUrl(): string {
  return (
    process.env.GENERIC_SWARM_BACKEND_API_BASE ||
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    "http://127.0.0.1:8000/api/v1"
  );
}

/**
 * Browser-facing API base.
 * Default is same-origin proxy so httpOnly access tokens never need to be JS-readable.
 * Override with NEXT_PUBLIC_BROWSER_API_BASE (e.g. direct backend URL for special cases).
 */
export function browserApiBaseUrl(): string {
  return process.env.NEXT_PUBLIC_BROWSER_API_BASE || "/api/proxy";
}

export function resolveApiBaseUrl(): string {
  if (typeof window === "undefined") {
    return backendApiBaseUrl();
  }
  return browserApiBaseUrl();
}

export const env = {
  appName: process.env.NEXT_PUBLIC_APP_NAME || "Generic Swarm Ops",
  appEnv: process.env.NEXT_PUBLIC_APP_ENV || "development",
  /** Prefer resolveApiBaseUrl() at call sites; kept for display / legacy. */
  get apiBaseUrl() {
    return resolveApiBaseUrl();
  },
  backendApiBaseUrl: backendApiBaseUrl(),
  enableRegistration: process.env.NEXT_PUBLIC_ENABLE_REGISTRATION !== "false",
  enableBilling: process.env.NEXT_PUBLIC_ENABLE_BILLING !== "false",
  enableSso: process.env.NEXT_PUBLIC_ENABLE_SSO === "true",
  // Opt-in only: real backend is the default product path (recommend, special-skills, etc.).
  demoMode: process.env.NEXT_PUBLIC_DEMO_MODE === "true",
};
