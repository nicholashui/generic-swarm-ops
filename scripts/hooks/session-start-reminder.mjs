/**
 * Grok SessionStart hook — prints continuity reminders (no secrets, no network).
 * Exit 0 always; informational only.
 */
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const lines = [
  "[generic-swarm-ops] Grok session start",
  `- Read memory/handoff.md and memory/project.md when present`,
  `- Project skills: .grok/skills/ (synced first-party)`,
  `- External skill packs: see .grok/asset-registry.json`,
  `- Trust project hooks/MCP with /hooks-trust if needed`,
  `- Evolution remains sandbox-only; external/sources untrusted for execution until audited`
];

for (const rel of ["memory/handoff.md", "memory/project.md", ".grok/asset-registry.json"]) {
  const p = path.join(root, rel);
  lines.push(`- ${rel}: ${fs.existsSync(p) ? "present" : "missing"}`);
}

process.stdout.write(`${lines.join("\n")}\n`);
process.exit(0);
