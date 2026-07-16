/**
 * Product data facade: demo fixtures when demoMode, live backend otherwise.
 *
 * Performance: callers must load only the slices they need via loadProductSlice.
 * Individual loaders are React-cache memoized per request so duplicate keys
 * within one RSC render share one network call.
 */
import { cache } from "react";
import { redirect } from "next/navigation";
import { env } from "@/lib/config/env";
import { AppError } from "@/lib/errors/app-error";
import {
  agents as demoAgents,
  apiKeys as demoApiKeys,
  approvals as demoApprovals,
  auditLogs as demoAudit,
  dashboardMetrics as demoMetrics,
  evaluations as demoEvals,
  knowledgeDocuments as demoKnowledge,
  memoryItems as demoMemory,
  onboardingChecklist,
  processes as demoProcesses,
  tools as demoTools,
  userRows as demoUsers,
  workflowRunEvents as demoEvents,
  workflows as demoWorkflows,
} from "@/lib/demo-data";
import {
  fetchLiveAgents,
  fetchLiveApiKeys,
  fetchLiveApprovals,
  fetchLiveAuditLogs,
  fetchLiveEvaluations,
  fetchLiveKnowledge,
  fetchLiveMemory,
  fetchLiveProcessSummary,
  fetchLiveTools,
  fetchLiveUsers,
  fetchLiveWorkflowRuns,
  fetchLiveWorkflows,
} from "@/lib/api/live-data";

export type ProductSliceKey =
  | "agents"
  | "tools"
  | "workflows"
  | "approvals"
  | "knowledgeDocuments"
  | "memoryItems"
  | "evaluations"
  | "processes"
  | "auditLogs"
  | "apiKeys"
  | "userRows"
  | "workflowRunEvents";

export const ALL_PRODUCT_SLICE_KEYS: ProductSliceKey[] = [
  "agents",
  "tools",
  "workflows",
  "approvals",
  "knowledgeDocuments",
  "memoryItems",
  "evaluations",
  "processes",
  "auditLogs",
  "apiKeys",
  "userRows",
  "workflowRunEvents",
];

function handleAuthError(err: unknown): never {
  if (err instanceof AppError && (err.status === 401 || err.status === 403)) {
    redirect("/login");
  }
  throw err;
}

async function safeLive<T>(fn: () => Promise<T>): Promise<T> {
  try {
    return await fn();
  } catch (err) {
    handleAuthError(err);
  }
}

/** Per-request memoized live fetchers (dedupe within one RSC render). */
const getAgentsCached = cache(async () =>
  env.demoMode ? demoAgents : safeLive(fetchLiveAgents),
);
const getToolsCached = cache(async () =>
  env.demoMode ? demoTools : safeLive(fetchLiveTools),
);
const getWorkflowsCached = cache(async () =>
  env.demoMode ? demoWorkflows : safeLive(fetchLiveWorkflows),
);
const getApprovalsCached = cache(async () =>
  env.demoMode ? demoApprovals : safeLive(fetchLiveApprovals),
);
const getKnowledgeCached = cache(async () =>
  env.demoMode ? demoKnowledge : safeLive(fetchLiveKnowledge),
);
const getMemoryCached = cache(async () =>
  env.demoMode ? demoMemory : safeLive(fetchLiveMemory),
);
const getEvaluationsCached = cache(async () =>
  env.demoMode ? demoEvals : safeLive(fetchLiveEvaluations),
);
const getProcessesCached = cache(async () =>
  env.demoMode ? demoProcesses : safeLive(fetchLiveProcessSummary),
);
const getAuditCached = cache(async () =>
  env.demoMode ? demoAudit : safeLive(fetchLiveAuditLogs),
);
const getApiKeysCached = cache(async () =>
  env.demoMode ? demoApiKeys : safeLive(fetchLiveApiKeys),
);
const getUsersCached = cache(async () =>
  env.demoMode ? demoUsers : safeLive(fetchLiveUsers),
);
const getRunsCached = cache(async () =>
  env.demoMode ? demoEvents : safeLive(fetchLiveWorkflowRuns),
);

const sliceLoaders: Record<ProductSliceKey, () => Promise<unknown>> = {
  agents: getAgentsCached,
  tools: getToolsCached,
  workflows: getWorkflowsCached,
  approvals: getApprovalsCached,
  knowledgeDocuments: getKnowledgeCached,
  memoryItems: getMemoryCached,
  evaluations: getEvaluationsCached,
  processes: getProcessesCached,
  auditLogs: getAuditCached,
  apiKeys: getApiKeysCached,
  userRows: getUsersCached,
  workflowRunEvents: getRunsCached,
};

const emptySlice: Record<ProductSliceKey, unknown> = {
  agents: [],
  tools: [],
  workflows: [],
  approvals: [],
  knowledgeDocuments: [],
  memoryItems: [],
  evaluations: [],
  processes: [],
  auditLogs: [],
  apiKeys: [],
  userRows: [],
  workflowRunEvents: [],
};

export type ProductBundle = {
  demoMode: boolean;
  agents: Awaited<ReturnType<typeof getAgentsCached>>;
  tools: Awaited<ReturnType<typeof getToolsCached>>;
  workflows: Awaited<ReturnType<typeof getWorkflowsCached>>;
  approvals: Awaited<ReturnType<typeof getApprovalsCached>>;
  knowledgeDocuments: Awaited<ReturnType<typeof getKnowledgeCached>>;
  memoryItems: Awaited<ReturnType<typeof getMemoryCached>>;
  evaluations: Awaited<ReturnType<typeof getEvaluationsCached>>;
  processes: Awaited<ReturnType<typeof getProcessesCached>>;
  auditLogs: Awaited<ReturnType<typeof getAuditCached>>;
  apiKeys: Awaited<ReturnType<typeof getApiKeysCached>>;
  userRows: Awaited<ReturnType<typeof getUsersCached>>;
  workflowRunEvents: Awaited<ReturnType<typeof getRunsCached>>;
  dashboardMetrics: Array<{ label: string; value: string; delta: string }>;
  onboardingChecklist: typeof onboardingChecklist;
};

