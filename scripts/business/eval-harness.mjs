import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { readJson } from "../lib/fs-safe.mjs";
import { createReport, printReport } from "./lib/business-report.mjs";
import { assertValidAgainstSchema } from "./lib/schema-lite.mjs";

function parseArgs(argv) {
  return {
    dryRun: argv.includes("--dry-run")
  };
}

export function evaluateCard(card, options = {}) {
  const failures = [];

  if (card.promotion_decision === "promote") {
    failures.push("Automatic promotion is not allowed");
  }

  // Full evaluation cards require metrics; corpus seeds may use assertions instead
  if (card.metrics) {
    const requiredMetrics = [
      "quality_score",
      "compliance_pass_rate",
      "average_cycle_time_minutes",
      "escalation_rate",
      "hallucination_rate",
      "unauthorized_tool_attempts",
      "cost_per_case_usd"
    ];
    for (const metric of requiredMetrics) {
      if (!(metric in (card.metrics || {}))) {
        failures.push(`Missing metric: ${metric}`);
      }
    }
  } else if (!card.assertions && !card.expected && !card.cases && !card.pass_criteria) {
    failures.push("Eval card missing metrics or structured expectations");
  }

  const status = failures.length > 0 ? "fail" : options.dryRun ? "blocked" : card.result || "pass";
  return {
    status,
    failures,
    target: card.target
  };
}

async function loadJsonDir(rootDir, relativeDir) {
  const abs = path.join(rootDir, relativeDir);
  const entries = await fs.readdir(abs, { withFileTypes: true }).catch(() => []);
  const cards = [];
  for (const entry of entries) {
    if (!entry.isFile() || !entry.name.endsWith(".json")) continue;
    cards.push({
      relativePath: path.posix.join(relativeDir.replace(/\\/g, "/"), entry.name),
      value: await readJson(path.join(abs, entry.name))
    });
  }
  return cards;
}

async function loadEvalCards(rootDir) {
  const schemaPath = path.join(rootDir, "business", "schemas", "evaluation-card.schema.json");
  const examplePath = path.join(rootDir, "business", "examples", "evaluation-card.example.json");
  const schema = await readJson(schemaPath);
  const cards = [];

  // Full corpus: golden, regression, adversarial, historical-replay, benchmarks
  for (const dir of [
    "business/evals/benchmark-results",
    "business/evals/golden-tasks",
    "business/evals/regression-tests",
    "business/evals/adversarial-tests",
    "business/evals/historical-replay"
  ]) {
    const loaded = await loadJsonDir(rootDir, dir);
    cards.push(...loaded);
  }

  if (cards.length === 0) {
    cards.push({
      relativePath: "business/examples/evaluation-card.example.json",
      value: await readJson(examplePath)
    });
  }

  for (const card of cards) {
    // Only full evaluation cards must match schema; other corpus files get soft checks
    if (card.value?.metrics && card.value?.promotion_decision) {
      assertValidAgainstSchema(schema, card.value, card.relativePath);
    } else if (card.value?.promotion_decision === "promote") {
      throw new Error(`${card.relativePath}: Automatic promotion is not allowed`);
    }
  }

  return cards;
}

export async function runEvaluationHarness(rootDir = process.cwd(), options = {}) {
  const cards = await loadEvalCards(rootDir);
  const findings = [];
  let exitCode = 0;

  for (const card of cards) {
    const result = evaluateCard(card.value, options);
    findings.push(`${card.relativePath}: ${result.status}`);
    for (const failure of result.failures) {
      findings.push(`${card.relativePath}: ${failure}`);
    }
    if (result.status === "fail") {
      exitCode = 1;
    }
  }

  const report = createReport("Business Evaluation Harness");
  report.addSection("Mode", [options.dryRun ? "dry-run" : "standard"]);
  report.addSection("Results", findings);
  printReport(report);

  if (exitCode > 0) {
    process.exitCode = exitCode;
  }
}

async function main() {
  await runEvaluationHarness(process.cwd(), parseArgs(process.argv.slice(2)));
}

const entryPath = process.argv[1] ? path.resolve(process.argv[1]) : "";
if (fileURLToPath(import.meta.url) === entryPath) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
