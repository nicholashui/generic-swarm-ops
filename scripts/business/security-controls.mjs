import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { listFilesRecursive, readJson } from "../lib/fs-safe.mjs";
import { createReport, printReport } from "./lib/business-report.mjs";
import { isHighRiskTier } from "./lib/risk-tiers.mjs";

const SECRET_PATTERNS = [
  /-----BEGIN (RSA|EC|OPENSSH|DSA) PRIVATE KEY-----/,
  /ghp_[A-Za-z0-9]{20,}/,
  /sk-[A-Za-z0-9]{20,}/,
  /AKIA[0-9A-Z]{16}/
];

export function inspectBusinessSecurity({ relativePath, content }) {
  const failures = [];
  const warnings = [];

  for (const pattern of SECRET_PATTERNS) {
    if (pattern.test(content)) {
      failures.push(`${relativePath}: secret-like content detected`);
      break;
    }
  }

  if (/full filesystem|unrestricted shell|all network access/i.test(content)) {
    warnings.push(`${relativePath}: review unsafe tool or MCP description`);
  }

  return { failures, warnings };
}

async function checkToolPermissions(rootDir, failures, warnings) {
  const registerPath = path.join(rootDir, "business", "security", "tool-permissions", "tool-permission-register.json");
  const register = await readJson(registerPath);
  for (const permission of register.tool_permissions || []) {
    if (permission.scope === "*" || permission.scope === "global") {
      failures.push(`tool-permission-register.json: overly broad scope for ${permission.tool}`);
    }
    if ((permission.allowed_actions || []).includes("*")) {
      failures.push(`tool-permission-register.json: wildcard action for ${permission.tool}`);
    }
    if ((permission.requires_human_gate_for || []).length === 0 && /billing|payment|delete|admin/i.test(permission.tool)) {
      warnings.push(`tool-permission-register.json: review human gate coverage for ${permission.tool}`);
    }
  }
}

async function checkWorkflowSecurity(rootDir, failures) {
  const workflowPath = path.join(rootDir, "business", "examples", "workflow-dna.example.json");
  const workflow = await readJson(workflowPath);
  for (const step of workflow.steps || []) {
    const sensitive = step.irreversible || step.action_type === "irreversible_execution" || step.action_type === "exception" || /billing|payment|delete|approval|admin/i.test((step.tools || []).join(" "));
    if (sensitive && !step.human_gate_required) {
      failures.push(`workflow-dna.example.json: step ${step.id} lacks a required human gate`);
    }
  }
  if (isHighRiskTier(workflow.risk_tier) && !(workflow.steps || []).some((step) => step.human_gate_required)) {
    failures.push("workflow-dna.example.json: high-risk workflows require at least one human-gated step");
  }
}

async function checkPromptInjectionCoverage(rootDir, failures) {
  const readmePath = path.join(rootDir, "business", "security", "prompt-injection-tests", "README.md");
  const content = await fs.readFile(readmePath, "utf8");
  if (!/indirect prompt injection/i.test(content)) {
    failures.push("prompt-injection-tests README must cover indirect prompt injection");
  }
}

export async function runBusinessSecurity(rootDir = process.cwd()) {
  const checks = [];
  const warnings = [];
  const failures = [];
  const businessRoot = path.join(rootDir, "business");
  const files = await listFilesRecursive(businessRoot);

  for (const filePath of files) {
    const relativePath = path.relative(rootDir, filePath).replace(/\\/g, "/");
    const content = await fs.readFile(filePath, "utf8").catch(() => "");
    const result = inspectBusinessSecurity({ relativePath, content });
    warnings.push(...result.warnings);
    failures.push(...result.failures);
  }

  await checkToolPermissions(rootDir, failures, warnings);
  await checkWorkflowSecurity(rootDir, failures);
  await checkPromptInjectionCoverage(rootDir, failures);

  checks.push(`scanned ${files.length} business file(s)`);

  const report = createReport("Business Security Controls");
  report.addSection("Checks", checks);
  report.addSection("Warnings", warnings);
  report.addSection("Failures", failures);
  printReport(report);

  if (failures.length > 0) {
    process.exitCode = 1;
  }
}

async function main() {
  await runBusinessSecurity(process.cwd());
}

const entryPath = process.argv[1] ? path.resolve(process.argv[1]) : "";
if (fileURLToPath(import.meta.url) === entryPath) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
