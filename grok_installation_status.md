# Grok Build installation status

**Project:** `generic-swarm-ops`  
**Date:** 2026-07-09  
**Harness:** Grok Build (dual-harness with Trae IDE retained)  
**Commands used:** `npm run grok:wire`, `npm run sync`, `npm run doctor`

---

## Executive summary

| Area | Status | Usable in Grok? | Notes |
|------|--------|-----------------|-------|
| **First-party skills** | Wired | **Yes** | 8 skills in `.grok/skills/` + source `skills/` |
| **Downloaded skill packs** | Wired | **Yes (discoverable)** | 363 `SKILL.md` across 7 packs via skill paths |
| **Plugins (ECC, Superpowers)** | Wired | **Yes (after trust/enable)** | Junctions under `.grok/plugins/` |
| **Hooks** | Partial | **Yes (project safe hook)** | SessionStart reminder; ECC hooks reference-only |
| **Memory** | Wired | **Yes** | Repo `memory/` + rules + optional MCP/Grok memory |
| **MCP** | Partial | **Yes (safe defaults)** | sequential-thinking + memory enabled; secret MCP off |
| **Agents / commands** | Wired | **Yes** | Generated under `.grok/agents/`, `.grok/commands/` |
| **Trae IDE** | Unchanged | **Yes** | Still generated via `npm run sync` |

**Bottom line:** Project and downloaded skills/plugins are **discoverable and usable** from Grok. External content stays under `external/sources/` with **audit policy**; no bulk “execute untrusted code” promotion. Folder trust (`/hooks-trust`) may be required for project hooks/MCP.

---

## What was done

1. Dual-harness baseline (earlier): `scripts/adapters/{shared,trae,grok}.mjs`, `.grok/*` + `.trae/*` via `npm run sync`.
2. **Asset wiring** (`scripts/grok-wire-assets.mjs`, `npm run grok:wire`):
   - Inventory → `.grok/asset-registry.json`
   - Project MCP/plugins/skills config → `.grok/config.toml`
   - Plugin junctions → `.grok/plugins/ecc`, `.grok/plugins/superpowers`
   - First-party discovery junctions → `.agents/skills/*`
   - Safe SessionStart hook → `.grok/hooks/session-start.json`
   - Memory continuity rule → `.grok/rules/memory-continuity.md`
   - Optional MCP catalog → `mcp-configs/optional/grok-mcp-catalog.json`
   - User skill paths → `~/.grok/config.toml` (BEGIN/END generic-swarm-ops block)
3. Regenerated managed docs/agents/skills with `npm run sync`.

---

## Skills

### First-party (active)

| Skill | Source | Grok copy |
|-------|--------|-----------|
| business-orchestration | `skills/planning/...` | `.grok/skills/business-orchestration/` |
| workflow-dna | `skills/implementation/...` | `.grok/skills/workflow-dna/` |
| evaluation-harness | `skills/testing/...` | `.grok/skills/evaluation-harness/` |
| governance-review | `skills/review/...` | `.grok/skills/governance-review/` |
| agentic-red-team | `skills/security/...` | `.grok/skills/agentic-red-team/` |
| memory-stewardship | `skills/memory/...` | `.grok/skills/memory-stewardship/` |
| evolution-sandbox | `skills/lifecycle/...` | `.grok/skills/evolution-sandbox/` |
| process-intelligence | `skills/lifecycle/...` | `.grok/skills/process-intelligence/` |

All first-party skills have YAML `name` + `description` frontmatter.

### Downloaded packs (discoverable)

| Pack | Path | SKILL.md count | Trust / policy |
|------|------|----------------|----------------|
| ECC | `external/sources/ecc/skills` | 277 | curated-only |
| ECC agents skills | `external/sources/ecc/.agents/skills` | 37 | curated-only |
| Superpowers | `external/sources/superpowers/skills` | 14 | reference |
| Anthropic skills | `external/sources/anthropic-skills/skills` | 17 | quarantine |
| Vercel agent skills | `external/sources/vercel-agent-skills/skills` | 9 | reference |
| Karpathy guidelines | `external/sources/andrej-karpathy-skills/skills` | 1 | reference |
| **Total (incl. first-party)** | | **363** | |

**How Grok finds them:**

