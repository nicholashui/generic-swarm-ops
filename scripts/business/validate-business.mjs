import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { readJson } from "../lib/fs-safe.mjs";
import { createReport, printReport } from "./lib/business-report.mjs";
import { assertValidAgainstSchema, describeSchemaTypes } from "./lib/schema-lite.mjs";
import { isHighRiskTier, isKnownRiskTier, requiresHumanApprovalByTier } from "./lib/risk-tiers.mjs";

const REQUIRED_DIRECTORIES = [
  "business",
  "business/process-intelligence/event-logs",
  "business/process-intelligence/discovered-processes",
  "business/process-intelligence/conformance-reports",
  "business/process-intelligence/bottlenecks",
  "business/process-intelligence/causal-hypotheses",
  "business/knowledge-base/rules",
  "business/knowledge-base/decision-patterns",
  "business/knowledge-base/exceptions",
  "business/knowledge-base/best-practices",
  "business/knowledge-base/tacit-knowledge",
  "business/knowledge-base/provenance",
  "business/experts/profiles",
  "business/experts/shadow-logs",
  "business/experts/decision-requirement-cards",
  "business/experts/interview-transcripts",
  "business/materials/documents",
  "business/materials/regulations",
  "business/materials/sops",
  "business/distilled/skills",
  "business/distilled/prompts",
  "business/distilled/workflows",
  "business/distilled/checklists",
  "business/distilled/playbooks",
  "business/memory/episodic",
  "business/memory/semantic",
  "business/memory/procedural",
  "business/memory/decision-memory",
  "business/memory/evaluation-memory",
  "business/evals/golden-tasks",
  "business/evals/regression-tests",
  "business/evals/adversarial-tests",
  "business/evals/human-review-sets",
  "business/evals/benchmark-results",
  "business/governance/ai-inventory",
  "business/governance/use-case-risk-tiering",
  "business/governance/risk-assessments",
  "business/governance/human-approval-policy",
  "business/governance/audit-logs",
  "business/governance/model-cards",
  "business/governance/assurance-cases",
  "business/security/threat-models",
  "business/security/tool-permissions",
  "business/security/prompt-injection-tests",
  "business/security/red-team-results",
  "business/security/incident-reports",
  "business/evolution/workflow-dna",
  "business/evolution/successful-variants",
  "business/evolution/failed-experiments",
  "business/evolution/mutation-history",
  "business/evolution/lessons-learned",
  "business/schemas",
  "business/examples",
  "business/policies",
  "business/adapters",
  "business/reports"
];

const SCHEMA_TO_EXAMPLE = [
  ["event-log.schema.json", "event-log.example.json"],
  ["decision-requirement-card.schema.json", "decision-requirement-card.example.json"],
  ["workflow-dna.schema.json", "workflow-dna.example.json"],
  ["evaluation-card.schema.json", "evaluation-card.example.json"]
];

async function mustExist(rootDir, relativePath, failures) {
  const targetPath = path.join(rootDir, relativePath);
  const stats = await fs.stat(targetPath).catch(() => null);
  if (!stats) {
    failures.push(`Missing required path: ${relativePath}`);
    return false;
  }
  return stats;
}

function ensureProvenance(relativePath, value, failures) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    failures.push(`${relativePath} must be an object`);
    return;
  }
  const provenance = value.provenance;
  if (!provenance || typeof provenance !== "object" || Array.isArray(provenance)) {
    failures.push(`${relativePath} must include a provenance object`);
    return;
  }
  if (!Array.isArray(provenance.source_refs) || provenance.source_refs.length === 0) {
    failures.push(`${relativePath} provenance must include source_refs`);
  }
  if (!provenance.captured_by) {
    failures.push(`${relativePath} provenance must include captured_by`);
  }
  if (!provenance.recorded_at) {
    failures.push(`${relativePath} provenance must include recorded_at`);
  }
}

