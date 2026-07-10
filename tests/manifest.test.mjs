import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { selectSources, validateSourceManifest } from "../scripts/lib/manifest.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("sources manifest parses and validates", async () => {
  const manifest = JSON.parse(await fs.readFile(path.join(root, "sources/manifest.json"), "utf8"));
  assert.equal(validateSourceManifest(manifest), true);
  const enabled = selectSources(manifest, "all");
  assert.ok(enabled.length > 0);
  assert.equal(new Set(enabled.map((source) => source.id)).size, enabled.length);
  assert.ok(enabled.every((source) => source.target.startsWith("external/sources/")));
  assert.ok(!enabled.some((source) => source.id === "modelcontextprotocol-servers-archived"));
});
