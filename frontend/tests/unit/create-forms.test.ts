import { describe, expect, it } from "vitest";
import { readFile } from "node:fs/promises";
import path from "node:path";
import {
  agentCreateSchema,
  formatMutationError,
  workflowCreateSchema,
} from "@/lib/forms/create-resource-schemas";
import { AppError } from "@/lib/errors/app-error";

describe("create resource schemas", () => {
  it("accepts valid agent payload", () => {
    const parsed = agentCreateSchema.parse({
      name: "Ops agent",
      description: "Handles onboarding assist",
      department: "operations",
      risk_level: "tier_2_draft",
      allowed_tools: ["audit_log_writer"],
      allowed_memory_scopes: ["workflow_memory"],
    });
    expect(parsed.name).toBe("Ops agent");
  });

  it("rejects agent without tools", () => {
    const result = agentCreateSchema.safeParse({
      name: "X",
      description: "desc",
      department: "ops",
      risk_level: "tier_2_draft",
      allowed_tools: [],
      allowed_memory_scopes: ["workflow_memory"],
    });
    expect(result.success).toBe(false);
  });

  it("accepts valid workflow payload", () => {
    const parsed = workflowCreateSchema.parse({
      name: "Onboarding",
      description: "Flagship path",
      department: "operations",
      risk_tier: "tier_4_execute_with_gate",
      primary_agent: "business_orchestrator",
      tools: ["billing_system"],
      human_gate: true,
      evaluation_suite: "golden+regression",
    });
    expect(parsed.human_gate).toBe(true);
  });

  it("formats AppError with request id and code", () => {
    const msg = formatMutationError(new AppError("validation failed", 422, "req_abc", "bad_request"));
    expect(msg).toContain("validation failed");
    expect(msg).toContain("request_id=req_abc");
    expect(msg).toContain("code=bad_request");
  });

  it("form-route-actions uses useWatch instead of form.watch (lint-safe)", async () => {
    const src = await readFile(
      path.join(process.cwd(), "src/components/domain/form-route-actions.tsx"),
      "utf8",
    );
    expect(src).toContain("useWatch");
    expect(src).toMatch(/useWatch\(\s*\{\s*control:\s*form\.control/);
    expect(src).not.toMatch(/form\.watch\s*\(/);
  });
});
