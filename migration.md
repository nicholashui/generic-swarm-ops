# Migration Plan: va-agent-swarm → generic-swarm-ops (standalone corpus)

**Version:** 1.1  
**Date:** 2026-07-13  
**Status:** **COMPLETE** (knowledge-standalone + N3 pack DoD) — see **`MIGRATION_COMPLETE.md`**  
**Repos:** `C:\Project\va-agent-swarm` → `C:\Project\generic-swarm-ops`  
**Deep plan (preferred SoT):** **`migration_plan.md` v2.0** — full 325-file inventory, copy feasibility, phases P0–P7, gates; §16 execution record.  
**Problem statement:** Every `business/video/agents/*/SPEC.md` was an L0 stub that only **referred** to `va-agent-swarm/study/agents.md`. Goal: after migration, **generic-swarm-ops can operate and be developed without `va-agent-swarm` present on disk** for design content.

---

## 0. Why “refer only” is dangerous

| Risk | Impact |
|------|--------|
| External path missing | Agent SPECs become empty shells; N3 “retention” is name-only |
| Context-window limits | Models skip `va-agent-swarm/...` links; never load deep tables |
| Dual SoT drift | va updates never land in generic; MAP/provenance rot |
| Onboarding | New contributors clone only generic → incomplete video domain |
| Offline / airgap | Host cannot reconstruct agent intents from pack alone |

**Non-negotiable outcome:** All **operational and design knowledge** required to run/improve the video Domain Pack lives **under `business/video/` (or pack-scoped host docs)**, with provenance notes — **not** as “go read the other repo.”

---

## 1. Current state (measured 2026-07-13)

### 1.1 generic-swarm-ops (host + pack shell)

| Asset | State |
|-------|--------|
| `business/video/agents/*` | **114** dirs; inventory `PASS count=114 n3=complete` |
| `SPEC.md` × 114 | ~37 KB total (~330 B each); **114/114** cite `va-agent-swarm/study/agents.md` only |
| `agent_spec.json` | ALC fields + tools stubs; provenance still points at va paths |
| Workflows | **14** thin DNA JSON (spine, A–J, e2e, LQR, delivery) |
| Knowledge | Minimal seed (`knowledge/seeds/spine-orchestration.md`) — explicitly “not 68-chapter corpus” |
| Process docs | `PROCESSES.md`, `process_coverage.json`, `docs/*` pack-linked stubs |
| va as submodule | **No** `.gitmodules`; **no** `external/va-agent-swarm` |

### 1.2 va-agent-swarm (upstream corpus, ~11 MB)

| Path | Role | Approx size |
|------|------|-------------|
| `study/agents.md` (+ hk, scripts) | **Authoritative 114-agent tables** (responsibilities, tools, critique bus, patterns) | ~75 KB (+ variants) |
| `study/SYSTEM_REFERENCE.md` | System map, 6-phase, orchestration | ~42 KB (+ variants) |
| `study/*_specification*.md` | Deep functional/technical (aesthetics, research, optimization, GCA, intent, RAG, coding, psych, screenwriter, podcast, LLM usage, …) | bulk of study |
| `study/agent_loop*.md` | Agent loop v1–v3 | medium |
| `study/*workflow*.md` | Human + AI production workflows, LQR narrative | medium |
| `study/workflows/*.svg` | A–J + LQR diagrams | ~0.3 MB |
| `study/ui/*` | Agent mgmt UI, project creation, redesign notes | ~1 MB |
| `study/reference/how_to_build_a_video_agent_system/` | **68** chapter `.txt` | ~4.2 MB |
| `plan/planner_agent_v2.*` | Planner designs | small |
| Root `project_starter_*`, `agent_loop_creator_*`, `inital_task*` | Starters / meta | small |

**Total va tree ~10.9 MB** — small enough to **copy in full** if desired; policy below prefers **structured pack layout** over dumping at repo root.

---

## 2. Target state (standalone generic)

