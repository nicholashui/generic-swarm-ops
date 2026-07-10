# Migrate generic-swarm-ops to Grok Build

**Status:** Executed (dual-harness) — Phases 1–5 applied via sync adapters  
**Date:** 2026-07-09  
**Repo:** `generic-swarm-ops`  
**Source harness:** Trae IDE  
**Target harness:** Grok Build (xAI), dual Trae + Grok support  

---

## 1. Goal

Make this repository fully usable under **Grok Build** while preserving the starter’s single source of truth (`rules/`, `skills/`, `hooks/`, `mcp-configs/`) and all business/governance constraints.

**Success means:**

1. Opening the repo in Grok Build loads correct project rules, skills, and agent roles.
2. Governance, risk tiers, sandbox-only evolution, and untrusted-source policy still hold.
3. Project handoff/memory files remain the continuity surface across sessions and tools.
4. Optionally, `npm run sync` can generate **both** Trae (`.trae/*`) and Grok (`.grok/*`) artifacts.
5. No expectation of one-click Trae chat-history import (summaries only).

**Non-goals (this plan):**

- Rewriting backend/frontend product code for Grok.
- Auto-importing Trae conversation history as live Grok sessions.
- Removing Trae support (default is dual-harness unless later decided otherwise).

---

## 2. Current state

### 2.1 Trae-oriented layout

| Area | Location | Notes |
|------|----------|--------|
| Managed agent rules | `AGENTS.md` (generated) | Currently states “targets Trae IDE only” |
| Trae workspace | `.trae/` | `settings.json`, `rules/`, `agents/`, `commands/`, `mcp.json` |
| Sync pipeline | `scripts/sync.mjs` + `scripts/adapters/trae.mjs` | Only emits Trae-facing files |
| Source of truth | `rules/`, `skills/`, `hooks/`, `mcp-configs/` | Sync regenerates managed outputs |
| Docs | `docs/trae.md`, `docs/agents.md`, `docs/sync.md` | Trae-centric |

### 2.2 Reusable content already in-repo

| Asset | Path | Reuse on Grok |
|-------|------|----------------|
| Constitution & policies | `rules/*.md` | High — surface via `AGENTS.md` / `.grok/rules/` |
| Skills | `skills/**/SKILL.md` | High — add frontmatter; discover via paths or `.grok/skills/` |
| Agent role cards | `.trae/agents/*.md` | Medium — remap to `.grok/agents/` or personas |
| Slash-style commands | `.trae/commands/*.md` | Medium — skills or `.grok/commands/` |
| Project memory | `memory/handoff.md`, `memory/project.md`, reflections | High as files; not auto-indexed by Grok |
| Business memory | `business/memory/*` | Product concern; independent of IDE |
| MCP manifests | `mcp-configs/` | Medium — redeclare for Grok config |
| Hooks | `hooks/` (empty roster today) | Medium when hooks are added |

### 2.3 What does not port automatically

| Asset | Why |
|-------|-----|
| Trae chat history | Different session store; no importer |
| `.trae/settings.json` | Trae-only schema |
| Trae-specific IDE UI bindings | Product-specific |
| Grok experimental memory | Separate store under `~/.grok/memory/` |

---

## 3. Mapping: Trae → Grok Build

| Trae / project concept | Grok Build equivalent | Migration approach |
|------------------------|----------------------|--------------------|
| `AGENTS.md` | `AGENTS.md` (auto-loaded) | Soften Trae-only wording; keep governance bullets |
| `.trae/rules/*.md` | `.grok/rules/*.md` and/or root `AGENTS.md` | Generate from `rules/` via adapter |
| `skills/**/SKILL.md` | `.grok/skills/` or `[skills].paths` | Frontmatter + discovery path |
| `.trae/agents/*.md` | `.grok/agents/*.md` and/or personas | Role cards → agent defs |
| `.trae/commands/*.md` | skills / slash commands | Copy intent; wrap as SKILL.md or command md |
| `.trae/mcp.json` | `~/.grok/config.toml` / project `.grok/config.toml` | Map server entries |
| Project `memory/*.md` | Repo files + optional Grok memory | Keep files; document “read on start” |
| Trae sessions | `~/.grok/sessions/` | New history only; port summaries manually |
| Lifecycle hooks | `.grok/hooks/` | Re-implement when hooks exist |