/**
 * Load only the requested product slices in parallel.
 * Prefer this over loadProductBundle() on route pages.
 */
export async function loadProductSlice(keys: ProductSliceKey[]): Promise<ProductBundle> {
  const unique = Array.from(new Set(keys));
  const results = await Promise.all(unique.map((key) => sliceLoaders[key]()));

  const partial: Record<ProductSliceKey, unknown> = { ...emptySlice };
  unique.forEach((key, index) => {
    partial[key] = results[index];
  });

  const agents = partial.agents as ProductBundle["agents"];
  const workflows = partial.workflows as ProductBundle["workflows"];
  const approvals = partial.approvals as ProductBundle["approvals"];
  const auditLogs = partial.auditLogs as ProductBundle["auditLogs"];

  const hasMetricSources =
    unique.includes("agents") ||
    unique.includes("workflows") ||
    unique.includes("approvals") ||
    unique.includes("auditLogs");

  const dashboardMetrics =
    env.demoMode && !hasMetricSources
      ? demoMetrics
      : [
          {
            label: "Active agents",
            value: String(agents.length),
            delta: env.demoMode ? "Demo" : "Live API",
          },
          {
            label: "Workflows",
            value: String(workflows.length),
            delta: env.demoMode ? "Demo" : "Live API",
          },
          {
            label: "Pending approvals",
            value: String(approvals.filter((a) => a.status === "pending").length),
            delta: env.demoMode ? "Demo" : "Live API",
          },
          {
            label: "Audit events",
            value: String(auditLogs.length),
            delta: env.demoMode ? "Demo" : "Live API",
          },
        ];

  return {
    demoMode: env.demoMode,
    agents: agents as ProductBundle["agents"],
    tools: partial.tools as ProductBundle["tools"],
    workflows: workflows as ProductBundle["workflows"],
    approvals: approvals as ProductBundle["approvals"],
    knowledgeDocuments: partial.knowledgeDocuments as ProductBundle["knowledgeDocuments"],
    memoryItems: partial.memoryItems as ProductBundle["memoryItems"],
    evaluations: partial.evaluations as ProductBundle["evaluations"],
    processes: partial.processes as ProductBundle["processes"],
    auditLogs: auditLogs as ProductBundle["auditLogs"],
    apiKeys: partial.apiKeys as ProductBundle["apiKeys"],
    userRows: partial.userRows as ProductBundle["userRows"],
    workflowRunEvents: partial.workflowRunEvents as ProductBundle["workflowRunEvents"],
    dashboardMetrics,
    onboardingChecklist,
  };
}

/** Full bundle — prefer loadProductSlice on pages. Kept for tests / rare full views. */
export async function loadProductBundle(): Promise<ProductBundle> {
  if (env.demoMode) {
    return {
      demoMode: true,
      agents: demoAgents,
      tools: demoTools,
      workflows: demoWorkflows,
      approvals: demoApprovals,
      knowledgeDocuments: demoKnowledge,
      memoryItems: demoMemory,
      evaluations: demoEvals,
      processes: demoProcesses,
      auditLogs: demoAudit,
      apiKeys: demoApiKeys,
      userRows: demoUsers,
      workflowRunEvents: demoEvents,
      dashboardMetrics: demoMetrics,
      onboardingChecklist,
    };
  }
  return loadProductSlice(ALL_PRODUCT_SLICE_KEYS);
}

/** Map /app/[section] to required data slices. */
export function productSlicesForRoute(section: string | undefined, child?: string): ProductSliceKey[] {
  switch (section) {
    case undefined:
    case "":
      // dashboard
      return ["agents", "workflows", "approvals", "auditLogs", "knowledgeDocuments", "processes"];
    case "domains":
      return ["agents"];
    case "agents":
      return ["agents"];
    case "tools":
      return ["tools"];
    case "workflows":
      return ["workflows"];
    case "workflow-runs":
      return ["workflowRunEvents", "workflows"];
    case "evolution":
      // client panels fetch their own data
      return [];
    case "approvals":
      return ["approvals"];
    case "knowledge":
      return ["knowledgeDocuments"];
    case "memory":
      return ["memoryItems"];
    case "evaluations":
      return ["evaluations"];
    case "processes":
      return ["processes"];
    case "audit-logs":
      return ["auditLogs"];
    case "settings":
      if (child === "api-keys") return ["apiKeys"];
      if (child === "users") return ["userRows"];
      if (child === "organization" || child === "profile") return [];
      if (child === "roles" || child === "billing" || child === "security" || child === "integrations") {
        return [];
      }
      return ["apiKeys", "userRows"];
    case "docs":
      return [];
    default:
      return [];
  }
}

export async function loadAgents() {
  return getAgentsCached();
}
export async function loadTools() {
  return getToolsCached();
}
export async function loadWorkflows() {
  return getWorkflowsCached();
}
export async function loadApprovals() {
  return getApprovalsCached();
}
export async function loadKnowledge() {
  return getKnowledgeCached();
}
export async function loadMemory() {
  return getMemoryCached();
}
export async function loadEvaluations() {
  return getEvaluationsCached();
}
export async function loadProcesses() {
  return getProcessesCached();
}
export async function loadAuditLogs() {
  return getAuditCached();
}
