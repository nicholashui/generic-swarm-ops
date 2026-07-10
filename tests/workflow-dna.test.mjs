import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("workflow dna enforces human gates and rollback for sensitive actions", async () => {
  const workflow = JSON.parse(await fs.readFile(path.join(root, "business/examples/workflow-dna.example.json"), "utf8"));

  assert.equal(workflow.audit_log_write_required, true);
  assert.ok(Array.isArray(workflow.verification.required_checks));
  assert.ok(workflow.verification.required_checks.includes("audit_log_complete"));
  assert.ok(Array.isArray(workflow.rollback.rollback_steps));
  assert.ok(workflow.rollback.rollback_steps.length > 0);

  const gatedSensitiveSteps = workflow.steps.filter((step) => step.human_gate_required && (step.irreversible || workflow.risk_tier === "tier_4_execute_with_gate"));
  assert.ok(gatedSensitiveSteps.length > 0, "expected at least one human-gated sensitive step");
  assert.ok(workflow.steps.every((step) => Array.isArray(step.tools) && step.tools.length > 0));
});
