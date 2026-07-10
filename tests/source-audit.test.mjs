import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("source audit markdown is generated", async () => {
  const auditPath = path.join(root, "docs/source-audit.md");
  const content = await fs.readFile(auditPath, "utf8");
  assert.match(content, /^# Source Audit/m);
  assert.match(content, /^## ecc/m);
  assert.match(content, /Selected components:/);
});
