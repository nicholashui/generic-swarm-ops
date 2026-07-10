import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { inspectBusinessSecurity } from "../scripts/business/security-controls.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("tool permissions are not overly broad by default", async () => {
  const register = JSON.parse(await fs.readFile(path.join(root, "business/security/tool-permissions/tool-permission-register.json"), "utf8"));
  for (const permission of register.tool_permissions) {
    assert.notEqual(permission.scope, "*");
    assert.notEqual(permission.scope, "global");
    assert.ok(Array.isArray(permission.allowed_actions));
    assert.ok(!permission.allowed_actions.includes("*"));
  }
});

test("security scanner detects obvious secrets in fixtures", async () => {
  const content = await fs.readFile(path.join(root, "tests/fixtures/business-secret.txt"), "utf8");
  const result = inspectBusinessSecurity({
    relativePath: "tests/fixtures/business-secret.txt",
    content
  });
  assert.ok(result.failures.some((failure) => /secret-like content/i.test(failure)));
});
