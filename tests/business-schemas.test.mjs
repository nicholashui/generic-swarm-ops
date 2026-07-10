import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { validateAgainstSchema } from "../scripts/business/lib/schema-lite.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("business schemas parse and examples validate", async () => {
  const pairs = [
    ["event-log.schema.json", "event-log.example.json"],
    ["decision-requirement-card.schema.json", "decision-requirement-card.example.json"],
    ["workflow-dna.schema.json", "workflow-dna.example.json"],
    ["evaluation-card.schema.json", "evaluation-card.example.json"]
  ];

  for (const [schemaName, exampleName] of pairs) {
    const schema = JSON.parse(await fs.readFile(path.join(root, "business/schemas", schemaName), "utf8"));
    const example = JSON.parse(await fs.readFile(path.join(root, "business/examples", exampleName), "utf8"));
    const result = validateAgainstSchema(schema, example);
    assert.equal(result.valid, true, `${exampleName} should validate against ${schemaName}: ${result.errors.join("; ")}`);
  }
});