```text
business/video/
  agents/<pack_id>/
    agent_spec.json          # already present; provenance → in-pack paths
    SPEC.md                  # FULL local content (no required external open)
    sources/                 # optional per-agent excerpts (if shared doc split)
  corpus/                    # NEW: mirrored va knowledge (in-pack SoT)
    README.md                # index + license/provenance
    MANIFEST.json            # file list, sha256, source path, copied_at
    study/                   # copy of va/study (see scope tiers)
    plan/                    # copy of va/plan
    root-docs/               # selected root md from va (starters optional)
  knowledge/seeds/           # indexed retrieval seeds (derived from corpus)
  workflows/                 # DNA (already) + optional SVG mirrors
  docs/                      # process maps (already) expanded from corpus
  MAP.md / ROSTER.json / PROCESSES.md / process_coverage.json
```

**Rule:** Any `source_refs` / SPEC “source:” line must resolve to a path **inside this repo** (e.g. `business/video/corpus/study/agents.md#…`). Optional note: “Originally from va-agent-swarm @ commit …” for history only — **not** required for reading content.

---

## 3. Scope tiers (what to copy)

User requirement: **ALL related information** so va may be **missing**. That implies **Tier C (full study corpus)** as default for completion. Tiers allow phased execution without losing the end goal.

| Tier | Name | Copy set | Standalone? |
|------|------|----------|-------------|
| **A** | Agent tables only | `study/agents.md` (+ `agents_hk.md` if wanted), extract **per-agent** into each `SPEC.md` | Partial — deep modules still external |
| **B** | Runtime-critical corpus | A + SYSTEM_REFERENCE, human/ai workflows, LQR docs, agent_loop v3, workflow SVGs, planner plan docs, deep specs that map to pack modules | Strong for DNA/runtime design |
| **C** | **Full related corpus (recommended end state)** | Entire `va-agent-swarm/study/**` + `va-agent-swarm/plan/**` + essential root starters | **Yes** — va disk optional |
| **D** | Optional scripts/i18n | `*.script.txt`, `*.script_hk.txt`, `*_zh*`, `*_hk.md` | Nice for media; not required for host runtime |

**Default completion bar for this plan:** **Tier C** (+ optional D).

### 3.1 Explicit exclusions (still “related” but optional)

| Exclude by default | Why |
|--------------------|-----|
| `.DS_Store`, `__pycache__`, node_modules | Noise |
| Binary IDE junk | Noise |
| Duplicative script languages if Tier C EN-only first | Size; can copy in Tier D |
| Rebuilding va’s aspirational LangGraph/Temporal **as second host** | N1/N2: host remains generic; content is knowledge + DNA, not a second stack |

### 3.2 License / provenance

- Record original repo URL + **git commit SHA** of va at copy time in `corpus/MANIFEST.json`.
- Preserve file headers; add pack banner: “Copied into Domain Pack for standalone operation; do not delete for N3.”
- Do not claim ownership rewrite; treat as **upstream import**.

---

## 4. Mapping: va assets → generic locations

| va path | generic destination | Consumer |
|---------|---------------------|----------|
| `study/agents.md` | `corpus/study/agents.md` + **split into** each `agents/<pack_id>/SPEC.md` | Coding agents, humans, optional retrieval |
| `study/agents_hk.md` | `corpus/study/agents_hk.md` | HK docs |
| `study/SYSTEM_REFERENCE.md` | `corpus/study/SYSTEM_REFERENCE.md` | Process/DNA authors |
| `study/*specification*.md` | `corpus/study/` (same names) | Deep module agents |
| `study/agent_loop*.md` | `corpus/study/` | Loop DNA / ALC design |
| `study/*workflow*.md` | `corpus/study/` + refresh `docs/process-maps.md` | Process index |
| `study/workflows/*.svg` | `corpus/study/workflows/` **and/or** `workflows/diagrams/` | DNA provenance |
| `study/ui/**` | `corpus/study/ui/` | FE domain routes (P2) |
| `study/reference/**` | `corpus/study/reference/` | Knowledge seeds / RAG |
| `plan/**` | `corpus/plan/` | Planner agent depth |
| Root `project_starter_*`, `agent_loop_creator_*` | `corpus/root-docs/` (optional) | Historical starters |

### 4.1 Per-agent SPEC.md target shape (after migration)

Each of 114 SPECs must be **self-contained**:

