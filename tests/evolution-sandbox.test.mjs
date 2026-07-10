import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validateVariantProposal } from "../scripts/business/evolution-sandbox-check.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("evolution sandbox variants do not mutate production directly", async () => {
  const variant = JSON.parse(await fs.readFile(path.join(root, "business/evolution/successful-variants/customer-onboarding-canary.json"), "utf8"));
  assert.deepEqual(validateVariantProposal(variant), []);
});

test("evolution sandbox flags direct production mutation fixtures", () => {
  const failures = validateVariantProposal({
    baseline_workflow_id: "wf_demo",
    direct_production_mutation: true,
    regression_test_result: "pass",
    adversarial_test_result: "pass",
    compliance_check: "pass",
    rollback_plan: ["revert"],
    risk_tier: "tier_4_execute_with_gate"
  });
  assert.ok(failures.some((failure) => /direct production mutation/i.test(failure)));
});
