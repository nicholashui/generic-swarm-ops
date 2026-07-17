/**
 * Live backend data adapters for demoMode=false.
 * Maps API payloads into the UI domain shapes used by product pages.
 */
import { backendApi } from "@/lib/api/client";
import type {
  Agent,
  ApiKeyRecord,
  Approval,
  AuditLog,
  EvaluationRun,
  KnowledgeDocument,
  MemoryItem,
  ProcessRecord,
  Tool,
  Workflow,
  WorkflowRunEvent,
} from "@/types/domain";

type Json = Record<string, unknown>;

function asString(value: unknown, fallback = ""): string {
  if (value == null) return fallback;
  return String(value);
}

export async function fetchLiveAgents(): Promise<Agent[]> {
  const rows = (await backendApi.listAgents()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    name: asString(row.name, asString(row.id)),
    status: asString(row.status, "active"),
    owner: asString(row.owner_user_id || row.owner, "system"),
    toolCount: Array.isArray(row.allowed_tools) ? row.allowed_tools.length : 0,
    knowledgeAccess: asString((row.allowed_memory_scopes as string[] | undefined)?.[0], "organization"),
    updatedAt: asString(row.updated_at || row.created_at, new Date().toISOString()),
    description: asString(row.description, asString(row.name)),
  }));
}

export async function fetchLiveTools(): Promise<Tool[]> {
  const rows = (await backendApi.listTools()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    name: asString(row.name, asString(row.id)),
    category: asString(row.category, "internal"),
    status: row.enabled === false ? "error" : "connected",
    lastUsed: asString(row.last_used || row.updated_at, new Date().toISOString()),
    usageCount: Number(row.usage_count || 0),
    credentials: asString(row.scope, "Configured"),
  }));
}

export async function fetchLiveWorkflows(): Promise<Workflow[]> {
  const rows = (await backendApi.listWorkflows()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    name: asString(row.name, asString(row.id)),
    status: asString(row.status, "active"),
    owner: asString(row.owner, "system"),
    trigger: "API",
    successRate: "n/a",
    updatedAt: asString(row.updated_at || row.created_at, new Date().toISOString()),
    description: asString(row.description || row.objective, asString(row.name)),
    // Preserve schema for Run now payload builder (extra field on domain Workflow is fine)
    input_schema: row.input_schema as Workflow["input_schema"] | undefined,
    // LangGraph orchestration fields (LG-13)
    execution_engine: row.execution_engine ?? row.engine,
    orchestration: row.orchestration,
  })) as Workflow[];
}

export async function fetchLiveApprovals(): Promise<Approval[]> {
  const rows = (await backendApi.listApprovals()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    title: asString(row.requested_action || row.step_id, "Approval"),
    status: asString(row.status, "pending"),
    risk: asString(row.risk_level, "medium"),
    workflow: asString(row.workflow_id),
    requester: asString(row.requested_by),
    createdAt: asString(row.created_at, new Date().toISOString()),
    reason: asString(row.decision_reason || row.requested_action, "Human gate"),
  }));
}

export async function fetchLiveKnowledge(): Promise<KnowledgeDocument[]> {
  const rows = (await backendApi.listKnowledge()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    title: asString(row.title, asString(row.id)),
    source: asString(
      row.source ||
        (Array.isArray((row.provenance as Json | undefined)?.source_refs)
          ? ((row.provenance as Json).source_refs as unknown[])[0]
          : undefined),
      "api",
    ),

    status: asString(row.status, "indexed"),
    updatedAt: asString(row.updated_at || row.created_at, new Date().toISOString()),
    snippet: asString(row.content, "").slice(0, 160),
  }));
}

export async function fetchLiveMemory(): Promise<MemoryItem[]> {
  const rows = (await backendApi.listMemory()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    title: asString(row.title, asString(row.id)),
    scope: asString(row.scope, "organization"),
    sensitivity: asString(row.sensitivity_level, "internal"),
    lastUsed: asString(row.updated_at || row.created_at, new Date().toISOString()),
    createdAt: asString(row.created_at, new Date().toISOString()),
    preview: asString(row.content, "").slice(0, 160),
  }));
}