```markdown
# <Name> (va_id N)

## Identity
pack_id, category, status, n3_maturity

## Responsibility
(from agents.md table row)

## Knowledge distillation sources
(local paths under business/video/corpus/... only)

## Quality / critique
Self-quality criteria, surpass-human signal, accepts critique from, comments on

## Tools (design-time)
(from agents.md; map to host tool ids where stubs exist)

## Architecture pattern
(from agents.md)

## Runtime binding (generic host)
agent_spec.json summary, DNA steps that reference this agent, standby route

## Local corpus index
Links to in-pack deep specs (relative paths)

## Provenance
Copied from va-agent-swarm@<sha> study/agents.md row N · date
```

**No required link** of the form `C:\Project\va-agent-swarm\...` or `va-agent-swarm/study/...` for primary content.

---

## 5. Phased execution plan

### Phase M0 — Inventory & freeze (0.5 day)

1. Record `va` git rev: `git -C C:\Project\va-agent-swarm rev-parse HEAD` → `corpus/SOURCE_COMMIT.txt`.
2. Generate file list + sizes + sha256 of every file to copy → draft `MANIFEST.json`.
3. Diff against existing pack; confirm 114 pack_id ↔ va_id MAP still 1:1.
4. **Exit:** freeze commit SHA; no silent copy without manifest.

### Phase M1 — Bulk corpus copy (Tier C) (0.5–1 day)

1. Script: `scripts/business/migrate_va_corpus.py` (to be created at execution):
   - Copy `study/**` → `business/video/corpus/study/`
   - Copy `plan/**` → `business/video/corpus/plan/`
   - Optional root docs → `corpus/root-docs/`
   - Write `MANIFEST.json` (path, sha256, bytes, source_relpath)
2. Add `business/video/corpus/README.md` (how to use; N3 standalone rule).
3. Update `.gitignore` only if secrets appear (should not).
4. **Exit:** open `business/video/corpus/study/agents.md` offline; va folder renamed/absent still works.

### Phase M2 — Expand all 114 SPEC.md from agents.md (1–2 days)

1. Parser: read agents.md category tables (rows 1–114).
2. Map name → pack_id via `ROSTER.json` / `MAP.md` (do not invent ids).
3. Rewrite each `SPEC.md` with full row content + local links.
4. Update `agent_spec.json` provenance `source_refs` to in-pack paths; set `spec_depth: "from_agents_md_v1"`.
5. **Exit:** grep finds **zero** required `va-agent-swarm/` primary refs under `business/video/agents/**/SPEC.md` (optional historical footnote OK if content duplicated).

### Phase M3 — Deep-spec binding (1 day)

1. Build `corpus/AGENT_DEEP_SPEC_INDEX.json`: pack_id → list of local deep-spec files (heuristic + manual table for meta agents).
2. Append “Local corpus index” section to each SPEC from index.
3. For shared modules (GCA, research, optimization), store once under `corpus/study/` and link many agents — **do not** duplicate megabytes per agent.
4. **Exit:** spine agents (orchestrator, planner, director, screenwriter, aiqaconsistency, …) have ≥1 local deep-spec link that opens in-repo.

### Phase M4 — Knowledge seeds for retrieval (1–2 days)

1. Chunk high-value corpus (SYSTEM_REFERENCE, agent tables, workflow md, selected reference chapters) into `knowledge/seeds/` with provenance.
2. Prefer Tier-0 small seeds for CI; larger optional packs behind flag.
3. Wire existing knowledge index path if present; otherwise document manual load.
4. **Exit:** at least spine seeds no longer say “68 chapters later.”

### Phase M5 — Process & DNA provenance (0.5–1 day)

1. Copy SVGs to `workflows/diagrams/` or corpus workflows.
2. Update `PROCESSES.md` / DNA `provenance.source_refs` to local paths.
3. Align `docs/process-maps.md` and `docs/deep-spec-modules.md` to cite corpus only.
4. **Exit:** process_coverage paths remain valid; no va-only process.

### Phase M6 — Verification gates (mandatory)