### 3.1 Grok discovery notes (relevant)

- **Rules:** `AGENTS.md` / `Agents.md` / Claude/Cursor compat names; also `.grok/rules/*.md`.
- **Skills:** `.grok/skills/`, `~/.grok/skills/`, extra dirs via `[skills] paths = [...]`.
- **Agents:** `.grok/agents/`, `~/.grok/agents/`.
- **Memory (experimental):** `~/.grok/memory/`; enable with `[memory] enabled = true` or `--experimental-memory`.
- **Project config:** optional `.grok/config.toml` (MCP, plugins, permissions scope).
- **No native Trae importer** — content must be pointed at or regenerated.

---

## 4. Target architecture

Keep **one source of truth**, two harness adapters:

```text
rules/  skills/  hooks/  mcp-configs/
              │
              ▼
         npm run sync
         ┌────┴────┐
         ▼         ▼
    .trae/*     .grok/*
  (Trae IDE)  (Grok Build)
         │         │
         └────┬────┘
              ▼
     AGENTS.md + docs/*
   (harness-agnostic where possible)
```

**Principles:**

1. Never hand-edit generated blocks without updating the generator.
2. Business policy stays in `rules/` and business artifacts, not in IDE lock-in text.
3. Evolution remains sandbox-only until validated and approved.
4. Downloaded `external/sources/` stay untrusted until audited.

---

## 5. Phased plan

### Phase 0 — Document and baseline (this file)

- [x] Write `migrate_to_grok_build.md` (this plan)
- [x] Confirm dual-harness vs Grok-only preference (default: **dual**)
- [x] Snapshot current sync outputs: `npm run sync:check` / `npm run doctor`

**Exit criteria:** Plan reviewed; approach chosen (minimal vs full adapter).

---

### Phase 1 — Minimal Grok usability (no generator yet)

**Intent:** Use Grok Build immediately with low risk.

| Step | Action | Detail | Done |
|------|--------|--------|------|
| 1.1 | Soften managed rules | Dual-harness wording in `shared.mjs` → regenerated `AGENTS.md` | [x] |
| 1.2 | Bootstrap `.grok/` | Generated via `scripts/adapters/grok.mjs` | [x] |
| 1.3 | Skill discovery | Sync copies skills into `.grok/skills/` | [x] |
| 1.4 | SKILL frontmatter | Added to each `skills/**/SKILL.md` | [x] |
| 1.5 | Handoff contract | In `AGENTS.md` + `.grok/rules/session-start.md` | [x] |
| 1.6 | Optional Grok memory | Documented in `memory/README.md` (opt-in; not forced) | [x] |
| 1.7 | Smoke check | `npm run sync`, `npm test`, `sync:check`, `doctor` | [x] |

**Skills inventory to frontmatter-upgrade:**

- `skills/planning/business-orchestration`
- `skills/implementation/workflow-dna`
- `skills/testing/evaluation-harness`
- `skills/review/governance-review`
- `skills/security/agentic-red-team`
- `skills/memory/memory-stewardship`
- `skills/lifecycle/evolution-sandbox`
- `skills/lifecycle/process-intelligence`

**Exit criteria:** New Grok session in this repo follows governance rules and can invoke project skills without re-pasting context.

---

### Phase 2 — Content port (agents, commands, MCP)

| Step | Action | Detail | Done |
|------|--------|--------|------|
| 2.1 | Agent roster | Shared roster → `.grok/agents/<id>.md` | [x] |
| 2.2 | Commands | `.grok/commands/*`; Trae keeps `sync-trae` alias | [x] |
| 2.3 | MCP | `mcp-configs/minimal.json` empty; no secrets generated (defer until servers defined) | [x] deferred |
| 2.4 | Hooks | `hooks/manifest.json` empty; no hooks emitted yet | [x] deferred |
| 2.5 | Docs | `docs/grok.md`, `docs/sync.md`, README, package.json | [x] |

**Agent roster to port (from Trae adapter):**