function validateWorkflowRules(relativePath, workflow, failures) {
  if (!Array.isArray(workflow.steps) || workflow.steps.length === 0) {
    failures.push(`${relativePath} must include bounded workflow steps`);
    return;
  }

  if (!Array.isArray(workflow.memory_reads) || workflow.memory_reads.length === 0) {
    failures.push(`${relativePath} must declare memory_reads`);
  }
  if (!Array.isArray(workflow.memory_writes) || workflow.memory_writes.length === 0) {
    failures.push(`${relativePath} must declare memory_writes`);
  }
  if (!workflow.guardrails || !Array.isArray(workflow.guardrails.human_approval_required_if)) {
    failures.push(`${relativePath} must define guardrails.human_approval_required_if`);
  }
  if (!workflow.verification || !Array.isArray(workflow.verification.required_checks) || workflow.verification.required_checks.length === 0) {
    failures.push(`${relativePath} must define verification.required_checks`);
  }
  if (!workflow.audit_log_write_required) {
    failures.push(`${relativePath} must require audit log writes`);
  }
  if (!workflow.rollback || !Array.isArray(workflow.rollback.rollback_steps) || workflow.rollback.rollback_steps.length === 0) {
    failures.push(`${relativePath} must define rollback.rollback_steps`);
  }
  if (!Array.isArray(workflow.fitness_metrics) || workflow.fitness_metrics.length === 0) {
    failures.push(`${relativePath} must define fitness_metrics`);
  }

  if (!isKnownRiskTier(workflow.risk_tier)) {
    failures.push(`${relativePath} has invalid risk tier ${workflow.risk_tier}`);
  }

  const highRisk = isHighRiskTier(workflow.risk_tier) || workflow.steps.some((step) => step.irreversible || step.action_type === "exception");
  const gatedSteps = workflow.steps.filter((step) => step.human_gate_required);
  if (highRisk && gatedSteps.length === 0) {
    failures.push(`${relativePath} must include at least one human-gated step for high-risk or irreversible work`);
  }

  if (requiresHumanApprovalByTier(workflow.risk_tier) && gatedSteps.length === 0) {
    failures.push(`${relativePath} risk tier ${workflow.risk_tier} requires a human gate`);
  }

  for (const step of workflow.steps) {
    const sensitiveStep = step.irreversible || step.action_type === "exception" || step.action_type === "irreversible_execution" || step.state === "critical_gate";
    if (!step.agent) {
      failures.push(`${relativePath} step ${step.id} must declare an agent`);
    }
    if (!Array.isArray(step.tools) || step.tools.length === 0) {
      failures.push(`${relativePath} step ${step.id} must declare tools`);
    }
    if (!Array.isArray(step.next) || step.next.length === 0) {
      failures.push(`${relativePath} step ${step.id} must declare next states`);
    }
    if (step.irreversible && (!workflow.rollback || !Array.isArray(workflow.rollback.rollback_steps) || workflow.rollback.rollback_steps.length === 0)) {
      failures.push(`${relativePath} step ${step.id} is irreversible and requires rollback steps`);
    }
    if (sensitiveStep && !step.human_gate_required) {
      failures.push(`${relativePath} step ${step.id} must be human-gated for high-risk, irreversible, or exception handling`);
    }
  }
}

export async function validateBusiness(rootDir = process.cwd()) {
  const failures = [];
  const notes = [];

  for (const relativePath of REQUIRED_DIRECTORIES) {
    const stats = await mustExist(rootDir, relativePath, failures);
    if (stats?.isDirectory()) {
      notes.push(`directory ok: ${relativePath}`);
    }
  }

  for (const [schemaName, exampleName] of SCHEMA_TO_EXAMPLE) {
    const schemaPath = path.join(rootDir, "business", "schemas", schemaName);
    const examplePath = path.join(rootDir, "business", "examples", exampleName);
    const schema = await readJson(schemaPath).catch((error) => {
      failures.push(`Failed to read schema ${schemaName}: ${error.message}`);
      return null;
    });
    const example = await readJson(examplePath).catch((error) => {
      failures.push(`Failed to read example ${exampleName}: ${error.message}`);
      return null;
    });
    if (!schema || !example) {
      continue;
    }

    notes.push(`${schemaName} schema types: ${describeSchemaTypes(schema).join(", ")}`);
    try {
      assertValidAgainstSchema(schema, example, exampleName);
      notes.push(`validated ${exampleName} against ${schemaName}`);
    } catch (error) {
      failures.push(error.message);
      continue;
    }

    if (typeof example.risk_tier === "string" && !isKnownRiskTier(example.risk_tier)) {
      failures.push(`${exampleName} uses an unknown risk tier ${example.risk_tier}`);
    }
    ensureProvenance(exampleName, example, failures);
    if (exampleName === "workflow-dna.example.json") {
      validateWorkflowRules(exampleName, example, failures);
    }
  }

  const report = createReport("Business Validation");
  report.addSection("Checks", notes);
  report.addSection("Failures", failures);
  printReport(report);

  if (failures.length > 0) {
    process.exitCode = 1;
  }

  return {
    failures,
    notes
  };
}

async function main() {
  await validateBusiness(process.cwd());
}

const entryPath = process.argv[1] ? path.resolve(process.argv[1]) : "";
if (fileURLToPath(import.meta.url) === entryPath) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
