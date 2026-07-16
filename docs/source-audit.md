# Source Audit

## ecc

- Name: ECC / Everything Claude Code
- URL: https://github.com/affaan-m/ECC.git
- Target: external/sources/ecc
- Status: downloaded
- Commit: ed387446052dfbc6b52de149406b70efa65edc59
- Branch: main
- License files: LICENSE
- Package files: package-lock.json, package.json
- Priority: required
- Tier: core
- Quarantine: false
- Import policy: curated-only
- Purpose: Primary reference source for extracting skills, agents, commands, hooks, rules, MCP conventions, and security-scanner patterns into curated Trae outputs.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: suspicious postinstall script found. | Review required: MCP-related files may request broad filesystem or network access.

## anthropic-claude-code

- Name: Anthropic Claude Code
- URL: https://github.com/anthropics/claude-code.git
- Target: external/sources/anthropic-claude-code
- Status: downloaded
- Commit: c39cb0f14bfe8bb519bae5bfc55add6867c5e2ab
- Branch: main
- License files: LICENSE.md
- Package files: none
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Official Claude Code repository for docs, issues, release notes, and compatibility references.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Review required: MCP-related files may request broad filesystem or network access.

## anthropic-claude-code-action

- Name: Anthropic Claude Code Action
- URL: https://github.com/anthropics/claude-code-action.git
- Target: external/sources/anthropic-claude-code-action
- Status: downloaded
- Commit: 1298632ce7736903d02a1435002705aa2a594a6c
- Branch: main
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Official GitHub Action patterns for Claude Code automation, PR review, issue workflows, and CI integration.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## anthropic-skills

- Name: Anthropic Agent Skills
- URL: https://github.com/anthropics/skills.git
- Target: external/sources/anthropic-skills
- Status: downloaded
- Commit: 9d2f1ae187231d8199c64b5b762e1bdf2244733d
- Branch: main
- License files: none
- Package files: none
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: curated-only
- Purpose: Official Agent Skills examples, specification, templates, and skill packaging patterns.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## anthropic-claude-plugins-official

- Name: Anthropic Claude Plugins Official
- URL: https://github.com/anthropics/claude-plugins-official.git
- Target: external/sources/anthropic-claude-plugins-official
- Status: downloaded
- Commit: b5eddebc6444d73108941ee698f25fa8759b8710
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Official Claude Code plugin marketplace structure and plugin manifest examples.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## openai-codex

- Name: OpenAI Codex CLI
- URL: https://github.com/openai/codex.git
- Target: external/sources/openai-codex
- Status: downloaded
- Commit: e7efc5b04b78095801c9025574c20cbc409419d8
- Branch: main
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Official Codex CLI source and AGENTS.md behavior reference.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## google-gemini-cli

- Name: Google Gemini CLI
- URL: https://github.com/google-gemini/gemini-cli.git
- Target: external/sources/google-gemini-cli
- Status: downloaded
- Commit: 3ff5ba20fc1ad7d867218bbdb34756eb54d6eccb
- Branch: main
- License files: LICENSE
- Package files: package-lock.json, package.json
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Official Gemini CLI source kept as a reference input for adapting MCP, settings, and command concepts into Trae-compatible workflows.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## opencode

- Name: OpenCode
- URL: https://github.com/anomalyco/opencode.git
- Target: external/sources/opencode
- Status: downloaded
- Commit: 888c4cb50476aaecaad48e6a448759da3040ed2e
- Branch: dev
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: OpenCode source for AGENTS.md, opencode config, agents, MCP, and plugin compatibility.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: suspicious postinstall script found.

## modelcontextprotocol-servers

- Name: Model Context Protocol Servers
- URL: https://github.com/modelcontextprotocol/servers.git
- Target: external/sources/modelcontextprotocol-servers
- Status: downloaded
- Commit: d31124c982401739917fd817c2a59db344529c16
- Branch: main
- License files: LICENSE
- Package files: package-lock.json, package.json
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Current MCP server examples and server discovery references.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## modelcontextprotocol-registry

- Name: Model Context Protocol Registry
- URL: https://github.com/modelcontextprotocol/registry.git
- Target: external/sources/modelcontextprotocol-registry
- Status: downloaded
- Commit: 29e32c39dcb5e0e2b43974089d959fcc4794eb6d
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: MCP registry references for discovering MCP servers safely.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## github-mcp-server

