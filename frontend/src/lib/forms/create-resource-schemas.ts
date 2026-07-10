import { z } from "zod";

export const RISK_TIERS = [
  "tier_0_observe",
  "tier_1_suggest",
  "tier_2_draft",
  "tier_3_execute_reversible",
  "tier_4_execute_with_gate",
] as const;

export const TOOL_OPTIONS = [
  "audit_log_writer",
  "crm",
  "billing_system",
  "email",
  "contract_parser",
  "policy_retriever",
] as const;

export const MEMORY_SCOPE_OPTIONS = [
  "workflow_memory",
  "organization_memory",
  "evaluation_memory",
  "episodic",
  "semantic",
] as const;

export const agentCreateSchema = z.object({
  name: z.string().min(2, "Name is required"),
  description: z.string().min(4, "Description is required"),
  department: z.string().min(1, "Owner team is required"),
  risk_level: z.enum(RISK_TIERS),
  allowed_tools: z.array(z.string()).min(1, "Select at least one tool"),
  allowed_memory_scopes: z.array(z.string()).min(1, "Select at least one memory scope"),
  system_instructions: z.string().optional(),
});

export type AgentCreateValues = z.infer<typeof agentCreateSchema>;

export const workflowCreateSchema = z.object({
  name: z.string().min(2, "Name is required"),
  description: z.string().min(4, "Description is required"),
  department: z.string().min(1, "Owner is required"),
  risk_tier: z.enum(RISK_TIERS),
  primary_agent: z.string().min(1, "Agent is required"),
  tools: z.array(z.string()).min(1, "Select at least one tool"),
  human_gate: z.boolean(),
  evaluation_suite: z.string().min(1, "Evaluation suite is required"),
  rollback_notes: z.string().optional(),
});

export type WorkflowCreateValues = z.infer<typeof workflowCreateSchema>;

export function formatMutationError(err: unknown): string {
  if (err && typeof err === "object" && "message" in err) {
    const message = String((err as { message?: string }).message || "Request failed");
    const requestId = (err as { requestId?: string }).requestId;
    const code = (err as { code?: string }).code;
    const parts = [message];
    if (code) parts.push(`code=${code}`);
    if (requestId) parts.push(`request_id=${requestId}`);
    return parts.join(" · ");
  }
  return "Request failed";
}