| Gate | Command / check |
|------|-----------------|
| Inventory still 114 | `python scripts/business/inventory_check.py` → PASS + n3=complete |
| Standalone SPEC content | Script: each SPEC.md ≥ N bytes / contains “Responsibility” section |
| No dangling primary refs | `rg "va-agent-swarm" business/video/agents -g SPEC.md` → only optional provenance lines, or zero |
| Manifest integrity | re-hash corpus files vs MANIFEST.json |
| Offline smoke | Temporarily ignore va path; open 5 random SPECs + agents.md from corpus |
| Unit suite | `cd backend && python -m pytest app/tests/unit -q` green |
| Optional | New unit test `test_video_corpus_standalone.py`: MANIFEST exists; agents.md present; sample pack_id SPEC contains responsibility text |

### Phase M7 — Docs & policy (0.5 day)

1. Update `business/video/README.md`: corpus is SoT; va optional upstream.
2. Update `adoption.md` / `adoption_hk.md` changelog note: corpus migration.
3. Update `docs/domain-packs.md` + handoff.
4. Policy: **future va updates** land as pack PRs (copy + manifest bump), never “just link.”

---

## 6. Automation design (execution scripts)

### 6.1 `scripts/business/migrate_va_corpus.py`

```text
args:
  --va-root C:\Project\va-agent-swarm
  --dest business/video/corpus
  --tier A|B|C|D
  --dry-run
  --update-manifest
behavior:
  copy files; preserve relative structure under study/ and plan/
  compute sha256; write MANIFEST.json + SOURCE_COMMIT.txt
  never delete existing agent_spec.json
```

### 6.2 `scripts/business/expand_video_agent_specs.py`

```text
args:
  --roster business/video/ROSTER.json
  --agents-md business/video/corpus/study/agents.md
  --agents-dir business/video/agents
  --write
behavior:
  parse markdown tables; match pack_id; rewrite SPEC.md
  fail closed if any of 114 rows missing or unmapped
```

### 6.3 `scripts/business/check_video_corpus_standalone.py`

```text
exit 0 iff:
  corpus/study/agents.md exists
  all 114 SPEC.md pass min-content rules
  inventory_check still passes
```

---

## 7. Risk & size

| Risk | Mitigation |
|------|------------|
| Repo bloat | ~11 MB total — acceptable; Tier D scripts optional |
| Duplicate i18n | EN first (Tier C); HK/zh scripts Tier D |
| Stale corpus | MANIFEST + SOURCE_COMMIT; PR process for va pulls |
| Overwrite good SPECs | expand script skips if `spec_depth: manual` flag set |
| Parsing agents.md tables brittle | Golden test: 114 rows extracted; snapshot pack_id map |
| Legal | Keep provenance; do not strip copyrights |

---

## 8. Success criteria (migration done)

1. **`C:\Project\va-agent-swarm` can be deleted/unmounted** and a developer can still:
   - Read every agent’s role/tools/critique design from `business/video/agents/*/SPEC.md` or `corpus/study/agents.md`
   - Read system/process design from `corpus/study/`
   - Run inventory + unit suite + spine DNA path on generic host  
2. No SPEC depends on opening an **external** path for primary content.  
3. `MANIFEST.json` proves copy integrity.  
4. N3 inventory still **114 n3=complete**.

---

## 9. Out of scope for this migration plan

- Implementing real Sora/Veo (stubs stay until media phase)
- Activating all 114 to live `active` L2 in one go
- Replacing generic host with va’s LangGraph stack
- Auto-translating all HK scripts (Tier D optional)

---

## 10. Recommended next action

1. Approve this plan (Tier **C** end state).  
2. Implement Phase M0–M1 scripts and run dry-run.  
3. M2 expand all SPECs.  
4. M6 gates + optional `test_video_corpus_standalone.py`.  
5. Changelog `adoption.md` / handoff: “video corpus standalone.”

**Do not** keep shipping “deep SPEC deferred — see va-agent-swarm” as the permanent N3 story.

---

## 11. Traceability

| Concern | Link |
|---------|------|
| Strategy N1/N3 | `adoption.md` v2.4 |
| Wave shell already present | `planning/improvement/wave-0`…`wave-5` |
| User problem | SPEC.md refer-only; context window |
| Source | `C:\Project\va-agent-swarm` |
| Destination | `business/video/` inside `C:\Project\generic-swarm-ops` |

---

*End of migration plan v1.0 — execute only after explicit GO on phases M0+.*
