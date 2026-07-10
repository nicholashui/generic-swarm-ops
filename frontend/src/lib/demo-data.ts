import type { Agent, ApiKeyRecord, Approval, AuditLog, EvaluationRun, KnowledgeDocument, MemoryItem, ProcessRecord, Tool, Workflow, WorkflowRunEvent } from "@/types/domain";

export const dashboardMetrics = [
  { label: "Active agents", value: "14", delta: "+3 this month" },
  { label: "Running workflows", value: "5", delta: "2 waiting approval" },
  { label: "Failed runs", value: "2", delta: "Below warning threshold" },
  { label: "Evaluation pass rate", value: "92%", delta: "Stable over 7 days" },
];
export const agents: Agent[] = [
  { id: "agent_support_triage", name: "Support triage coordinator", status: "active", owner: "Alex Morgan", toolCount: 4, knowledgeAccess: "Support KB", updatedAt: "2026-07-07T08:45:00Z", description: "Routes inbound support requests and applies approval-aware escalation rules." },
  { id: "agent_invoice_review", name: "Invoice review analyst", status: "draft", owner: "Priya Chen", toolCount: 3, knowledgeAccess: "Finance policies", updatedAt: "2026-07-06T13:05:00Z", description: "Validates incoming invoices against risk and approval thresholds." },
];
export const tools: Tool[] = [
  { id: "tool_slack", name: "Slack Workspace", category: "Communication", status: "connected", lastUsed: "2026-07-07T08:40:00Z", usageCount: 214, credentials: "Configured, secrets masked" },
  { id: "tool_notion", name: "Notion Knowledge Sync", category: "Documents", status: "error", lastUsed: "2026-07-07T06:15:00Z", usageCount: 48, credentials: "Reconnect required" },
];
export const workflows: Workflow[] = [
  { id: "wf_customer_onboarding_v12", name: "Customer onboarding", status: "active", owner: "Alex Morgan", trigger: "Manual", successRate: "96%", updatedAt: "2026-07-07T08:20:00Z", description: "Intake, enrichment, knowledge retrieval, risk checks, and reviewer approval." },
  { id: "wf_invoice_audit_v5", name: "Invoice audit", status: "paused", owner: "Priya Chen", trigger: "Scheduled", successRate: "89%", updatedAt: "2026-07-06T16:50:00Z", description: "Reviews finance records, identifies anomalies, and prepares audit-ready evidence." },
];
export const approvals: Approval[] = [
  { id: "approval_01", title: "Approve onboarding outreach", status: "pending", risk: "High", workflow: "Customer onboarding", requester: "Support triage coordinator", createdAt: "2026-07-07T08:28:00Z", reason: "Customer risk score exceeded automatic approval threshold." },
  { id: "approval_02", title: "Reject finance exception payout", status: "approved", risk: "Critical", workflow: "Invoice audit", requester: "Invoice review analyst", createdAt: "2026-07-06T14:05:00Z", reason: "Payout requires reviewer confirmation due to policy exception." },
];
export const knowledgeDocuments: KnowledgeDocument[] = [
  { id: "doc_policy_01", title: "Support escalation policy", source: "Confluence", status: "indexed", updatedAt: "2026-07-07T05:30:00Z", snippet: "Escalations above medium risk require reviewer sign-off and visible audit context." },
  { id: "doc_finance_07", title: "Invoice exception handbook", source: "Notion", status: "failed", updatedAt: "2026-07-07T06:12:00Z", snippet: "Sync failed during schema normalization. Reconnect source and re-index." },
];
export const memoryItems: MemoryItem[] = [
  { id: "mem_01", title: "Customer onboarding edge cases", scope: "organization", sensitivity: "internal", lastUsed: "2026-07-07T08:22:00Z", createdAt: "2026-07-05T11:00:00Z", preview: "Flag accounts with incomplete tax data before triggering outreach." },
  { id: "mem_02", title: "Finance reviewer preference", scope: "department", sensitivity: "restricted", lastUsed: "2026-07-06T16:10:00Z", createdAt: "2026-07-04T09:40:00Z", preview: "Masked in UI preview because the record is marked sensitive by policy." },
];
export const evaluations: EvaluationRun[] = [
  { id: "eval_01", name: "Onboarding regression suite", target: "Customer onboarding", score: "0.92", status: "passed", updatedAt: "2026-07-07T07:45:00Z" },
  { id: "eval_02", name: "Invoice anomaly suite", target: "Invoice audit", score: "0.84", status: "warning", updatedAt: "2026-07-06T17:15:00Z" },
];
export const processes: ProcessRecord[] = [
  { id: "proc_01", name: "Knowledge re-index", status: "running", type: "knowledge", startedAt: "2026-07-07T08:01:00Z", duration: "24m", progress: "68%" },
  { id: "proc_02", name: "Nightly evaluation batch", status: "succeeded", type: "evaluation", startedAt: "2026-07-06T23:00:00Z", duration: "14m", progress: "100%" },
];
export const auditLogs: AuditLog[] = [
  { id: "audit_01", action: "workflow_run.started", actor: "Alex Morgan", resource: "wf_customer_onboarding_v12", status: "success", createdAt: "2026-07-07T08:28:12Z" },
  { id: "audit_02", action: "api_key.created", actor: "Alex Morgan", resource: "api_ops_console", status: "success", createdAt: "2026-07-07T08:11:02Z" },
];
export const apiKeys: ApiKeyRecord[] = [
  { id: "api_ops_console", name: "Operations console", status: "active", createdAt: "2026-07-07T08:11:02Z", lastUsed: "2026-07-07T08:29:02Z", maskedValue: "api_4f0a••••••••••2c19" },
  { id: "api_audit_export", name: "Audit export integration", status: "revoked", createdAt: "2026-07-02T10:22:00Z", lastUsed: "2026-07-05T16:08:00Z", maskedValue: "api_802b••••••••••ea11" },
];
export const userRows = [
  { id: "user_admin", name: "Alex Morgan", role: "Admin", status: "Active", lastActive: "2 minutes ago" },
  { id: "user_reviewer", name: "Priya Chen", role: "Reviewer", status: "Active", lastActive: "1 hour ago" },
  { id: "user_auditor", name: "Diego Mendez", role: "Security Auditor", status: "Invited", lastActive: "Never" },
];
export const onboardingChecklist = ["Create first agent", "Connect first tool", "Add knowledge source", "Create workflow", "Run workflow", "Invite teammate"];
export const workflowRunEvents: WorkflowRunEvent[] = [
  { id: "evt_01", runId: "run_01", type: "run.started", timestamp: "2026-07-07T08:28:12Z", payload: { message: "Workflow queued and dispatch accepted." } },
  { id: "evt_02", runId: "run_01", type: "step.started", timestamp: "2026-07-07T08:28:30Z", payload: { step: "Collect customer context", agent: "Support triage coordinator" } },
  { id: "evt_03", runId: "run_01", type: "approval.requested", timestamp: "2026-07-07T08:29:18Z", payload: { step: "Reviewer gate", risk: "High", assignedReviewer: "Priya Chen" } },
];
