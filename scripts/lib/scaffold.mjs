import path from "node:path";
import { fileURLToPath } from "node:url";

import { ensureDir, pathExists, writeJson, writeText } from "./fs-safe.mjs";
import { getDocsManifest, getSourceManifest } from "./manifest.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, "..", "..");

const REQUIRED_DIRECTORIES = [
  ".trae",
  ".trae/rules",
  ".trae/agents",
  ".trae/commands",
  "sources",
  "external",
  "external/sources",
  "external/docs",
  "scripts",
  "scripts/adapters",
  "scripts/lib",
  "rules",
  "skills",
  "skills/planning",
  "skills/implementation",
  "skills/testing",
  "skills/review",
  "skills/security",
  "skills/memory",
  "skills/lifecycle",
  "hooks",
  "hooks/scripts",
  "mcp-configs",
  "mcp-configs/optional",
  "memory",
  "memory/reflections",
  "reviews",
  "suggestions",
  "suggestions/pending",
  "suggestions/approved",
  "suggestions/rejected",
  "docs",
  "examples",
  "examples/sdd-feature-workflow",
  "examples/self-review-workflow",
  "examples/skill-suggestion-workflow",
  "examples/trae-sync-workflow",
  "tests",
  "tests/fixtures"
];

function repoRootRelative(filePath) {
  return path.relative(projectRoot, filePath).replace(/\\/g, "/");
}

async function writeIfMissing(rootDir, relativePath, content) {
  const targetPath = path.join(rootDir, relativePath);
  if (await pathExists(targetPath)) {
    return false;
  }
  await writeText(targetPath, content);
  return true;
}

async function writeJsonIfMissing(rootDir, relativePath, value) {
  const targetPath = path.join(rootDir, relativePath);
  if (await pathExists(targetPath)) {
    return false;
  }
  await writeJson(targetPath, value);
  return true;
}

export async function createRequiredStructure(rootDir) {
  for (const relativeDir of REQUIRED_DIRECTORIES) {
    await ensureDir(path.join(rootDir, relativeDir));
  }
}