- Name: GitHub MCP Server
- URL: https://github.com/github/github-mcp-server.git
- Target: external/sources/github-mcp-server
- Status: downloaded
- Commit: 8ac674b0562bf2d2cccaea2965d32fcb2511cdbe
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: official
- Quarantine: true
- Import policy: reference-only
- Purpose: Official GitHub MCP server for GitHub issue, PR, repo, workflow, and code search integration.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## agents-md

- Name: AGENTS.md Specification
- URL: https://github.com/openai/agents.md.git
- Target: external/sources/agents-md
- Status: downloaded
- Commit: d1ac7f063d20e70015ed6732664049ae4ba9d74e
- Branch: main
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: standard
- Quarantine: true
- Import policy: reference-only
- Purpose: AGENTS.md standard/reference for repository instructions used inside Trae-oriented projects.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## andrej-karpathy-skills

- Name: Andrej Karpathy Skills
- URL: https://github.com/forrestchang/andrej-karpathy-skills.git
- Target: external/sources/andrej-karpathy-skills
- Status: downloaded
- Commit: 2c606141936f1eeef17fa3043a72095b4765b9c2
- Branch: main
- License files: none
- Package files: none
- Priority: required
- Tier: behavior-rules
- Quarantine: false
- Import policy: curated-only
- Purpose: Karpathy-style behavioral rules: think before coding, simplicity, surgical changes, goal-driven execution.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## andrej-karpathy-skills-cursor-vscode

- Name: Andrej Karpathy Skills for Cursor and VS Code
- URL: https://github.com/mbeijen/andrej-karpathy-skills-cursor-vscode.git
- Target: external/sources/andrej-karpathy-skills-cursor-vscode
- Status: downloaded
- Commit: a51d67704dc30e4adc9b322676548fa03fb078a7
- Branch: main
- License files: none
- Package files: none
- Priority: required
- Tier: behavior-rules
- Quarantine: true
- Import policy: curated-only
- Purpose: Cursor/VS Code rule-file adaptation of Karpathy-style behavior rules.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## claude-mem

- Name: Claude Mem
- URL: https://github.com/thedotmack/claude-mem.git
- Target: external/sources/claude-mem
- Status: downloaded
- Commit: f5633c1f84181673896c038cbe285131c6d669a3
- Branch: main
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: memory
- Quarantine: true
- Import policy: reference-only
- Purpose: Persistent memory architecture reference. Must not install automatically.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: suspicious postinstall script found.

## superpowers

- Name: Superpowers
- URL: https://github.com/obra/superpowers.git
- Target: external/sources/superpowers
- Status: downloaded
- Commit: d884ae04edebef577e82ff7c4e143debd0bbec99
- Branch: main
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: skills
- Quarantine: true
- Import policy: curated-only
- Purpose: Composable software-development skill methodology for multiple coding agents.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## claude-code-best-practice

- Name: Claude Code Best Practice
- URL: https://github.com/shanraisshan/claude-code-best-practice.git
- Target: external/sources/claude-code-best-practice
- Status: downloaded
- Commit: 0c9123288eb8f16d06bd69421556a610967eab59
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: best-practices
- Quarantine: true
- Import policy: curated-only
- Purpose: Community best-practice source for Claude Code agents, commands, skills, hooks, and workflows.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## awesome-claude-code

- Name: Awesome Claude Code
- URL: https://github.com/hesreallyhim/awesome-claude-code.git
- Target: external/sources/awesome-claude-code
- Status: downloaded
- Commit: 8633f29f7297d8816a39571fdb5f094cedd8a7b3
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: discovery
- Quarantine: true
- Import policy: reference-only
- Purpose: Curated discovery list for Claude Code skills, hooks, commands, plugins, workflows, and tooling.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## awesome-agent-skills

- Name: Awesome Agent Skills
- URL: https://github.com/VoltAgent/awesome-agent-skills.git
- Target: external/sources/awesome-agent-skills
- Status: downloaded
- Commit: c97eda5e3406670f3285c6bf9eb7639a7ecc03cc
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: discovery
- Quarantine: true
- Import policy: reference-only
- Purpose: Cross-agent discovery list for Claude Code, Codex, Gemini CLI, Cursor, and related skills.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## wshobson-agents

