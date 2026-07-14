import { env } from "@/lib/config/env";
import { AppError } from "@/lib/errors/app-error";

const TOKEN_COOKIE = "gso_access_token";
let accessToken: string | null = null;

function readBrowserCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
  return match ? decodeURIComponent(match[1]) : null;
}

function writeBrowserCookie(name: string, value: string | null) {
  if (typeof document === "undefined") return;
  if (value) {
    document.cookie = `${name}=${encodeURIComponent(value)}; path=/; SameSite=Lax`;
  } else {
    document.cookie = `${name}=; path=/; Max-Age=0; SameSite=Lax`;
  }
}

/** Persist token for both client sessionStorage and a server-readable cookie (SSR). */
export function setAccessToken(token: string | null) {
  accessToken = token;
  writeBrowserCookie(TOKEN_COOKIE, token);
  if (typeof window !== "undefined") {
    if (token) window.sessionStorage.setItem(TOKEN_COOKIE, token);
    else window.sessionStorage.removeItem(TOKEN_COOKIE);
  }
}

/** Persist session user for Server Components (`getSessionUser` reads `frontend_session`). */
export function setFrontendSessionUser(user: Record<string, unknown>) {
  writeBrowserCookie("frontend_session", JSON.stringify(user));
}

export function getAccessToken(): string | null {
  if (accessToken) return accessToken;
  const fromCookie = readBrowserCookie(TOKEN_COOKIE);
  if (fromCookie) {
    accessToken = fromCookie;
    return fromCookie;
  }
  if (typeof window !== "undefined") {
    accessToken = window.sessionStorage.getItem(TOKEN_COOKIE);
  }
  return accessToken;
}

/** Server Components / RSC: read token from request cookies. */
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
  return getAccessToken();
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = await resolveAccessToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  if (token) headers.Authorization = `Bearer ${token}`;

  const response = await fetch(`${env.apiBaseUrl}${path}`, {
    credentials: "include",
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
    // FastAPI validation errors
    if (!payload.error?.message && Array.isArray(payload.detail)) {
      message = payload.detail.map((d) => d.msg || "validation error").join("; ");
    } else if (!payload.error?.message && typeof payload.detail === "string") {
      message = payload.detail;
    }
    throw new AppError(message || response.statusText, response.status, requestId, payload.error?.code);
  }
  return response.json() as Promise<T>;
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
  /** Public endpoint — no prior session required. */
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
  /** Video archetype A–J registry (selection metadata). */
  videoArchetypes: () => request("/domains/video/archetypes"),
  /** Ranked DNA recommendation from free-text brief (real selector, not mock). */
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
  /** Pack special-skill integrations (17) from REGISTRY on disk. */
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
