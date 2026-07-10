import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { createReport, printReport } from "./lib/business-report.mjs";

const REQUIRED_FILES = [
  "business/governance/ai-inventory/README.md",
  "business/governance/use-case-risk-tiering/risk-tiers.json",
  "business/governance/human-approval-policy/policy.md",
  "business/governance/audit-logs/README.md",
  "business/governance/model-cards/model-card.template.md",
  "business/governance/assurance-cases/assurance-case.template.md",
  "business/security/tool-permissions/tool-permission-register.json"
];

export async function runGovernanceCheck(rootDir = process.cwd()) {
  const checks = [];
  const failures = [];

  for (const relativePath of REQUIRED_FILES) {
    const targetPath = path.join(rootDir, relativePath);
    const stats = await fs.stat(targetPath).catch(() => null);
    if (!stats) {
      failures.push(`Missing governance artifact: ${relativePath}`);
      continue;
    }
    checks.push(`present: ${relativePath}`);
  }

  const report = createReport("Business Governance Check");
  report.addSection("Checks", checks);
  report.addSection("Failures", failures);
  printReport(report);

  if (failures.length > 0) {
    process.exitCode = 1;
  }
}

async function main() {
  await runGovernanceCheck(process.cwd());
}

const entryPath = process.argv[1] ? path.resolve(process.argv[1]) : "";
if (fileURLToPath(import.meta.url) === entryPath) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
