import test from "node:test";
import assert from "node:assert/strict";

import { buildGrokFiles } from "../scripts/adapters/grok.mjs";
import { buildTraeFiles } from "../scripts/adapters/trae.mjs";
import {
  AGENT_RULES_MARKDOWN,
  BUSINESS_AGENTS,
  HARNESS_COMMANDS,
  PROJECT_SKILLS
} from "../scripts/adapters/shared.mjs";

test("trae adapter defines the expected managed outputs", () => {
  const files = buildTraeFiles();
  assert.ok(files["AGENTS.md"]);
  assert.ok(files["docs/agents.md"]);
  assert.ok(files["docs/trae.md"]);
  assert.ok(files[".trae/settings.json"]);
  assert.match(files["AGENTS.md"], /Trae IDE and Grok Build/);
  assert.match(files["AGENTS.md"], /memory\/handoff\.md/);
  assert.ok(files[".trae/agents/business-orchestrator.md"]);
  assert.ok(files[".trae/commands/sync-trae.md"]);
});

test("grok adapter defines the expected managed outputs", () => {
  const files = buildGrokFiles();
  assert.ok(files["docs/grok.md"]);
  assert.ok(files[".grok/rules/session-start.md"]);
  assert.ok(files[".grok/agents/business-orchestrator.md"]);
  assert.ok(files[".grok/commands/sync-workspace.md"]);
  for (const skill of PROJECT_SKILLS) {
    const key = `.grok/skills/${skill.name}/SKILL.md`;
    assert.ok(files[key], `missing ${key}`);
    assert.match(files[key], new RegExp(`name:\\s*${skill.name}`));
  }
});

test("shared roster is non-empty and dual outputs do not collide", () => {
  assert.ok(BUSINESS_AGENTS.length >= 10);
  assert.ok(HARNESS_COMMANDS.length >= 5);
  assert.ok(AGENT_RULES_MARKDOWN.includes("dual-harness"));

  const trae = buildTraeFiles();
  const grok = buildGrokFiles();
  for (const key of Object.keys(trae)) {
    assert.equal(Object.hasOwn(grok, key), false, `path collision: ${key}`);
  }
});
