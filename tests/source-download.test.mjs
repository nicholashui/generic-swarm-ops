import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("source lock has the expected shape", async () => {
  const realPath = path.join(root, "sources/source-lock.json");
  const fixturePath = path.join(root, "tests/fixtures/sample-source-lock.json");
  const targetPath = await fs.access(realPath).then(() => realPath).catch(() => fixturePath);
  const lock = JSON.parse(await fs.readFile(targetPath, "utf8"));
  assert.equal(lock.schema_version, "1.0");
  assert.ok(Array.isArray(lock.sources));
  assert.ok(Array.isArray(lock.failures));
  for (const source of lock.sources) {
    assert.ok(source.id);
    assert.ok(source.target.startsWith("external/sources/"));
    assert.ok(source.import_policy);
  }
});
