import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("governance artifacts exist", async () => {
  const required = [
    "business/governance/ai-inventory/README.md",
    "business/governance/use-case-risk-tiering/risk-tiers.json",
    "business/governance/human-approval-policy/policy.md",
    "business/governance/audit-logs/README.md",
    "business/governance/model-cards/model-card.template.md",
    "business/governance/assurance-cases/assurance-case.template.md",
    "business/security/tool-permissions/tool-permission-register.json"
  ];

  for (const relativePath of required) {
    const stats = await fs.stat(path.join(root, relativePath));
    assert.equal(stats.isFile(), true, `${relativePath} should be a file`);
  }
});
