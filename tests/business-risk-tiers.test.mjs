import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { RISK_TIER_ORDER, isHighRiskTier, requiresHumanApprovalByTier } from "../scripts/business/lib/risk-tiers.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("risk tier register matches expected tier order", async () => {
  const content = JSON.parse(await fs.readFile(path.join(root, "business/governance/use-case-risk-tiering/risk-tiers.json"), "utf8"));
  const ids = content.tiers.map((tier) => tier.id);
  assert.deepEqual(ids, RISK_TIER_ORDER);
  assert.equal(isHighRiskTier("tier_4_execute_with_gate"), true);
  assert.equal(requiresHumanApprovalByTier("tier_2_draft"), true);
  assert.equal(requiresHumanApprovalByTier("tier_3_execute_reversible"), false);
});