- Control: business-orchestrator, evolution-manager, evaluation-harness, governance-officer, security-red-team, memory-steward, tool-permission-broker, incident-commander  
- Learning/process: expert-shadow, cognitive-task-analyst, process-miner, task-mining-agent, conformance-agent, bottleneck-analyzer, causal-improvement-agent, knowledge-distiller, knowledge-curator  
- Engineering: developer  

**Exit criteria:** Grok can run the same validation workflows via agents/skills/commands that Trae documents today.

---

### Phase 3 — Proper dual sync adapter

| Step | Action | Detail | Done |
|------|--------|--------|------|
| 3.1 | Add `scripts/adapters/grok.mjs` | Plus `shared.mjs` roster | [x] |
| 3.2 | Wire `scripts/sync.mjs` | Merge Trae + Grok; collision check | [x] |
| 3.3 | Generated outputs | Rules, agents, skills, commands, docs | [x] |
| 3.4 | Tests | `tests/sync.test.mjs`, `tests/adapters.test.mjs` | [x] |
| 3.5 | CI / doctor | `sync:check` covers `.grok` paths; doctor unchanged | [x] |

**Suggested generated tree:**

```text
.grok/
  rules/
    starter.md
    business-operating-system.md
  agents/
    business-orchestrator.md
    ...
  skills/                 # optional: mirrors or thin wrappers
  hooks/                  # when defined
  config.toml             # only if safe defaults; secrets never generated
docs/grok.md
AGENTS.md                 # harness-agnostic managed block
```

**Exit criteria:** `npm run sync` and `npm run sync:check` keep Trae and Grok artifacts consistent from the same sources.

---

### Phase 4 — Memory and history continuity

| Step | Action | Detail |
|------|--------|--------|
| 4.1 | Handoff discipline | Keep `memory/handoff.md` as cross-tool continuity (progress, blockers, next steps) |
| 4.2 | Project memory | Use `memory/project.md` for durable conventions and decisions |
| 4.3 | Trae history export (manual) | For critical past Trae threads: summarize decisions into handoff/project memory |
| 4.4 | Grok session hygiene | Use `/flush` after important sessions; `/remember` for durable facts |
| 4.5 | Optional Grok memory | Enable only if team wants automatic cross-session recall; still version-control handoff files for shared truth |

**Important distinction:**

| Kind | Location | Shared via git? | Auto-migrated from Trae? |
|------|----------|-----------------|---------------------------|
| Project handoff | `memory/` | Yes | No (manual summary) |
| Business memory | `business/memory/` | Yes (policy-dependent) | N/A |
| Grok experimental memory | `~/.grok/memory/` | No (user machine) | No |
| Grok sessions | `~/.grok/sessions/` | No | No |

**Exit criteria:** A new Grok session can recover project state from repo files without needing Trae open.

---

### Phase 5 — Hardening and optional Trae de-emphasis

| Step | Action | Detail |
|------|--------|--------|
| 5.1 | Package metadata | Update `package.json` description from “for Trae IDE” to dual/Grok as appropriate |
| 5.2 | README / starter docs | Onboarding path for Grok Build |
| 5.3 | Policy review | Confirm risk tiers, approval gates, and evolution sandbox still enforced under Grok workflows |
| 5.4 | Optional Trae freeze | If Grok-only: keep adapter but stop requiring Trae outputs in check mode (feature flag) |

**Exit criteria:** Docs and checks match the chosen long-term harness strategy.

---

## 6. Recommended AGENTS.md policy (target wording)

Managed block should be harness-agnostic, for example:

```markdown
- This project supports agent harnesses: Trae IDE and Grok Build.
- Prefer generated/synced config under `.trae/` and `.grok/` over hand-edited IDE files.
- Downloaded repositories under external/sources/ are reference material until audited.
- Business workflows require provenance, risk tiers, and human gates where defined.
- Evolution proposals must remain sandbox-only until validated and approved.
- At session start, read memory/handoff.md and memory/project.md when present.
- Regenerate managed files with `npm run sync`.
```

---

## 7. Skill frontmatter template

Apply to each project skill before relying on auto-invocation:

```markdown
---
name: memory-stewardship
description: >
  Maintain provenance, retention, and quality across episodic, semantic,
  procedural, and evaluation memory. Use when editing business memory,
  provenance fields, or retention policy.
---

# Memory Stewardship

...existing body...
```