1. Project `.grok/skills/` (first-party copies)
2. `.agents/skills/*` junctions (first-party categories)
3. `[skills].paths` in **project** `.grok/config.toml` and **user** `~/.grok/config.toml` (all pack roots)

**Not bulk-installed into `~/.grok/skills/`** — discovery by path avoids copying thousands of files and keeps policy clear.

### User global Grok skills (unchanged)

`check-work`, `code-review`, `create-skill`, `docx`, `help`, `imagine`, `pptx`, `xlsx` under `~/.grok/skills/`.

---

## Plugins

| Plugin root | Junction | Present | Wired |
|-------------|----------|---------|-------|
| ECC | `.grok/plugins/ecc` → `external/sources/ecc` | Yes | Yes |
| Superpowers | `.grok/plugins/superpowers` → `external/sources/superpowers` | Yes | Yes |

Configured in `.grok/config.toml`:

```toml
[plugins]
paths = [ ".../external/sources/superpowers", ".../external/sources/ecc" ]
enabled = ["superpowers", "ecc"]
```

**Operator action:** In Grok TUI use `/plugins` to confirm enablement; grant project trust if hooks/MCP from plugins are blocked.

**Anthropic official plugins** (`external/sources/anthropic-claude-plugins-official`) remain **reference-only** (quarantine, not auto-junctioned) — enable case-by-case after review.

---

## Hooks

| Hook | Location | Status |
|------|----------|--------|
| SessionStart reminder | `.grok/hooks/session-start.json` → `scripts/hooks/session-start-reminder.mjs` | **Active (project)** |
| Project manifest | `hooks/manifest.json` | Updated |
| ECC hooks | `external/sources/ecc/hooks` | Reference only (Claude-oriented bootstrap; not auto-run) |
| Superpowers hooks | `external/sources/superpowers/hooks` | Available when Superpowers plugin trusted/enabled |

**Trust:** Project hooks need `/hooks-trust` (or `grok --trust`) the first time. Same gate applies to project MCP/LSP.

---

## Memory

| Layer | Path | Role | Status |
|-------|------|------|--------|
| Project handoff | `memory/handoff.md` | Cross-session / cross-tool continuity | Present; session rule loads it |
| Project context | `memory/project.md` | Durable project facts | Present; dual-harness noted |
| Memory guide | `memory/README.md` | How to use | Updated previously |
| Grok rule | `.grok/rules/memory-continuity.md` | Instructs Grok | Wired |
| Business memory | `business/memory/*` | Product domain | Unchanged (provenance rules apply) |
| Grok experimental | `~/.grok/memory/` | Personal optional | Opt-in via `[memory] enabled = true` |
| MCP memory server | `.grok/config.toml` `[mcp_servers.memory]` | Tool-based memory | **Enabled** (no secrets) |

**Team source of truth remains git-backed `memory/`**, not experimental Grok memory.

---

## MCP

### Enabled by default (no secrets)

| Server | Config | Purpose |
|--------|--------|---------|
| sequential-thinking | `.grok/config.toml` | Chain-of-thought tool |
| memory | `.grok/config.toml` | MCP memory graph |

### Present but disabled (need credentials or local install)

| Server | Why disabled |
|--------|----------------|
| github | Needs `GITHUB_PERSONAL_ACCESS_TOKEN` |
| filesystem | Optional broad FS access |
| opendesign | Local Trae Open Design path; enable if installed |

### Catalogs / references

| Asset | Path |
|-------|------|
| Optional catalog | `mcp-configs/optional/grok-mcp-catalog.json` |
| Minimal project MCP | `mcp-configs/minimal.json` (empty servers object) |
| ECC MCP templates | `external/sources/ecc/mcp-configs/mcp-servers.json` |
| Trae MCP (local) | `.trae/mcp.json` (opendesign) |
| Official MCP servers tree | `external/sources/modelcontextprotocol-servers` (reference) |

**Never commit tokens.** Enable secret MCP by setting env vars and flipping `enabled = true` in `.grok/config.toml` (or user config).

---

## Agents & commands (generated)

| Kind | Path | Count (approx.) |
|------|------|-----------------|
| Agents | `.grok/agents/*.md` | 18 business + developer |
| Commands | `.grok/commands/*.md` | bootstrap, validate-business, run-evals, governance-check, security-check, sync-workspace, … |
| Rules | `.grok/rules/*.md` | starter, business OS, session-start, memory-continuity |