export async function fetchLiveEvaluations(): Promise<EvaluationRun[]> {
  const rows = (await backendApi.listEvaluations()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    name: asString(row.eval_type || row.target, asString(row.id)),
    target: asString(row.target || row.workflow_id),
    score: asString((row.metrics as Json | undefined)?.quality_score ?? "n/a"),
    status: asString(row.status || row.result, "unknown"),
    updatedAt: asString(row.created_at, new Date().toISOString()),
  }));
}

export async function fetchLiveProcessSummary(): Promise<ProcessRecord[]> {
  const summary = (await backendApi.processSummary()) as Json;
  const activity = (summary.activity_counts as Record<string, number> | undefined) || {};
  return Object.entries(activity).map(([name, count]) => ({
    id: `proc_${name}`,
    name,
    status: "succeeded",
    type: "process_intelligence",
    startedAt: new Date().toISOString(),
    duration: `${count} events`,
    progress: "100%",
  }));
}

export async function fetchLiveAuditLogs(): Promise<AuditLog[]> {
  const rows = (await backendApi.listAuditLogs()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    action: asString(row.action),
    actor: asString(row.actor_user_id || row.actor_type, "system"),
    resource: asString(row.resource_id || row.resource_type),
    status: asString(row.status, "success"),
    createdAt: asString(row.created_at, new Date().toISOString()),
  }));
}

export async function liveLogin(email: string, password: string): Promise<{ access_token: string; user: Json }> {
  return backendApi.login(email, password) as Promise<{ access_token: string; user: Json }>;
}

export async function liveApprove(approvalId: string, reason?: string): Promise<Json> {
  return backendApi.decideApproval(approvalId, "approved", reason) as Promise<Json>;
}

export async function liveReject(approvalId: string, reason?: string): Promise<Json> {
  return backendApi.decideApproval(approvalId, "rejected", reason) as Promise<Json>;
}

export async function liveStartWorkflow(workflowId: string, payload: Record<string, unknown> = {}): Promise<Json> {
  return backendApi.startWorkflowRun(workflowId, payload) as Promise<Json>;
}

export async function fetchLiveWorkflowRuns(): Promise<WorkflowRunEvent[]> {
  const rows = (await backendApi.listWorkflowRuns()) as Json[];
  return rows.flatMap((row) => {
    const runId = asString(row.id, "run");
    return [
      {
        id: `${runId}_evt_status`,
        runId,
        type: "run.status_changed" as const,
        timestamp: asString(row.updated_at || row.created_at, new Date().toISOString()),
        payload: {
          status: asString(row.status),
          workflow_id: asString(row.workflow_id),
          message: `Run ${runId} is ${asString(row.status)}`,
        },
      },
    ];
  });
}

export async function fetchLiveApiKeys(): Promise<ApiKeyRecord[]> {
  const rows = (await backendApi.listApiKeys()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id || row.token || row.name),
    name: asString(row.name, "api-key"),
    status: asString(row.status, "active"),
    createdAt: asString(row.created_at, new Date().toISOString()),
    lastUsed: asString(row.last_used || row.created_at, new Date().toISOString()),
    maskedValue: asString(row.masked_value || row.id, "api_••••"),
  }));
}

export async function fetchLiveUsers(): Promise<{ id: string; name: string; role: string; status: string; lastActive: string }[]> {
  const rows = (await backendApi.listUsers()) as Json[];
  return rows.map((row) => ({
    id: asString(row.id),
    name: asString(row.name || row.email),
    role: asString(row.role, "viewer"),
    status: asString(row.status, "Active"),
    lastActive: asString(row.updated_at || row.created_at, "recent"),
  }));
}
