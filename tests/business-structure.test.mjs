import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("business structure exists", async () => {
  const required = [
    "business/process-intelligence/event-logs",
    "business/knowledge-base/provenance",
    "business/experts/decision-requirement-cards",
    "business/evals/benchmark-results",
    "business/governance/use-case-risk-tiering",
    "business/security/tool-permissions",
    "business/evolution/workflow-dna",
    "business/schemas",
    "business/examples"
  ];

  for (const relativePath of required) {
    const stats = await fs.stat(path.join(root, relativePath));
    assert.equal(stats.isDirectory(), true, `${relativePath} should be a directory`);
  }
});
