#!/usr/bin/env node
/**
 * Export FastAPI OpenAPI schema to frontend/openapi.json (no long-running server).
 */
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const backend = path.join(root, "backend");
const out = path.join(root, "frontend", "openapi.json");

const py = `
from app.main import app
import json
from pathlib import Path
Path(r"""${out.replace(/\\/g, "\\\\")}""").write_text(
    json.dumps(app.openapi(), indent=2), encoding="utf-8"
)
print("exported", r"""${out.replace(/\\/g, "\\\\")}""")
`;

const result = spawnSync("python", ["-c", py], {
  cwd: backend,
  env: { ...process.env, PYTHONPATH: backend },
  encoding: "utf-8",
  shell: false,
});

if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
if (result.status !== 0) {
  console.error("OpenAPI export failed");
  process.exit(result.status || 1);
}