- Name: Claude Code Subagents by wshobson
- URL: https://github.com/wshobson/agents.git
- Target: external/sources/wshobson-agents
- Status: downloaded
- Commit: b6af3711058190e4b5c5274b9758498fe626ec5a
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: agents
- Quarantine: true
- Import policy: curated-only
- Purpose: Community Claude Code subagent definitions for specialist-agent patterns.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## vercel-agent-skills

- Name: Vercel Labs Agent Skills
- URL: https://github.com/vercel-labs/agent-skills.git
- Target: external/sources/vercel-agent-skills
- Status: downloaded
- Commit: f8a72b9603728bb92a217a879b7e62e43ad76c81
- Branch: main
- License files: none
- Package files: none
- Priority: required
- Tier: skills
- Quarantine: true
- Import policy: curated-only
- Purpose: Frontend, React, Next.js, and deployment-oriented agent skill patterns.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## awesome-cursorrules

- Name: Awesome Cursor Rules
- URL: https://github.com/PatrickJS/awesome-cursorrules.git
- Target: external/sources/awesome-cursorrules
- Status: downloaded
- Commit: b044f956f021b6e8877f16781bcfc466a6a120e9
- Branch: main
- License files: LICENSE
- Package files: package.json
- Priority: required
- Tier: cursor
- Quarantine: true
- Import policy: reference-only
- Purpose: Cursor rule examples and discovery reference.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## cursor-security-rules

- Name: Cursor Security Rules
- URL: https://github.com/matank001/cursor-security-rules.git
- Target: external/sources/cursor-security-rules
- Status: downloaded
- Commit: ebbe0abd48ba08cadfaa3723ebfdf4914081e682
- Branch: main
- License files: LICENSE
- Package files: none
- Priority: required
- Tier: security
- Quarantine: true
- Import policy: curated-only
- Purpose: Security-focused Cursor rule examples.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: No additional notes.

## itgoyo-awesome-agent-skills

- Name: itgoyo Awesome Agent Skills
- URL: https://github.com/itgoyo/awesome-agent-skills.git
- Target: external/sources/itgoyo-awesome-agent-skills
- Status: downloaded
- Commit: 34fbc07ef168a1238408cdbf622fa1e36e0b70af
- Branch: master
- License files: none
- Package files: none
- Priority: optional
- Tier: discovery
- Quarantine: true
- Import policy: reference-only
- Purpose: Additional discovery index for popular agent-skills repositories.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## itgoyo-awesome-claude-code-skills

- Name: itgoyo Awesome Claude Code Skills
- URL: https://github.com/itgoyo/awesome-claude-code-skills.git
- Target: external/sources/itgoyo-awesome-claude-code-skills
- Status: downloaded
- Commit: 5db38294d495729f0cc348b34578f20a3b0682af
- Branch: main
- License files: none
- Package files: none
- Priority: optional
- Tier: discovery
- Quarantine: true
- Import policy: reference-only
- Purpose: Top-starred Claude Code ecosystem repository index.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## subinium-awesome-claude-code

- Name: subinium Awesome Claude Code
- URL: https://github.com/subinium/awesome-claude-code.git
- Target: external/sources/subinium-awesome-claude-code
- Status: downloaded
- Commit: 2f1af568069ef985c40674a55decb540e782ede5
- Branch: main
- License files: none
- Package files: none
- Priority: optional
- Tier: discovery
- Quarantine: true
- Import policy: reference-only
- Purpose: Additional curated Claude Code discovery list.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found.

## modelcontextprotocol-servers-archived

- Name: Model Context Protocol Servers Archived
- URL: https://github.com/modelcontextprotocol/servers-archived.git
- Target: external/sources/modelcontextprotocol-servers-archived
- Status: not-downloaded
- Commit: n/a
- Branch: n/a
- License files: none
- Package files: none
- Priority: archived
- Tier: historical
- Quarantine: true
- Import policy: never-import
- Purpose: Historical MCP reference only. Do not download or use by default because it is archived.
- Selected components: none yet
- Rejected components: bulk import rejected until human review
- Security notes: Unsafe for automatic import: no license file found. | Unsafe for automatic import: source is archived.

