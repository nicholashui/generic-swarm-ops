import {
  ACCESS_TOKEN_COOKIE,
  AUTH_COOKIE_MAX_AGE_SEC,
  SESSION_COOKIE,
  toSessionCookieUser,
} from "@/lib/auth/cookies";
import { resolveApiBaseUrl } from "@/lib/config/env";
import { AppError } from "@/lib/errors/app-error";

const TOKEN_COOKIE = ACCESS_TOKEN_COOKIE;
let accessToken: string | null = null;

function readBrowserCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  if (!match) return null;
  try {
    return decodeURIComponent(match[1]);
  } catch {
    return match[1];
  }
}

function writeBrowserCookie(name: string, value: string | null, httpOnlyNote = false) {
  // Browser JS cannot set httpOnly; only used for non-secret session display cookie.
  if (typeof document === "undefined" || httpOnlyNote) return;
  if (value) {
    document.cookie = `${name}=${encodeURIComponent(value)}; path=/; max-age=${AUTH_COOKIE_MAX_AGE_SEC}; SameSite=Lax`;
  } else {
    document.cookie = `${name}=; path=/; Max-Age=0; SameSite=Lax`;
  }
}

/**
 * Memory-only access token for rare client cases.
 * Prefer httpOnly cookie + /api/proxy; do not mirror bearer into document.cookie.
 */
export function setAccessToken(token: string | null) {
  accessToken = token;
  if (typeof window !== "undefined") {
    if (token) window.sessionStorage.setItem(TOKEN_COOKIE, token);
    else window.sessionStorage.removeItem(TOKEN_COOKIE);
  }
}

/** Persist non-secret session user for middleware / shell (not the bearer token). */
export function setFrontendSessionUser(user: Record<string, unknown>) {
  const session = toSessionCookieUser(user);
  writeBrowserCookie(SESSION_COOKIE, JSON.stringify(session));
}

export function clearClientSession() {
  accessToken = null;
  writeBrowserCookie(SESSION_COOKIE, null);
  writeBrowserCookie(TOKEN_COOKIE, null);
  if (typeof window !== "undefined") {
    window.sessionStorage.removeItem(TOKEN_COOKIE);
  }
}

export function getAccessToken(): string | null {
  if (accessToken) return accessToken;
  // httpOnly token is not readable in the browser — rely on /api/proxy.
  if (typeof window !== "undefined") {
    return window.sessionStorage.getItem(TOKEN_COOKIE);
  }
  return null;
}

/** Server Components / RSC: read token from request cookies (httpOnly OK). */
export async function getServerAccessToken(): Promise<string | null> {
  try {
    const { cookies } = await import("next/headers");
    const store = await cookies();
    return store.get(TOKEN_COOKIE)?.value ?? null;
  } catch {
    return getAccessToken();
  }
}

export async function resolveAccessToken(): Promise<string | null> {
  if (typeof window === "undefined") {
    return getServerAccessToken();
  }
  // Browser uses cookie via proxy; Authorization header optional.
  return getAccessToken();
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await resolveAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  // Server-side: attach bearer for direct backend calls.
  // Browser-side via /api/proxy: cookie carries auth; still pass memory token if present.
  if (token) headers.Authorization = `Bearer ${token}`;

  const base = resolveApiBaseUrl().replace(/\/$/, "");
  const response = await fetch(`${base}${path.startsWith("/") ? path : `/${path}`}`, {
    credentials: "same-origin",
    cache: "no-store",
    ...options,
    headers,
  });
  const headerRequestId = response.headers.get("X-Request-ID") || response.headers.get("x-request-id") || undefined;
  if (!response.ok) {
    const payload = (await response.json().catch(() => ({
      error: { message: response.statusText, code: "unknown" },
      meta: {},
    }))) as {
      error?: { message?: string; code?: string; details?: unknown };
      meta?: { request_id?: string };
      detail?: string | Array<{ msg?: string }>;
    };
    const bodyRequestId = payload.meta?.request_id;
    const requestId = headerRequestId || bodyRequestId;
    let message = payload.error?.message || response.statusText;
    if (!payload.error?.message && Array.isArray(payload.detail)) {
      message = payload.detail.map((d) => d.msg || "validation error").join("; ");
    } else if (!payload.error?.message && typeof payload.detail === "string") {
      message = payload.detail;
    }
    throw new AppError(message || response.statusText, response.status, requestId, payload.error?.code);
  }
  return response.json() as Promise<T>;
}

