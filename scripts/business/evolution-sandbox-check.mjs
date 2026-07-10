import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { readJson } from "../lib/fs-safe.mjs";
import { createReport, printReport } from "./lib/business-report.mjs";
import { isHighRiskTier } from "./lib/risk-tiers.mjs";

const REQUIRED_FIELDS = [
  "baseline_workflow_id",
  "regression_test_result",
  "adversarial_test_result",
  "compliance_check",
  "rollback_plan"
];

export function validateVariantProposal(variant) {
  const failures = [];
  if (variant.direct_production_mutation) {
    failures.push("Variant implies direct production mutation");
  }
  for (const field of REQUIRED_FIELDS) {
    if (!(field in variant)) {
      failures.push(`Missing ${field}`);
    }
  }
  if (!Array.isArray(variant.rollback_plan) || variant.rollback_plan.length === 0) {
    failures.push("rollback_plan must be a non-empty array");
  }
  if (isHighRiskTier(variant.risk_tier) && !variant.approval_record) {
    failures.push("High-risk variants require approval_record");
  }
  return failures;
}

export async function runEvolutionSandboxCheck(rootDir = process.cwd()) {
  const directories = [
    "business/evolution/successful-variants",
    "business/evolution/failed-experiments"
  ];
  const checks = [];
  const failures = [];
  let proposalCount = 0;

  for (const relativeDir of directories) {
    const absoluteDir = path.join(rootDir, relativeDir);
    const entries = await fs.readdir(absoluteDir, { withFileTypes: true }).catch(() => []);
    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith(".json")) {
        continue;
      }
      proposalCount += 1;
      const relativePath = `${relativeDir}/${entry.name}`.replace(/\\/g, "/");
      const proposal = await readJson(path.join(absoluteDir, entry.name));
      const proposalFailures = validateVariantProposal(proposal);
      if (proposalFailures.length === 0) {
        checks.push(`validated ${relativePath}`);
      } else {
        for (const failure of proposalFailures) {
          failures.push(`${relativePath}: ${failure}`);
        }
      }
    }
  }

  if (proposalCount === 0) {
    checks.push("no variant proposals found; sandbox scaffolding present");
  }

  const report = createReport("Evolution Sandbox Check");
  report.addSection("Checks", checks);
  report.addSection("Failures", failures);
  printReport(report);

  if (failures.length > 0) {
    process.exitCode = 1;
  }
}

async function main() {
  await runEvolutionSandboxCheck(process.cwd());
}

const entryPath = process.argv[1] ? path.resolve(process.argv[1]) : "";
if (fileURLToPath(import.meta.url) === entryPath) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