Regenerate with `npm run sync`.

---

## File map (Grok-facing)

```text
.grok/
  asset-registry.json     # inventory (source of truth for status)
  config.toml             # skills paths, plugins, MCP
  hooks/session-start.json
  rules/                  # starter, BOS, session-start, memory-continuity
  agents/                 # role cards
  commands/               # slash-style command docs
  skills/                 # first-party SKILL.md copies
  plugins/
    ecc/                  # junction → external/sources/ecc
    superpowers/          # junction → external/sources/superpowers
.agents/skills/           # junctions → skills/<category>
memory/                   # handoff + project continuity
mcp-configs/optional/grok-mcp-catalog.json
scripts/grok-wire-assets.mjs
scripts/hooks/session-start-reminder.mjs
```

---

## Operator checklist (first session)

1. Open repo root in Grok Build.
2. Run `/hooks-trust` if project hooks/MCP are skipped.
3. Confirm skills: `/skills` (expect first-party + large external list).
4. Confirm plugins: `/plugins` (ecc, superpowers).
5. Confirm MCP: `/mcps` (sequential-thinking, memory).
6. Read `memory/handoff.md`.
7. Optional: enable experimental memory in `~/.grok/config.toml`:
   ```toml
   [memory]
   enabled = true
   ```
8. Optional: enable GitHub MCP after setting `GITHUB_PERSONAL_ACCESS_TOKEN`.

---

## Maintenance

| Action | Command |
|--------|---------|
| Re-inventory + re-wire after downloads | `npm run grok:wire` |
| Dry-run inventory only | `npm run grok:wire:check` |
| Regenerate agents/skills/docs | `npm run sync` |
| Verify managed files exist | `npm run sync:check` |
| Health | `npm run doctor` |

After `npm run sources:download` or adding packs, re-run **`npm run grok:wire`**.

---

## Policy & risk

| Policy | Applied |
|--------|---------|
| Dual-harness Trae + Grok | Yes |
| `external/sources` not auto-executed | Yes (discovery only; no postinstall run) |
| Secrets not in git | Yes (MCP secrets disabled / env placeholders) |
| Evolution sandbox-only | Unchanged |
| ECC import_policy curated-only | Discovery wired; no bulk “approved production import” |
| Quarantined Anthropic skills | Discoverable; treat as untrusted until reviewed |

**Risk note:** Registering ~360 skills increases description surface in Grok. Prefer invoking **named** skills. Disable noisy packs by removing their path from `[skills].paths` or using `[skills] disabled = [...]`.

---

## Gaps / follow-ups

| Item | Priority | Action |
|------|----------|--------|
| Enable Open Design MCP | Low | Set `opendesign.enabled = true` if app installed |
| GitHub MCP | Medium | Token + enable |
| Curated ECC subset (agent-sort daily pack) | Medium | Reduce 277 → daily set after review |
| Full ECC hooks port | Low | Only if needed; currently Claude-specific |
| Anthropic plugins marketplace wire | Low | Audit then optional junction under `.grok/plugins/` |
| Folder trust CI/docs | Low | Document in onboarding |

---

## Verification snapshot

```text
npm run grok:wire   → 363 SKILL.md, 7 packs, 2 plugins wired
npm run sync        → AGENTS.md + .grok/* + .trae/* regenerated
npm run doctor      → Result: OK (Windows symlink privilege FAIL is expected; junctions used)
```

| Artifact | Exists |
|----------|--------|
| `.grok/asset-registry.json` | Yes |
| `.grok/config.toml` | Yes |
| `.grok/hooks/session-start.json` | Yes |
| `.grok/plugins/ecc` | Yes (junction) |
| `.grok/plugins/superpowers` | Yes (junction) |
| `.agents/skills/*` | Yes (junctions) |
| `~/.grok/config.toml` skills block | Yes |

---

## Related docs

- `migrate_to_grok_build.md` — migration plan (executed dual-harness)
- `docs/grok.md` — generated Grok workspace notes
- `docs/sync.md` — sync dual adapter
- `docs/source-audit.md` — per-source quarantine / import policy
- `.grok/asset-registry.json` — machine-readable inventory

---

*Report generated as part of Grok asset wiring. Re-run `npm run grok:wire` and refresh this file after major source updates.*
