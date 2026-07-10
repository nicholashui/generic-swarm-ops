/**
 * Wire project + downloaded assets so Grok Build can discover and use them.
 *
 * Creates:
 * - .grok/asset-registry.json (inventory)
 * - .grok/config.toml (project MCP + plugin path hints)
 * - .grok/hooks/*.json (safe project hooks)
 * - .grok/plugins/* junctions to curated plugin roots
 * - .agents/skills/* junctions for first-party skill categories (discovery)
 * - mcp-configs/optional/grok-mcp-catalog.json (templates; secrets not filled)
 * - Updates hooks/manifest.json
 *
 * Policy:
 * - Does not execute external package install scripts
 * - Does not enable MCP servers that require secrets by default
 * - External trees remain under external/sources/ (reference + discovery)
 */
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");

function exists(p) {
  try {
    fs.accessSync(p);
    return true;
  } catch {
    return false;
  }
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function writeText(rel, content) {
  const abs = path.join(rootDir, rel);
  ensureDir(path.dirname(abs));
  fs.writeFileSync(abs, content.endsWith("\n") ? content : `${content}\n`, "utf8");
  console.log(`wrote ${rel}`);
}

function countSkillMd(dir) {
  if (!exists(dir)) return 0;
  let n = 0;
  const walk = (d) => {
    let entries;
    try {
      entries = fs.readdirSync(d, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      if (e.name === "node_modules" || e.name === ".git") continue;
      const full = path.join(d, e.name);
      if (e.isDirectory()) walk(full);
      else if (e.isFile() && e.name === "SKILL.md") n += 1;
    }
  };
  walk(dir);
  return n;
}

function isJunctionOrDir(p) {
  if (!exists(p)) return false;
  try {
    const st = fs.lstatSync(p);
    return st.isDirectory() || st.isSymbolicLink();
  } catch {
    return false;
  }
}

/** Windows directory junction; falls back to no-op message if unavailable. */
function ensureJunction(linkPath, targetPath) {
  const absLink = path.isAbsolute(linkPath) ? linkPath : path.join(rootDir, linkPath);
  const absTarget = path.isAbsolute(targetPath) ? targetPath : path.join(rootDir, targetPath);
  if (!exists(absTarget)) {
    console.warn(`skip junction (target missing): ${linkPath} -> ${targetPath}`);
    return false;
  }
  if (isJunctionOrDir(absLink)) {
    // Already present — leave in place
    console.log(`junction exists ${path.relative(rootDir, absLink)}`);
    return true;
  }
  ensureDir(path.dirname(absLink));
  if (process.platform === "win32") {
    try {
      execFileSync("cmd", ["/c", "mklink", "/J", absLink, absTarget], {
        stdio: ["ignore", "pipe", "pipe"]
      });
      console.log(`junction ${path.relative(rootDir, absLink)} -> ${path.relative(rootDir, absTarget)}`);
      return true;
    } catch (error) {
      console.warn(`junction failed ${absLink}: ${error.message}`);
      return false;
    }
  }
  try {
    fs.symlinkSync(absTarget, absLink, "dir");
    console.log(`symlink ${path.relative(rootDir, absLink)} -> ${path.relative(rootDir, absTarget)}`);
    return true;
  } catch (error) {
    console.warn(`symlink failed ${absLink}: ${error.message}`);
    return false;
  }
}

const SKILL_PACKS = [
  {
    id: "first-party",
    label: "Project first-party skills",
    path: "skills",
    trust: "first-party",
    policy: "active",
    discovery: [".grok/skills", "skills"]
  },
  {
    id: "ecc",
    label: "ECC / Everything Claude Code",
    path: "external/sources/ecc/skills",
    trust: "curated-only",
    policy: "discoverable",
    notes: "Large pack (~277 skills). Prefer invoke by name; audit before relying on hooks/scripts."
  },
  {
    id: "ecc-agents-skills",
    label: "ECC .agents/skills subset",
    path: "external/sources/ecc/.agents/skills",
    trust: "curated-only",
    policy: "discoverable"
  },
  {
    id: "superpowers",
    label: "Superpowers",
    path: "external/sources/superpowers/skills",
    trust: "reference",
    policy: "discoverable"
  },
  {
    id: "anthropic-skills",
    label: "Anthropic Agent Skills",
    path: "external/sources/anthropic-skills/skills",
    trust: "quarantine",
    policy: "discoverable"
  },
  {
    id: "vercel-agent-skills",
    label: "Vercel Agent Skills",
    path: "external/sources/vercel-agent-skills/skills",
    trust: "reference",
    policy: "discoverable"
  },
  {
    id: "karpathy-guidelines",
    label: "Karpathy guidelines skill",
    path: "external/sources/andrej-karpathy-skills/skills",
    trust: "reference",
    policy: "discoverable"
  }
];

const PLUGIN_ROOTS = [
  {
    id: "ecc",
    label: "ECC plugin root",
    path: "external/sources/ecc",
    junction: ".grok/plugins/ecc"
  },
  {
    id: "superpowers",
    label: "Superpowers plugin root",
    path: "external/sources/superpowers",
    junction: ".grok/plugins/superpowers"
  }
];

const MEMORY_ROOTS = [
  { id: "project-handoff", path: "memory", role: "git-shared continuity" },
  { id: "business-memory", path: "business/memory", role: "product domain memory" },
  { id: "grok-experimental", path: "~/.grok/memory", role: "optional personal cross-session (not in repo)" }
];

function buildRegistry() {
  const skillPacks = SKILL_PACKS.map((pack) => {
    const abs = path.join(rootDir, pack.path);
    return {
      ...pack,
      present: exists(abs),
      skill_md_count: countSkillMd(abs),
      absolute_path: abs
    };
  });

  const plugins = PLUGIN_ROOTS.map((p) => ({
    ...p,
    present: exists(path.join(rootDir, p.path)),
    wired: exists(path.join(rootDir, p.junction))
  }));

  const hooks = {
    project_manifest: "hooks/manifest.json",
    project_hooks_dir: ".grok/hooks",
    external: [
      {
        id: "ecc-hooks",
        path: "external/sources/ecc/hooks",
        present: exists(path.join(rootDir, "external/sources/ecc/hooks")),
        policy: "reference-only-by-default (Claude-oriented; not auto-executed)"
      },
      {
        id: "superpowers-hooks",
        path: "external/sources/superpowers/hooks",
        present: exists(path.join(rootDir, "external/sources/superpowers/hooks")),
        policy: "available via superpowers plugin when trusted/enabled"
      }
    ]
  };

  const mcp = {
    project_minimal: "mcp-configs/minimal.json",
    optional_catalog: "mcp-configs/optional/grok-mcp-catalog.json",
    trae: ".trae/mcp.json",
    ecc_reference: "external/sources/ecc/mcp-configs/mcp-servers.json",
    project_config: ".grok/config.toml"
  };

  return {
    schema_version: "1.0",
    generated_at: new Date().toISOString(),
    harness: "grok-build",
    policy: {
      external_sources: "reference until audited; discoverable via skills paths / plugins",
      secrets: "never committed; MCP needing tokens stay disabled until env provided",
      evolution: "sandbox-only until approved",
      folder_trust: "project hooks/MCP require /hooks-trust or --trust"
    },
    skill_packs: skillPacks,
    plugins,
    hooks,
    memory: MEMORY_ROOTS,
    mcp,
    totals: {
      skill_md: skillPacks.reduce((a, p) => a + (p.skill_md_count || 0), 0),
      skill_packs_present: skillPacks.filter((p) => p.present).length,
      plugins_present: plugins.filter((p) => p.present).length
    }
  };
}

function buildProjectConfigToml(registry) {
  const skillPaths = registry.skill_packs
    .filter((p) => p.present && p.id !== "first-party")
    .map((p) => p.absolute_path.replace(/\\/g, "/"));

  // Also include first-party nested tree so category paths resolve
  const firstParty = path.join(rootDir, "skills").replace(/\\/g, "/");
  const allSkillPaths = [firstParty, ...skillPaths];

  // Project config: MCP + plugin paths (skills paths also written for harnesses that merge project config)
  const lines = [
    "# AUTO-GENERATED by scripts/grok-wire-assets.mjs — do not put secrets here.",
    "# Project-scoped Grok config (MCP / plugins). Skills paths mirrored for discoverability.",
    "",
    "[skills]",
    "paths = [",
    ...allSkillPaths.map((p, i) => `  "${p}"${i < allSkillPaths.length - 1 ? "," : ""}`),
    "]",
    "",
    "[plugins]",
    "paths = [",
    `  "${path.join(rootDir, "external/sources/superpowers").replace(/\\/g, "/")}",`,
    `  "${path.join(rootDir, "external/sources/ecc").replace(/\\/g, "/")}"`,
    "]",
    'enabled = ["superpowers", "ecc"]',
    "",
    "# --- MCP: safe defaults (no secrets required) ---",
    "[mcp_servers.sequential-thinking]",
    'command = "npx"',
    'args = ["-y", "@modelcontextprotocol/server-sequential-thinking"]',
    "enabled = true",
    "",
    "[mcp_servers.memory]",
    'command = "npx"',
    'args = ["-y", "@modelcontextprotocol/server-memory"]',
    "enabled = true",
    "description = \"MCP memory graph (optional; complements repo memory/ and Grok experimental memory)\"",
    "",
    "# --- MCP: templates disabled until credentials exist ---",
    "[mcp_servers.github]",
    'command = "npx"',
    'args = ["-y", "@modelcontextprotocol/server-github"]',
    "enabled = false",
    'env = { GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_PERSONAL_ACCESS_TOKEN}" }',
    "",
    "[mcp_servers.filesystem]",
    'command = "npx"',
    `args = ["-y", "@modelcontextprotocol/server-filesystem", "${rootDir.replace(/\\/g, "/")}"]`,
    "enabled = false",
    "",
    "# Open Design (from Trae mcp.json) — enable only if installed on this machine",
    "[mcp_servers.opendesign]",
    "enabled = false",
    'command = "C:\\\\Users\\\\NH24831\\\\AppData\\\\Local\\\\Programs\\\\Open Design\\\\Open Design.exe"',
    'args = ["C:\\\\Users\\\\NH24831\\\\AppData\\\\Local\\\\Programs\\\\Open Design\\\\resources\\\\app\\\\prebundled\\\\daemon\\\\daemon-cli.mjs", "mcp"]',
    ""
  ];
  return lines.join("\n");
}

function buildMcpCatalog() {
  return {
    schema_version: "1.0",
    note: "Optional MCP catalog for Grok. Copy enabled entries into .grok/config.toml with real secrets via env vars — never commit tokens.",
    servers: {
      "sequential-thinking": {
        transport: "stdio",
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        requires_secrets: false,
        default_enabled: true
      },
      memory: {
        transport: "stdio",
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-memory"],
        requires_secrets: false,
        default_enabled: true
      },
      github: {
        transport: "stdio",
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-github"],
        env: ["GITHUB_PERSONAL_ACCESS_TOKEN"],
        requires_secrets: true,
        default_enabled: false,
        reference: "external/sources/ecc/mcp-configs/mcp-servers.json"
      },
      filesystem: {
        transport: "stdio",
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-filesystem", "<repo-root>"],
        requires_secrets: false,
        default_enabled: false
      },
      "mcp-official-servers": {
        note: "Many official servers live under external/sources/modelcontextprotocol-servers — enable case-by-case",
        path: "external/sources/modelcontextprotocol-servers",
        default_enabled: false
      }
    }
  };
}

function buildSessionStartHook() {
  return {
    hooks: {
      SessionStart: [
        {
          hooks: [
            {
              type: "command",
              command: "node scripts/hooks/session-start-reminder.mjs"
            }
          ]
        }
      ]
    }
  };
}

function buildMemoryRule() {
  return `<!-- AUTO-GENERATED by scripts/grok-wire-assets.mjs -->

# Memory Continuity (Grok)

## Repo memory (shared)

- Read \`memory/handoff.md\` and \`memory/project.md\` at session start.
- Update \`memory/handoff.md\` after major milestones.
- Domain/product memory lives under \`business/memory/\` with provenance rules.

## Grok experimental memory (personal)

Optional personal recall under \`~/.grok/memory/\`. Enable with:

\`\`\`toml
# ~/.grok/config.toml
[memory]
enabled = true
\`\`\`

or \`grok --experimental-memory\`.

Do **not** treat experimental memory as team source of truth.

## MCP memory

When \`[mcp_servers.memory]\` is enabled in \`.grok/config.toml\`, Grok can also use the MCP memory server tools. Prefer provenance-backed writes for business-critical facts.
`;
}

function mirrorSkillsPathsToUserConfig(registry) {
  const userConfig = path.join(process.env.USERPROFILE || process.env.HOME || "", ".grok", "config.toml");
  if (!userConfig || !exists(path.dirname(userConfig))) {
    console.warn("skip user config mirror: ~/.grok missing");
    return;
  }

  const skillPaths = registry.skill_packs
    .filter((p) => p.present)
    .map((p) => p.absolute_path.replace(/\\/g, "/"));

  const markerBegin = "# BEGIN generic-swarm-ops skills paths";
  const markerEnd = "# END generic-swarm-ops skills paths";
  const block = [
    markerBegin,
    "[skills]",
    "paths = [",
    ...skillPaths.map((p, i) => `  "${p}"${i < skillPaths.length - 1 ? "," : ""}`),
    "]",
    markerEnd,
    ""
  ].join("\n");

  let existing = exists(userConfig) ? fs.readFileSync(userConfig, "utf8") : "";
  if (existing.includes(markerBegin) && existing.includes(markerEnd)) {
    existing = existing.replace(
      new RegExp(`${markerBegin}[\\s\\S]*?${markerEnd}\\n?`),
      block
    );
  } else {
    existing = `${existing.trimEnd()}\n\n${block}`;
  }
  fs.writeFileSync(userConfig, existing.endsWith("\n") ? existing : `${existing}\n`, "utf8");
  console.log(`updated ${userConfig} skills paths`);
}

function main() {
  const dryRun = process.argv.includes("--dry-run");
  const skipUser = process.argv.includes("--no-user-config");

  console.log("grok-wire-assets: inventory + wire");
  const registry = buildRegistry();

  if (dryRun) {
    console.log(JSON.stringify(registry, null, 2));
    return;
  }

  // Plugin junctions
  ensureDir(path.join(rootDir, ".grok/plugins"));
  for (const plugin of PLUGIN_ROOTS) {
    ensureJunction(plugin.junction, plugin.path);
  }

  // First-party skill categories as .agents/skills junctions for discovery
  ensureDir(path.join(rootDir, ".agents/skills"));
  const categories = ["planning", "implementation", "testing", "review", "security", "memory", "lifecycle"];
  for (const cat of categories) {
    const src = path.join("skills", cat);
    if (exists(path.join(rootDir, src))) {
      ensureJunction(path.join(".agents/skills", cat), src);
    }
  }

  // Safe hooks
  writeText(
    ".grok/hooks/session-start.json",
    JSON.stringify(buildSessionStartHook(), null, 2)
  );
  writeText(".grok/rules/memory-continuity.md", buildMemoryRule());

  // MCP catalog + project config
  writeText(
    "mcp-configs/optional/grok-mcp-catalog.json",
    JSON.stringify(buildMcpCatalog(), null, 2)
  );
  writeText(".grok/config.toml", buildProjectConfigToml(registry));

  // Recompute wired plugin status after junctions
  registry.plugins = PLUGIN_ROOTS.map((p) => ({
    ...p,
    present: exists(path.join(rootDir, p.path)),
    wired: exists(path.join(rootDir, p.junction))
  }));
  registry.wired_at = new Date().toISOString();

  writeText(".grok/asset-registry.json", JSON.stringify(registry, null, 2));

  // Project hooks manifest
  writeText(
    "hooks/manifest.json",
    JSON.stringify(
      {
        schema_version: "1.0",
        hooks: [
          {
            id: "session-start-reminder",
            harness: "grok",
            path: ".grok/hooks/session-start.json",
            event: "SessionStart"
          }
        ],
        external_reference: [
          "external/sources/ecc/hooks",
          "external/sources/superpowers/hooks"
        ]
      },
      null,
      2
    )
  );

  if (!skipUser) {
    mirrorSkillsPathsToUserConfig(registry);
  }

  console.log(
    `done: ${registry.totals.skill_md} SKILL.md across ${registry.totals.skill_packs_present} packs; plugins wired=${registry.plugins.filter((p) => p.wired).length}`
  );
}

main();