---

## 8. Risks and mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Dual generators drift | Trae and Grok disagree on policy | Single source (`rules/`, agent roster in adapter); shared tests |
| Hand-edited `.grok` overwritten | Lost local tweaks | Mark generated files; put personal overrides in `~/.grok/` or gitignored local files |
| Skills without frontmatter | Weak auto-invocation | Phase 1 frontmatter pass |
| Assuming chat history migrated | Lost context | Explicit handoff summaries only |
| Secrets in MCP config | Leak risk | Never commit tokens; use env vars in Grok config |
| Grok memory treated as shared source of truth | Team inconsistency | Keep `memory/*.md` as shared; Grok memory is personal/experimental |
| Breaking Trae users | Regression | Dual adapter default; keep `npm run sync` emitting `.trae/*` |

---

## 9. Validation checklist

After each phase:

```bash
npm run doctor
npm run sync:check          # after dual adapter: includes .grok paths
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
npm test
```

Grok-side checks:

- [ ] `grok inspect` shows root `AGENTS.md` (and `.grok/rules` if present)
- [ ] Project skills appear and are invocable
- [ ] Agent/persona roles available if Phase 2 done
- [ ] Handoff file guidance followed in a fresh session
- [ ] No policy regression (external sources untrusted; evolution sandboxed)

---

## 10. Decision log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Harness strategy | Dual Trae + Grok (default) | Preserve existing Trae users; add Grok without fork |
| Source of truth | `skills/`, `scripts/adapters/shared.mjs`, rules content in generators | Single roster, two harness projections |
| Shared continuity | Repo `memory/*.md` | Git-shared; tool-agnostic |
| Trae chat import | Manual summaries only | No portable session format |
| Skills on Grok | Copy into `.grok/skills/` on sync | Project-local discovery without user global config |
| MCP / hooks | Defer until manifests non-empty | Avoid empty/secret-prone config files |
| Implementation order | Phases 1–5 in one pass | Dual adapter landed with content |

_Update this table when decisions change._

---

## 11. Open questions

1. **Dual forever or Grok-primary later?** Default dual until Trae usage is confirmed zero.
2. **Skills location:** symlink/copy into `.grok/skills/` vs `[skills].paths` only?
3. **Should `npm run sync` generate a project `.grok/config.toml`** with MCP stubs, or leave MCP to user global config?
4. **Which Trae conversations** are critical enough to summarize into `memory/`?
5. **Enable Grok experimental memory by default** for this project, or opt-in only?

---

## 12. Immediate next actions (after plan approval)

1. Approve dual-harness default (or override).
2. Execute **Phase 1**: AGENTS wording, `.grok` bootstrap, skill frontmatter, handoff contract.
3. Smoke-test a Grok session against `npm run doctor` and one business validation skill.
4. Then implement **Phase 3** adapter if dual sync is desired (can interleave with Phase 2 content).

---

## 13. References

| Doc / path | Why |
|------------|-----|
| `AGENTS.md` | Current managed agent rules |
| `docs/sync.md` | Sync layer behavior |
| `docs/trae.md` | Generated Trae workspace notes |
| `scripts/adapters/trae.mjs` | Source of agent roster + Trae generation |
| `scripts/sync.mjs` | Sync entrypoint |
| `memory/README.md` | Project memory purpose |
| `skills/manifest.json` | Skill categories |
| Grok user guide: project rules, skills, memory, sessions, hooks, MCP | Harness behavior |

---

## Appendix A — Phase effort sketch

| Phase | Effort (approx.) | Dependencies |
|-------|------------------|--------------|
| 0 Plan | Done | — |
| 1 Minimal usability | Small | Plan approval |
| 2 Agents/commands/MCP | Medium | Phase 1 |
| 3 Dual sync adapter | Medium | Phase 1; can parallel Phase 2 |
| 4 Memory continuity | Small–medium | Manual Trae summaries |
| 5 Hardening / docs | Small | Phases 1–3 |

## Appendix B — Out of scope reminders

- Product backend memory APIs (`business/memory`, backend memory service) are not IDE migration work.
- Pinokio/external source trees under `external/sources/` remain reference-only until audited.
- No automatic promotion of evolution sandbox variants.
