import {
  AGENT_RULES_MARKDOWN,
  BUSINESS_AGENTS,
  HARNESS_COMMANDS,
  VALIDATION_COMMANDS_MARKDOWN,
  buildAgentContent
} from "./shared.mjs";
import { generatedHeader, managedBlock } from "../lib/report.mjs";

export function buildTraeFiles() {
  const header = generatedHeader();
  const agentList = BUSINESS_AGENTS.map((agent) => `- ${agent.title}`).join("\n");

  const files = {
    "AGENTS.md": `${header}

# AGENTS

${managedBlock("AGENT RULES", AGENT_RULES_MARKDOWN)}
`,
    "docs/agents.md": `${header}

# Agents

${managedBlock(
  "AGENT RULES",
  `## Supported Workflows

- Starter bootstrap validation
- Source download and audit
- Business workflow validation
- Governance, security, and evolution sandbox checks

## Harnesses

- Trae IDE (\`.trae/\`)
- Grok Build (\`.grok/\`)

## Control And Learning Agents

${agentList}

## Validation Commands

${VALIDATION_COMMANDS_MARKDOWN}`
)}
`,
    "docs/trae.md": `${header}

# Trae Workspace

${managedBlock(
  "TRAE SETUP",
  `## Generated Paths

- \`.trae/settings.json\`
- \`.trae/rules/starter.md\`
- \`.trae/rules/business-operating-system.md\`
- \`.trae/agents/*.md\`
- \`.trae/commands/*.md\`

## Policy

Downloaded sources are not imported or executed automatically.
Business workflows remain bounded by risk tiers, approval gates, audit logging, and sandboxed evolution.
This repository is dual-harness: Trae IDE and Grok Build share the same rules, skills, and agent roster via \`npm run sync\`.`
)}
`,
    ".trae/settings.json": `${header}
${JSON.stringify(
  {
    ai: { model: "default", temperature: 0.2 },
    rules: { enabled: true, directory: ".trae/rules" },
    agents: { directory: ".trae/agents" },
    commands: { directory: ".trae/commands" }
  },
  null,
  2
)}
`,
    ".trae/rules/starter.md": `${header}

# Starter Rules

- Use manifests as the source of truth.
- Treat external/sources as untrusted input.
- Prefer reproducible generation via npm scripts.
- Dual-harness: keep Trae (\`.trae/\`) and Grok (\`.grok/\`) in sync with \`npm run sync\`.
`,
    ".trae/rules/business-operating-system.md": `${header}

# Business Operating System Rules

- Use bounded workflow DNA with explicit agents, tools, guardrails, verification, and rollback.
- Require provenance for business rules, decision cards, workflows, and evaluation cards.
- Enforce autonomy risk tiers and human approval triggers before execution.
- Never mutate production directly from the evolution sandbox.
`,
    ".trae/agents/developer.md": `${header}

# Developer Agent

## Role

Implement and maintain the repository according to starter.md and structure.md.

## Workflow

1. Run doctor.
2. Download and audit sources.
3. Initialize and validate business artifacts.
4. Sync harness workspace files (\`npm run sync\`).
5. Run governance, security, eval, and test checks.
`
  };

  for (const agent of BUSINESS_AGENTS) {
    files[`.trae/agents/${agent.id}.md`] = `${header}

${buildAgentContent(agent)}`;
  }

  // Keep legacy Trae command name "sync-trae" as alias of sync-workspace.
  const traeCommands = HARNESS_COMMANDS.map(([name, command]) =>
    name === "sync-workspace" ? ["sync-trae", command] : [name, command]
  );

  for (const [name, command] of traeCommands) {
    files[`.trae/commands/${name}.md`] = `${header}

# /${name}

Run:

\`\`\`bash
${command}
\`\`\`
`;
  }

  return files;
}