function createStaticFiles({ projectName, projectPurpose, stack }) {
  return {
    ".gitignore": `node_modules/\nexternal/sources/\nexternal/docs/\n`,
    ".editorconfig": `root = true\n\n[*]\ncharset = utf-8\nend_of_line = lf\ninsert_final_newline = true\nindent_style = space\nindent_size = 2\ntrim_trailing_whitespace = true\n`,
    "external/.gitignore": `# Downloaded upstream repositories are intentionally not committed.\nsources/\ndocs/\n`,
    "sources/README.md": `# Sources\n\nThis directory stores source manifests and source lock metadata used by the starter bootstrap workflow.\n`,
    "rules/manifest.json": `${JSON.stringify({
      schema_version: "1.0",
      files: [
        "00-constitution.md",
        "10-karpathy.md",
        "20-sdd.md",
        "30-security.md",
        "40-testing.md",
        "50-token-efficiency.md",
        "60-human-approval.md"
      ]
    }, null, 2)}\n`,
    "rules/00-constitution.md": `# Constitution\n\n- Follow the user's goal exactly.\n- Prefer simple, maintainable solutions.\n- Make surgical changes.\n- Do not perform destructive actions without approval.\n- Do not install, execute, or import downloaded third-party code until audited.\n- Run relevant tests or explain why tests were not run.\n- Update status after major work.\n`,
    "rules/10-karpathy.md": `# Karpathy-Style Agent Rules\n\n- Think before coding.\n- Do not assume hidden requirements.\n- Prefer the simplest working solution.\n- Avoid speculative abstractions.\n- Change only what is necessary.\n- Keep the goal visible.\n- Verify the result.\n`,
    "rules/20-sdd.md": `# Spec-Driven Development\n\n- Treat \`starter.md\` as the implementation contract.\n- Prefer explicit manifests over hidden conventions.\n- Keep generated outputs reproducible through scripts.\n`,
    "rules/30-security.md": `# Security\n\n- Downloaded sources are untrusted until audited.\n- Never execute downloaded repository hooks or install scripts.\n- Record suspicious patterns in security and audit outputs.\n`,
    "rules/40-testing.md": `# Testing\n\n- Add focused tests for bootstrap-critical logic.\n- Run tests before claiming success.\n- Keep tests deterministic and dependency-free.\n`,
    "rules/50-token-efficiency.md": `# Token Efficiency\n\n- Read only what is needed.\n- Reuse manifests and generated summaries.\n- Avoid unnecessary repo-wide rewrites.\n`,
    "rules/60-human-approval.md": `# Human Approval\n\nHuman approval is required before:\n\n- installing global packages,\n- running remote install scripts,\n- enabling MCP servers with credentials,\n- copying third-party repo code into active Trae workspace configs,\n- modifying hooks,\n- deleting files,\n- applying self-generated skill/rule changes.\n`,
    "skills/manifest.json": `${JSON.stringify({
      schema_version: "1.0",
      skills: [
        "planning",
        "implementation",
        "testing",
        "review",
        "security",
        "memory",
        "lifecycle"
      ]
    }, null, 2)}\n`,
    "hooks/manifest.json": `${JSON.stringify({ schema_version: "1.0", hooks: [] }, null, 2)}\n`,
    "mcp-configs/manifest.json": `${JSON.stringify({
      schema_version: "1.0",
      configs: ["minimal.json"]
    }, null, 2)}\n`,
    "mcp-configs/minimal.json": `${JSON.stringify({
      mcpServers: {}
    }, null, 2)}\n`,
    "memory/README.md": `# Memory\n\nProject memory files for handoff, reflections, and long-lived project context.\n`,
    "memory/project.md": `# Project Memory\n\n- Project name: ${projectName}\n- Purpose: ${projectPurpose}\n- Stack: ${stack}\n`,
    "memory/handoff.md": `# Handoff\n\nDocument current progress, blockers, and next steps here.\n`,
    "suggestions/audit-log.md": `# Suggestions Audit Log\n\nNo suggestions recorded yet.\n`,
    "docs/installation.md": `# Installation\n\n## Requirements\n\n- Node.js 20+\n- Git\n\n## Setup\n\n\`\`\`bash\nnpm run init\nnpm run bootstrap\n\`\`\`\n`,
    "docs/usage.md": `# Usage\n\n## Common Commands\n\n- \`npm run bootstrap\`\n- \`npm run doctor\`\n- \`npm run sources:download\`\n- \`npm run sources:audit\`\n- \`npm run sync -- --dry-run\`\n`,
    "docs/agents.md": `# Agents\n\nThis project targets Trae IDE and keeps downstream source repositories as reference material until audited.\n`,
    "docs/trae.md": `# Trae\n\nThis starter generates project-level Trae artifacts under \`.trae/\` and keeps them reproducible via \`npm run sync\`.\n`,
    "docs/architecture.md": `# Architecture\n\nThe repository is organized around manifests, bootstrap scripts, audit outputs, and generated Trae workspace files.\n`,
    "docs/security.md": `# Security\n\nDownloaded repositories are untrusted by default. The security script scans for suspicious scripts, secrets, and overly broad MCP access.\n`,
    "docs/sync.md": `# Sync\n\nThe sync layer generates Trae-facing files such as \`AGENTS.md\`, \`docs/agents.md\`, \`docs/trae.md\`, and \`.trae/*\`.\n`,
    "docs/troubleshooting.md": `# Troubleshooting\n\n- Run \`npm run doctor\` to check local prerequisites.\n- Inspect \`sources/source-lock.json\` for clone failures.\n- Inspect \`docs/source-audit.md\` for audit warnings.\n`,
    "docs/changelog.md": `# Changelog\n\n## 1.2.0-trae-only\n\n- Initial self-bootstrap implementation for Trae IDE.\n`,
    "README.md": `# starter\n\nExecutable starter for downloading, auditing, curating, and syncing Trae IDE workspace sources.\n\n## Quick start\n\n\`\`\`bash\nnpm run bootstrap\n\`\`\`\n\nThis downloads approved upstream repositories into:\n\n\`\`\`text\nexternal/sources/\n\`\`\`\n\nThen it writes:\n\n\`\`\`text\nsources/source-lock.json\ndocs/source-audit.md\n\`\`\`\n\n## Important\n\nDownloaded repositories are untrusted until audited.\n\nThe project does not execute downloaded code and does not import third-party skills automatically.\n`,
    "task.md": `# Task\n\nImplement \`starter.md\` as an executable repository.\n\n## Required first milestone\n\n- [ ] Create package.json\n- [ ] Create source manifests\n- [ ] Create create-project flow\n- [ ] Create downloader\n- [ ] Download enabled GitHub sources\n- [ ] Generate source lock\n- [ ] Generate source audit\n- [ ] Run doctor\n- [ ] Run tests\n`,
    "status.md": `# Status\n\n## Current phase\n\nBootstrap implementation.\n\n## Latest update\n\nIn progress.\n\n## Blockers\n\nNone yet.\n\n## Commands to run\n\n\`\`\`bash\nnpm run bootstrap\n\`\`\`\n`,
    "examples/sdd-feature-workflow/README.md": `# Example\n\nSpec-driven feature workflow placeholder.\n`,
    "examples/self-review-workflow/README.md": `# Example\n\nSelf-review workflow placeholder.\n`,
    "examples/skill-suggestion-workflow/README.md": `# Example\n\nSkill suggestion workflow placeholder.\n`,
    "examples/trae-sync-workflow/README.md": `# Example\n\nTrae sync workflow placeholder.\n`,
    "tests/fixtures/sample-source-lock.json": `${JSON.stringify({
      schema_version: "1.0",
      generated_at: "2026-07-07T00:00:00.000Z",
      sources: [
        {
          id: "ecc",
          name: "ECC / Everything Claude Code",
          url: "https://github.com/affaan-m/ECC.git",
          resolved_url: "https://github.com/affaan-m/ECC.git",
          target: "external/sources/ecc",
          status: "downloaded",
          commit: "abc123",
          branch: "main",
          last_commit_at: "2026-07-07T00:00:00Z",
          last_commit_subject: "fixture",
          license_files: ["LICENSE"],
          package_files: ["package.json"],
          quarantine: false,
          import_policy: "curated-only"
        }
      ],
      failures: []
    }, null, 2)}\n`,
    "tests/manifest.test.mjs": `import test from "node:test";\nimport assert from "node:assert/strict";\nimport fs from "node:fs/promises";\nimport path from "node:path";\nimport { fileURLToPath } from "node:url";\n\nimport { selectSources, validateSourceManifest } from "../scripts/lib/manifest.mjs";\n\nconst __dirname = path.dirname(fileURLToPath(import.meta.url));\nconst root = path.resolve(__dirname, "..");\n\ntest("sources manifest parses and validates", async () => {\n  const manifest = JSON.parse(await fs.readFile(path.join(root, "sources/manifest.json"), "utf8"));\n  assert.equal(validateSourceManifest(manifest), true);\n  const enabled = selectSources(manifest, "all");\n  assert.ok(enabled.length > 0);\n  assert.equal(new Set(enabled.map((source) => source.id)).size, enabled.length);\n  assert.ok(enabled.every((source) => source.target.startsWith("external/sources/")));\n  assert.ok(!enabled.some((source) => source.id === "modelcontextprotocol-servers-archived"));\n});\n`,
    "tests/source-download.test.mjs": `import test from "node:test";\nimport assert from "node:assert/strict";\nimport fs from "node:fs/promises";\nimport path from "node:path";\nimport { fileURLToPath } from "node:url";\n\nconst __dirname = path.dirname(fileURLToPath(import.meta.url));\nconst root = path.resolve(__dirname, "..");\n\ntest("source lock has the expected shape", async () => {\n  const realPath = path.join(root, "sources/source-lock.json");\n  const fixturePath = path.join(root, "tests/fixtures/sample-source-lock.json");\n  const targetPath = await fs.access(realPath).then(() => realPath).catch(() => fixturePath);\n  const lock = JSON.parse(await fs.readFile(targetPath, "utf8"));\n  assert.equal(lock.schema_version, "1.0");\n  assert.ok(Array.isArray(lock.sources));\n  assert.ok(Array.isArray(lock.failures));\n  for (const source of lock.sources) {\n    assert.ok(source.id);\n    assert.ok(source.target.startsWith("external/sources/"));\n    assert.ok(source.import_policy);\n  }\n});\n`,
    "tests/source-audit.test.mjs": `import test from "node:test";\nimport assert from "node:assert/strict";\nimport fs from "node:fs/promises";\nimport path from "node:path";\nimport { fileURLToPath } from "node:url";\n\nconst __dirname = path.dirname(fileURLToPath(import.meta.url));\nconst root = path.resolve(__dirname, "..");\n\ntest("source audit markdown is generated", async () => {\n  const auditPath = path.join(root, "docs/source-audit.md");\n  const content = await fs.readFile(auditPath, "utf8");\n  assert.match(content, /^# Source Audit/m);\n  assert.match(content, /^## ecc/m);\n  assert.match(content, /Selected components:/);\n});\n`,
    "tests/sync.test.mjs": `import test from "node:test";\nimport assert from "node:assert/strict";\nimport fs from "node:fs/promises";\nimport path from "node:path";\nimport { fileURLToPath } from "node:url";\nimport { execFile } from "node:child_process";\nimport { promisify } from "node:util";\n\nconst execFileAsync = promisify(execFile);\nconst __dirname = path.dirname(fileURLToPath(import.meta.url));\nconst root = path.resolve(__dirname, "..");\n\ntest("sync generates managed files with the auto-generated header", async () => {\n  await execFileAsync("node", ["scripts/sync.mjs"], { cwd: root });\n  const files = [\n    "AGENTS.md",\n    "docs/agents.md",\n    "docs/trae.md",\n    ".trae/settings.json"\n  ];\n  for (const file of files) {\n    const content = await fs.readFile(path.join(root, file), "utf8");\n    assert.match(content, /AUTO-GENERATED by starter/);\n  }\n});\n`,
    "tests/adapters.test.mjs": `import test from "node:test";\nimport assert from "node:assert/strict";\n\nimport { buildTraeFiles } from "../scripts/adapters/trae.mjs";\n\ntest("trae adapter defines the expected managed outputs", () => {\n  const files = buildTraeFiles();\n  assert.ok(files["AGENTS.md"]);\n  assert.ok(files["docs/agents.md"]);\n  assert.ok(files["docs/trae.md"]);\n  assert.ok(files[".trae/settings.json"]);\n});\n`
  };
}

export async function scaffoldRepository(rootDir, options = {}) {
  const projectName = options.projectName || "starter";
  const projectPurpose = options.projectPurpose || "Trae IDE starter repository";
  const stack = options.stack || "Node.js 20+, plain JavaScript, no runtime dependencies for bootstrap scripts";

  await createRequiredStructure(rootDir);
  await writeJsonIfMissing(rootDir, "sources/manifest.json", getSourceManifest());
  await writeJsonIfMissing(rootDir, "sources/docs-manifest.json", getDocsManifest());

  const files = createStaticFiles({ projectName, projectPurpose, stack });
  const created = [];

  for (const [relativePath, content] of Object.entries(files)) {
    const didCreate = await writeIfMissing(rootDir, relativePath, content);
    if (didCreate) {
      created.push(relativePath);
    }
  }

  return {
    created,
    root: repoRootRelative(rootDir)
  };
}
