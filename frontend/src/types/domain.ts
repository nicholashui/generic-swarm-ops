import type { AppRole } from "./permissions";

export type SessionUser = { id: string; organization_id: string; email: string; name: string; role: AppRole };
export type Agent = { id: string; name: string; status: string; owner: string; toolCount: number; knowledgeAccess: string; updatedAt: string; description: string };
export type Tool = { id: string; name: string; category: string; status: string; lastUsed: string; usageCount: number; credentials: string };
export type Workflow = {
  id: string;
  name: string;
  status: string;
  owner: string;
  trigger: string;
  successRate: string;
  updatedAt: string;
  description: string;
  input_schema?: {
    type?: string;
    required?: string[];
    properties?: Record<string, { type?: string; default?: unknown }>;
  } | null;
};
export type Approval = { id: string; title: string; status: string; risk: string; workflow: string; requester: string; createdAt: string; reason: string };
export type KnowledgeDocument = { id: string; title: string; source: string; status: string; updatedAt: string; snippet: string };
export type MemoryItem = { id: string; title: string; scope: string; sensitivity: string; lastUsed: string; createdAt: string; preview: string };
export type EvaluationRun = { id: string; name: string; target: string; score: string; status: string; updatedAt: string };
export type ProcessRecord = { id: string; name: string; status: string; type: string; startedAt: string; duration: string; progress: string };
export type AuditLog = { id: string; action: string; actor: string; resource: string; status: string; createdAt: string };
export type ApiKeyRecord = { id: string; name: string; status: string; createdAt: string; lastUsed: string; maskedValue: string };
export type WorkflowRunEvent = { id: string; runId: string; type: "run.started" | "run.status_changed" | "step.started" | "step.completed" | "step.failed" | "tool_call.started" | "tool_call.completed" | "approval.requested" | "approval.approved" | "approval.rejected" | "log" | "error" | "run.completed" | "run.failed" | "run.cancelled"; timestamp: string; payload: Record<string, unknown> };