/** Same-origin logout BFF — clears cookies + revokes backend token. */
export async function logoutViaBff(): Promise<void> {
  clearClientSession();
  const response = await fetch("/api/auth/logout", {
    method: "POST",
    credentials: "same-origin",
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new AppError("Logout failed", response.status);
  }
}

export const backendApi = {
  login: (email: string, password: string) =>
    request<{ access_token: string; refresh_token?: string; user: Record<string, unknown> }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: () => request("/auth/me"),
  metrics: () => request("/health/metrics"),
  health: () => request("/health"),
  listAgents: () => request("/agents"),
  /** SPEC.md (or README) from business/<domain>/agents/<id>/ */
  getAgentSpec: (agentId: string) =>
    request<{
      agent_id: string;
      domain_id: string;
      name: string;
      path: string;
      markdown: string;
    }>(`/agents/${encodeURIComponent(agentId)}/spec`),
  listTools: () => request("/tools"),
  listWorkflows: () => request("/workflows"),
  listWorkflowRuns: () => request("/workflow-runs"),
  listApprovals: () => request("/approvals"),
  listKnowledge: () => request("/knowledge"),
  listMemory: () => request("/memory"),
  listEvaluations: () => request("/evaluations"),
  processSummary: () => request("/processes/summary"),
  listAuditLogs: () => request("/audit-logs"),
  listApiKeys: () => request("/auth/api-keys"),
  listUsers: () => request("/users"),
  updateUser: (userId: string, payload: { name?: string; role?: string; department?: string; status?: string }) =>
    request(`/users/${encodeURIComponent(userId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  listInvitations: () => request("/users/invitations"),
  createInvitation: (payload: { email: string; name?: string; role?: string; department?: string }) =>
    request("/users/invitations", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  acceptInvitation: (payload: { token: string; password: string; name?: string }) =>
    request<{
      access_token?: string;
      refresh_token?: string;
      user?: Record<string, unknown>;
      [key: string]: unknown;
    }>("/users/invitations/accept", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  listOrganizations: () => request("/organizations"),
  getOrganization: (organizationId: string) =>
    request(`/organizations/${encodeURIComponent(organizationId)}`),
  updateOrganization: (organizationId: string, payload: { name?: string; slug?: string; status?: string }) =>
    request(`/organizations/${encodeURIComponent(organizationId)}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  decideApproval: (approvalId: string, decision: "approved" | "rejected", reason?: string) =>
    request(`/approvals/${approvalId}/decision`, {
      method: "POST",
      body: JSON.stringify({ decision, reason: reason || decision }),
    }),
  startWorkflowRun: (workflowId: string, payload: Record<string, unknown> = {}) =>
    request(`/workflows/${workflowId}/run`, {
      method: "POST",
      body: JSON.stringify({ input_payload: payload }),
    }),
  createAgent: (payload: Record<string, unknown>) =>
    request("/agents", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  createWorkflow: (payload: Record<string, unknown>) =>
    request("/workflows", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  settings: () => request("/settings"),
  cancelWorkflowRun: (runId: string) =>
    request(`/workflow-runs/${runId}/cancel`, { method: "POST", body: "{}" }),
  retryWorkflowRun: (runId: string) =>
    request(`/workflow-runs/${runId}/retry`, { method: "POST", body: "{}" }),
  pauseWorkflowRun: (runId: string) =>
    request(`/workflow-runs/${encodeURIComponent(runId)}/pause`, { method: "POST", body: "{}" }),
  resumeWorkflowRun: (runId: string) =>
    request(`/workflow-runs/${encodeURIComponent(runId)}/resume`, { method: "POST", body: "{}" }),
  expireWorkflowRun: (runId: string, reason?: string) =>
    request(`/workflow-runs/${encodeURIComponent(runId)}/expire`, {
      method: "POST",
      body: JSON.stringify(reason ? { reason } : {}),
    }),
  streamEvents: (runId: string) => request(`/workflow-runs/${runId}/stream`),
  searchKnowledge: (query: string) =>
    request(`/knowledge/search?query=${encodeURIComponent(query)}`),
  reflectRun: (runId: string) =>
    request(`/improvement/reflect/${encodeURIComponent(runId)}`, { method: "POST", body: "{}" }),
  listImprovementLessons: (workflowId?: string) =>
    request(`/improvement/lessons${workflowId ? `?workflow_id=${encodeURIComponent(workflowId)}` : ""}`),
  autoProposeImprovement: (payload: { workflow_id: string; run_id?: string }) =>
    request("/improvement/auto-propose", { method: "POST", body: JSON.stringify(payload) }),
  evolutionArchive: () => request("/evolution/archive"),
  listEvolutionVariants: () => request("/evolution/variants"),
  evaluateVariant: (variantId: string) =>
    request(`/evolution/variants/${encodeURIComponent(variantId)}/evaluate`, { method: "POST", body: "{}" }),
  promoteVariant: (variantId: string, mode: "canary" | "promote" = "canary") =>
    request(`/evolution/variants/${encodeURIComponent(variantId)}/promote`, {
      method: "POST",
      body: JSON.stringify({ mode }),
    }),
  runCoevolution: (payload: Record<string, unknown> = {}) =>
    request("/evolution/coevolution/run", { method: "POST", body: JSON.stringify(payload) }),
  governanceReview: () => request("/evolution/governance/review"),
  lessonUtilityDashboard: (agentId?: string, limit = 20) => {
    const params = new URLSearchParams();
    if (agentId) params.set("agent_id", agentId);
    params.set("limit", String(limit));
    return request(`/improvement/lesson-utility?${params.toString()}`);
  },
  videoN3Status: () => request("/domains/video/n3-status"),
  videoArchetypes: () => request("/domains/video/archetypes"),
  recommendVideoWorkflow: (payload: {
    brief: string;
    duration_sec?: number | null;
    top_k?: number;
    budget_hint?: string;
    channel_hint?: string;
  }) =>
    request("/domains/video/recommend-workflow", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  videoSpecialSkills: () => request("/domains/video/special-skills"),
  federateKnowledgeGraph: (pushNeo4j = false) =>
    request("/knowledge/graph/federate", {
      method: "POST",
      body: JSON.stringify({ push_neo4j: pushNeo4j }),
    }),
  proposeSkill: (payload: Record<string, unknown>) =>
    request("/improvement/skills/propose", { method: "POST", body: JSON.stringify(payload) }),
  listSkillProposals: () => request("/improvement/skills"),
  startImprovementLoop: (payload: Record<string, unknown>) =>
    request("/loops/run", { method: "POST", body: JSON.stringify(payload) }),
};

export { TOKEN_COOKIE };
