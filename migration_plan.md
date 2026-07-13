# Migration Plan (Deep): Copy **ALL** va-agent-swarm information into generic-swarm-ops

**Document:** `migration_plan.md`  
**Version:** 2.0  
**Date:** 2026-07-13  
**Status:** **Executed 2026-07-13** (P0–P2, P3 index, P6 gates, P7 docs) — see completion note §16  
**Supersedes for depth:** `migration.md` v1.0 (kept as short brief; **this file is the detailed SoT**)  

| | Path |
|--|------|
| **Source** | `C:\Project\va-agent-swarm` (git `main` @ `965d85e378c936f1aba1c39cad8158f97b1bdaf6` as of study) |
| **Dest host** | `C:\Project\generic-swarm-ops` |
| **Dest pack root** | `business/video/` |

---

## 0. Problem (why this plan exists)

| Today in generic | Risk |
|------------------|------|
| All **114** `business/video/agents/*/SPEC.md` are ~300-byte stubs | Content is only a **pointer** to `va-agent-swarm/study/agents.md` |
| Coding agents have limited context windows | They **do not** reliably open external repos / long hop chains |
| N3 claims “full roster retained” | Catalog dirs exist, but **design knowledge** still lives outside the host |
| User requirement | Even if **va-agent-swarm is missing/deleted**, generic must still hold **all related information** and remain developable/runnable |

**Definition of done (user intent):**

> After migration, a developer or coding agent with **only** `generic-swarm-ops` can read every agent’s design, every process/system doc, every deep specification, every workflow diagram, every UI study doc, every reference chapter, and every planner/starter doc that today lives in va — **without** opening `C:\Project\va-agent-swarm`.

---

## 1. Deep source inventory (va-agent-swarm)

### 1.1 Totals (content only, excluding `.git`)

| Metric | Value |
|--------|-------|
| **Content files** | **325** |
| **Content bytes** | **~10.87 MB** (~11.4 MB if counting junk) |
| **With `.git` object pack** | ~15 MB total tree (**.git is NOT copied**) |
| **Largest content file** | ~208 KB (`study/reference/.../chapter_35.txt`) |
| **Non-ASCII path names** | **0** |
| **Space in paths** | **0** (safe for scripts) |
| **Empty content files** | **0** (inital_task\* are small but non-zero) |

**Conclusion:** Full corpus copy is **technically cheap** (≪ normal monorepo media). No LFS required. No path-encoding blockers on Windows.

### 1.2 Top-level layout to copy

```text
va-agent-swarm/
  plan/                          # 10 files — planner_agent v2.0/v2.1 (+ scripts, hk)
  study/                         # 276 content files (+ .gitignore)
    reference/how_to_build_.../  # 68 chapter .txt
    ui/                          # 42 files (md/svg/scripts)
    workflows/                   # 19 files (16 svg + py/ps1 helpers)
    *.md / *.script*.txt         # specs, agents, workflows, loops, …
  agent_loop_creator_v1*         # 10 files (md + scripts + hk/zh)
  agent_loop_creator_v2*         # 10 files
  project_starter_0.1 … 0.5*     # 25 files (5 versions × 5 variants)
  inital_task*                   # 4 files (typo “inital” preserved)
```

### 1.3 File taxonomy (must all be included for “ALL”)

| Class | Count (approx) | Extensions | Copy? |
|-------|----------------|------------|-------|
| English markdown specs | ~37 core EN + tables | `.md` | **YES** |
| HK Traditional Chinese md | ~36 | `*_hk.md` | **YES** |
| Spoken scripts (EN/HK/ZH) | ~111 under study + more at root | `.script.txt`, `.script_hk.txt`, `.script_zh.txt` | **YES** |
| Reference book chapters | **68** | `.txt` under `study/reference/` | **YES** |
| Workflow diagrams | **16+ SVG** (+ structure svg/html) | `.svg`, `.html` | **YES** |
| UI study pack | **42** | md/svg/scripts | **YES** |
| Planner plans | **10** | under `plan/` | **YES** |
| Root starters / creators | **~49** | md + scripts | **YES** |
| Helper scripts | **2 py + 1 ps1** | under `study/workflows/` | **YES** (tools, not host runtime) |
| study `.gitignore` | 1 | | **YES** (as `corpus/study/.gitignore` or merge note) |
| `.DS_Store` | 2 | | **NO** (noise) |
| `.git/**` | pack/idx/sample | | **NO** (use commit pin instead) |

### 1.4 Filename quirks (preserve bytes; do not “fix” on copy)

| Quirk | Examples | Migration rule |
|-------|----------|----------------|
| Typos in upstream names | `podcast_agent_functional_specifcation*` (missing ‘i’) | **Copy as-is**; index both real + typo names |
| Typos | `video_generation_techology_*`, `inital_task*` | **Copy as-is** |
| Version fan-out | `project_starter_0.1`…`0.5` × languages | **Copy all** |
| Multi-language | `_hk`, `.script_zh`, `.script_hk` | **Copy all** (user: ALL information) |

### 1.5 Content already partially present in generic (must not block copy)

| generic today | Overlap with va |
|---------------|-----------------|
| 114 agent dirs + stub SPEC + agent_spec.json | **No** full agents.md content |
| 14 DNA JSON | Thin stubs; va has **SVG + narrative**, not same files |
| `knowledge/seeds/spine-orchestration.md` | Short; **does not** replace 68 chapters |
| `docs/process-maps.md`, deep-spec-modules | Stubs |

**Rule:** Corpus copy is **additive** under `business/video/corpus/`. Never delete DNA/agent_spec during import. SPEC rewrite is a **second step** that **embeds** content, not replaces the corpus file.

---

## 2. Target layout (everything landable inside generic)

```text
business/video/
  corpus/                              # FULL va knowledge mirror (SoT for docs)
    README.md
    SOURCE_COMMIT.txt                  # va git SHA at copy time
    SOURCE_URL.txt
    MANIFEST.json                      # every file: relpath, sha256, bytes, mtime
    COPY_LOG.jsonl                     # per-file ok/skip/error
    study/                             # ← mirror va/study/**
    plan/                              # ← mirror va/plan/**
    root/                              # ← all va root *.md / *.script*.txt
      agent_loop_creator_v1.md
      project_starter_0.1.md
      … (all root content files)
  agents/<pack_id>/
    agent_spec.json                    # existing; update provenance only
    SPEC.md                            # EXPANDED self-contained (from agents.md row + links)
  knowledge/
    seeds/                             # optional derived chunks for retrieval
    index/                             # optional later
  workflows/
    *.dna.json                         # existing host DNA
    diagrams/                          # optional symlink-or-copy of corpus/study/workflows/*.svg
  docs/                                # pack docs pointing ONLY to corpus/ paths
  ROSTER.json / MAP.md / PROCESSES.md / process_coverage.json / …
```

### 2.1 Why both `corpus/` **and** expanded `SPEC.md`?

| Store | Purpose |
|-------|---------|
| **`corpus/` full tree** | Bit-for-bit fidelity; answers “ALL information”; scripts/i18n/SVG/reference intact |
| **Expanded `SPEC.md`** | Agent-local entrypoint for coding agents (no hop to find “id 53” in a 75 KB table) |

Coding agents read **SPEC.md first**; humans/search use **corpus/**. Neither depends on va disk.

### 2.2 Path rewrite policy (critical for “could copy / could use”)

After copy, **all primary citations** inside pack docs must be **repo-relative**:

| Forbidden as primary | Required primary |
|----------------------|------------------|
| `C:\Project\va-agent-swarm\...` | `business/video/corpus/study/agents.md` |
| `va-agent-swarm/study/...` (as only source) | Same under `business/video/corpus/...` |
| GitHub raw URL only | Local path first; URL optional historical |

Optional footer on every file:

```text
<!-- provenance: copied from va-agent-swarm@965d85e path=study/agents.md -->
```

---

## 3. Completeness matrix — “ALL” means these buckets are 100% copied

| # | Bucket | Source glob | Dest | Files (study snapshot) | Gate |
|---|--------|-------------|------|------------------------|------|
| B1 | Agent roster tables | `study/agents.md`, `agents_hk.md`, agents scripts | `corpus/study/` | 5 | SHA match |
| B2 | System reference | `study/SYSTEM_REFERENCE*` | `corpus/study/` | 5 | present |
| B3 | Production workflows | `study/*video_production_workflow*`, LQR narrative | `corpus/study/` | all matches | count |
| B4 | Deep agent specs | `study/*specification*`, `*specifcation*` (typo) | `corpus/study/` | all matches | count |
| B5 | Agent loops | `study/agent_loop*` | `corpus/study/` | all matches | count |
| B6 | Thinking / build / tech notes | `thinking_model*`, `system_build_plan*`, `video_generation_*`, `complex_problem_*`, `knowledge_router*`, `llm_usage*` | `corpus/study/` | all | count |
| B7 | Reference book | `study/reference/**` | `corpus/study/reference/` | **68** | count==68 |
| B8 | UI corpus | `study/ui/**` | `corpus/study/ui/` | **42** | count==42 |
| B9 | Workflow diagrams + helpers | `study/workflows/**` | `corpus/study/workflows/` | **19** | count==19 |
| B10 | Planner | `plan/**` | `corpus/plan/` | **10** | count==10 |
| B11 | Root creators | `agent_loop_creator_v1*`, `v2*` | `corpus/root/` | **20** | count==20 |
| B12 | Root starters | `project_starter_0.*` | `corpus/root/` | **25** | count==25 |
| B13 | Root tasks | `inital_task*` | `corpus/root/` | **4** | count==4 |
| B14 | study meta | `study/.gitignore` | `corpus/study/` | 1 | optional |
| — | **TOTAL content** | all except junk/git | `corpus/` | **325** | **manifest count==325** |

**Exclude only:**

| Path | Reason |
|------|--------|
| `.git/**` | Replaced by `SOURCE_COMMIT.txt` |
| `.DS_Store` | OS junk |
| (none else) | User: ALL related information |

---

## 4. Feasibility: “could copy” checklist (engineering)

| Concern | Finding | How plan ensures copy works |
|---------|---------|------------------------------|
| Size | ~11 MB | Single `shutil.copy2` / robocopy; no LFS |
| Encoding | UTF-8 md/txt; SVG XML | Copy binary-safe; open as UTF-8 in expanders |
| Windows paths | No illegal chars; path length OK | Use `pathlib`; store POSIX relpaths in MANIFEST |
| Concurrent write | Agent SPECs + corpus | Two-phase: (1) corpus freeze (2) SPEC expand |
| Partial failure | Network N/A (local disk) | Manifest + resume: skip matching sha256 |
| Idempotent re-run | Required | `--force` overwrites corpus; SPECs skip if `spec_lock: true` |
| Git of generic | Large PR | One commit “import video corpus @ SHA”; LFS not needed |
| CI checkout | Fine | No submodule recursion |
| Antivirus lock | Rare on md | Retry 3× on PermissionError |
| Junction/symlink | None observed | Copy as regular files |
| Executable scripts | `.py`/`.ps1` | Copy only; do not execute on import |

---

## 5. Phase plan (execution order)

### Phase P0 — Freeze source (30 min)

1. `git -C C:\Project\va-agent-swarm rev-parse HEAD` → `SOURCE_COMMIT.txt`
2. `git -C … status -sb` must be clean or dirty state recorded
3. Enumerate **325** files → write `MANIFEST.planned.json` (expected set)
4. **Exit:** planned count = 325; SHA pinned

### Phase P1 — Bulk binary-safe copy (1–2 hr)

1. Implement `scripts/business/migrate_va_corpus.py`:
   ```text
   --va-root <path>
   --dest business/video/corpus
   --include-all-content   # default true
   --exclude .git,.DS_Store
   --dry-run
   ```
2. Algorithm:
   - Walk source files
   - Skip exclude set
   - Map:
     - `study/**` → `corpus/study/**`
     - `plan/**` → `corpus/plan/**`
     - root files → `corpus/root/<filename>`
   - `copy2` preserve mtime
   - sha256 each dest file
   - append `COPY_LOG.jsonl`
3. Write final `MANIFEST.json`
4. **Exit gates:**
   - `MANIFEST.json` entries == 325
   - Every planned path exists on disk
   - Spot-check sha256 of `agents.md`, `SYSTEM_REFERENCE.md`, chapter_01.txt, A-viral-hook.svg

### Phase P2 — Expand 114 SPEC.md (core fix for coding agents) (2–4 hr)

1. Implement `scripts/business/expand_video_agent_specs.py`
2. Parse `corpus/study/agents.md` category tables (rows 1–114)
3. Join with `ROSTER.json` (`va_id` ↔ `pack_id`)
4. For each agent write full SPEC (responsibility, knowledge sources, quality, tools, architecture, local links)
5. Update `agent_spec.json`:
   - `provenance.source_refs` → in-pack paths only
   - `spec_depth`: `agents_md_embedded`
6. **Exit gates:**
   - 114/114 SPEC.md contain section `## Responsibility`
   - min size e.g. ≥ 800 bytes each (tune after sample)
   - `rg "va-agent-swarm/study" business/video/agents --glob SPEC.md` → 0 matches (or only inside HTML comment provenance)

### Phase P3 — Internal link map & deep-spec index (2 hr)

1. Build `corpus/INDEX.md` (human TOC of corpus)
2. Build `corpus/AGENT_DOC_MAP.json`:
   ```json
   {
     "video.orchestrator": {
       "va_id": 53,
       "agents_md_anchor": "…",
       "related_corpus": [
         "study/SYSTEM_REFERENCE.md",
         "study/agent_loop_v3.md",
         "…"
       ]
     }
   }
   ```
3. Heuristic + manual table for deep specs (research → video.webresearch, aesthetics → critics, GCA → creative, etc.)
4. Inject “Related local documents” into each SPEC from map
5. **Exit:** every pack_id has ≥1 related_corpus entry (shared docs OK)

### Phase P4 — Knowledge seeds (optional but recommended) (2–4 hr)

1. Generate retrieval-friendly seeds from corpus (SYSTEM_REFERENCE sections, agents tables split, workflows)
2. Place under `business/video/knowledge/seeds/` with provenance → corpus paths
3. Replace spine seed text that says “68 chapters later”
4. **Exit:** seeds only cite `business/video/corpus/...`

### Phase P5 — Process / DNA provenance rewrite (1–2 hr)

1. Copy or reference SVGs in `workflows/diagrams/` (or link paths in DNA provenance to corpus)
2. Rewrite DNA `provenance.source_refs` and PROCESSES.md links to corpus
3. Refresh `docs/process-maps.md` / `deep-spec-modules.md`
4. **Exit:** `process_coverage.json` paths still resolve; no va-only

### Phase P6 — Standalone verification suite (mandatory)

| ID | Check | Pass rule |
|----|-------|-----------|
| V1 | Inventory | `python scripts/business/inventory_check.py` → PASS 114 n3=complete |
| V2 | Manifest completeness | 325 files present + sha256 match |
| V3 | Offline corpus | With va path unavailable, open `corpus/study/agents.md` |
| V4 | SPEC quality | `check_video_specs_standalone.py` all 114 |
| V5 | No external primary refs | grep policy on agents/ + video docs |
| V6 | Backend unit | `pytest app/tests/unit -q` green |
| V7 | New unit test | `test_video_corpus_standalone.py` drives real scripts/filesystem (not hardcode) |

### Phase P7 — Documentation & policy (1 hr)

1. `business/video/README.md` — corpus is pack SoT; va optional upstream
2. `business/video/corpus/README.md` — how to refresh from va
3. `adoption.md` / `adoption_hk.md` changelog note
4. `memory/handoff.md` pointer
5. Policy: **future va updates** = re-run migrate with new SHA + PR; never “just add a refer”

---

## 6. Tooling specifications (to implement at execution)

### 6.1 `scripts/business/migrate_va_corpus.py`

- **Input:** va root, dest, exclude list  
- **Output:** full tree + MANIFEST + COPY_LOG + SOURCE_COMMIT  
- **Must support:** dry-run, resume, force  
- **Must copy:** every file in §3 matrix (325)  
- **Must not copy:** `.git`, `.DS_Store`  
- **Must preserve:** exact relative names including typos  

### 6.2 `scripts/business/expand_video_agent_specs.py`

- **Input:** ROSTER + corpus agents.md  
- **Output:** 114 SPEC.md  
- **Fail closed:** unmapped va_id, missing row, parse error  
- **Idempotent:** same input → stable SPEC (deterministic field order)

### 6.3 `scripts/business/check_video_corpus_standalone.py`

- Exit 0 only if V2–V5 rules hold  
- Used in CI optional job `video-corpus-standalone`

### 6.4 `backend/app/tests/unit/test_video_corpus_standalone.py`

- Assert MANIFEST exists and len ≥ 325  
- Assert `corpus/study/agents.md` exists and contains `DirectorAgent`  
- Assert random sample of 5 pack_ids: SPEC.md has Responsibility  
- Assert inventory_check still passes  
- **Does not** reimplement migration; only validates artifacts on disk  

---

## 7. Agent table extraction notes (agents.md)

`study/agents.md` structure:

- 10 category sections with markdown tables  
- Columns include: #, Agent, Responsibility, Knowledge Distillation Source, Self-Quality Criteria, Surpass-Human Signal, Accepts Critique From, Comments On, Tool Access, Architecture Pattern  
- Section 11: common agent structure (copy as shared `corpus/study/` content; link from all SPECs)  
- Section 12: references  

Parser requirements:

- Handle bold names `**DirectorAgent**`  
- Map display names → pack_id via ROSTER (`DirectorAgent` → `video.director`)  
- Preserve multi-line cells if any  
- Unit test: extract exactly **114** numeric ids 1..114 with no gaps  

---

## 8. Risks & mitigations

| Risk | Mitigation |
|------|------------|
| PR too large for review UI | Single import commit + follow-up SPEC expand commit; reviewers use MANIFEST |
| Agents.md parse misses rows | Fail closed; snapshot expected 114 ids |
| Spec expand overwrites manual work | `agent_spec.spec_lock` or SPEC frontmatter `lock: true` |
| Duplicate knowledge bloat | Corpus once; SPEC links; no 114× full coding_agent copy |
| Stale after va changes | Document refresh command; SOURCE_COMMIT compare |
| Host “runs” still needs stubs | Runtime stubs already in generic; corpus enables **design-time** standalone, not magic media APIs |
| Legal | Provenance headers; keep upstream attribution |

---

## 9. Success criteria (migration_plan complete when executed)

1. **`business/video/corpus/`** contains **all 325** content files from va (per MANIFEST).  
2. **`SOURCE_COMMIT.txt`** pins va SHA.  
3. **All 114 SPEC.md** are self-contained (not refer-only).  
4. Primary docs under `business/video/` do not require `C:\Project\va-agent-swarm` to exist.  
5. Inventory still **`INVENTORY PASS count=114 n3=complete`**.  
6. Backend unit suite green + `test_video_corpus_standalone` green.  
7. Offline proof: rename/ignore va path → open agents.md + 10 SPECs + SYSTEM_REFERENCE + 1 SVG + 1 reference chapter from corpus only.

---

## 10. Explicit non-goals

| Non-goal | Why |
|----------|-----|
| Copy `.git` directory | Use commit pin |
| Second LangGraph host inside generic | N1/N2 host is generic runtime |
| Live Sora/Veo from docs alone | Docs ≠ provider keys; stubs remain until media phase |
| Auto-activate 114 agents to production | Separate activation waves |
| Rewriting typo filenames on first import | Fidelity first; aliases in INDEX later |

---

## 11. Effort estimate

| Phase | Effort |
|-------|--------|
| P0 freeze | 0.5 h |
| P1 bulk copy + script | 2–4 h |
| P2 SPEC expand + parser tests | 4–8 h |
| P3 indexes | 2–4 h |
| P4 seeds | 2–4 h (optional polish) |
| P5 provenance | 1–2 h |
| P6–P7 verify/docs | 2–3 h |
| **Total** | **~2–3 engineering days** for full ALL copy + SPEC expand |

---

## 12. Recommended execution command sequence (after GO)

```bash
# P0–P1
python scripts/business/migrate_va_corpus.py ^
  --va-root C:\Project\va-agent-swarm ^
  --dest business/video/corpus ^
  --include-all-content

# P2
python scripts/business/expand_video_agent_specs.py --write

# P6
python scripts/business/check_video_corpus_standalone.py
python scripts/business/inventory_check.py
cd backend && python -m pytest app/tests/unit/test_video_corpus_standalone.py app/tests/unit -q
```

---

## 13. Relation to other docs

| Doc | Role |
|-----|------|
| `migration.md` | Short problem brief |
| **`migration_plan.md` (this)** | **Deep plan ensuring ALL files can and will land** |
| `adoption.md` v2.4 | N3 strategy; corpus migration is post-N3 depth fill |
| `planning/improvement/wave-*` | Pack shell already present; does not replace corpus copy |

---

## 14. Decision required before execute

| Decision | Recommendation |
|----------|----------------|
| Copy **all languages/scripts** (FULL 325)? | **YES** (user: ALL information) |
| Destination | `business/video/corpus/` as specified |
| Expand SPECs in same PR as corpus? | Prefer **two commits**: (1) corpus (2) SPEC expand |

**Await GO to implement scripts and run P0–P7.**

---

## 16. Execution record (2026-07-13)

| Phase | Result |
|-------|--------|
| P0 freeze | va SHA `965d85e378c936f1aba1c39cad8158f97b1bdaf6` |
| P1 bulk copy | **325** files → `business/video/corpus/` (`migrate_va_corpus.py --force`) |
| P2 SPEC expand | **114** SPEC.md written (`expand_video_agent_specs.py --write`, join on va_id) |
| P3 indexes | `corpus/README.md`, `INDEX.md`, `AGENT_DOC_MAP.json` |
| P6 gates | `STANDALONE PASS`; inventory `114 n3=complete`; `test_video_corpus_standalone` **4 passed** |
| P7 docs | `business/video/README.md`, handoff, adoption changelog 2.4.1 |

Scripts added:

- `scripts/business/migrate_va_corpus.py`
- `scripts/business/expand_video_agent_specs.py`
- `scripts/business/check_video_corpus_standalone.py`
- `backend/app/tests/unit/test_video_corpus_standalone.py`

**Knowledge-standalone:** yes (va disk not required for SPECs + corpus).  
**Runtime media:** still stubs (by design).

---

## 15. Plan review (2026-07-13) — pre-execution

**Verdict:** **Approve with minor amendments.** Suitable to execute after applying §15.3. Numbers re-checked: **325 content files**, **~10.9 MB**, study **276**, ref **68**, ui **42**, workflows **19**, plan **10**, root content **40**.

### 15.1 Strengths

| Strength | Why it matters |
|----------|----------------|
| Correct problem diagnosis | 114/114 SPECs are refer-only; external hops fail under context limits |
| Feasible full copy | ~11 MB, no bad paths, no LFS — “ALL files” is realistic |
| Dual store (corpus + SPEC) | Fidelity **and** agent-local entrypoints |
| Exclude only `.git` / `.DS_Store` | Matches “ALL information” without junk |
| Typo preservation | Avoids broken links if docs cite misspelled names |
| Two-phase copy then expand | Safer than rewrite-while-copy |
| Explicit non-goals | No second LangGraph host; no fake media from docs |
| Verification matrix V1–V7 | Executable gates, not wishful prose |

### 15.2 Gaps / risks in the plan (fix before or during GO)

| # | Severity | Issue | Recommended fix |
|---|----------|--------|-----------------|
| R1 | **High** | **“Run without va” ≠ “runtime needs zero network”.** Plan says standalone for *docs/design*; host still uses stubs/APIs. | In README + success criteria: distinguish **knowledge-standalone** vs **media-runtime**. |
| R2 | **High** | **agents.md → pack_id mapping is brittle.** Display names (`ProducerAgent / EP`, `CinematographerAgent (DoP)`) may not fuzzy-match ROSTER cleanly. | Prefer **va_id (column #)** as primary key; name match secondary. Golden fixture: 114 ids extracted. |
| R3 | **Med** | **Internal links inside copied md still say `./foo` or old paths.** Copy alone does not rewrite relative links *within* corpus files that point outside. | P1.5: scan corpus for `](http` / absolute paths / `va-agent-swarm`; rewrite or document “links are intra-corpus relative only.” Most study links are relative `./` — **verify** after copy. |
| R4 | **Med** | **Bucket B1–B14 counts are not disjoint.** Sum of bucket estimates ≠ 325 if used as additive checklist without a global walk. | Gate on **global walk count == 325**, not sum of buckets. Buckets are coverage lenses only. |
| R5 | **Med** | **study count 276 vs “276 + .gitignore”.** If `.gitignore` included, planned count may be 326. | Freeze: content files excluding `.DS_Store`/`.git`; include `study/.gitignore` → re-count once and pin exact integer in MANIFEST.planned. |
| R6 | **Med** | **No rewrite of agent_spec tools from agents.md “Tool Access”.** SPECs get design tools; runtime allow-lists stay stubs — good, but plan should say **explicitly** not to auto-add Sora/Veo to allow-lists from docs. | Add safety rule: expand SPEC tools as *design-time*; runtime tools only via existing register. |
| R7 | **Low** | **GitHub PR size / clone.** 11 MB is fine; 325 files + expanded SPECs OK. | Two commits as planned. |
| R8 | **Low** | **CI optional job** may never run if not wired. | Wire `check_video_corpus_standalone.py` into existing inventory job or wave CI after import. |
| R9 | **Low** | **HK/zh scripts bloat context** for agents that load whole corpus. | Keep full copy; instruct coding agents to open **SPEC.md + INDEX**, not entire corpus. |
| R10 | **Info** | **migration.md vs migration_plan.md** dual docs. | Keep plan as SoT; migration.md already points here. |

### 15.3 Required amendments before GO (checklist)

- [ ] Pin **exact** planned file count after one dry-run walk (325 ± gitignore decision).
- [ ] SPEC expand joins on **`va_id` first**, not display name alone.
- [ ] Add **safety rule**: never promote design-time tool names into production allow-list automatically.
- [ ] Add **post-copy link audit** step (relative links resolve under corpus/).
- [ ] Clarify success: **knowledge-standalone** complete; runtime media still stubs.
- [ ] Add **refresh runbook**: `migrate_va_corpus.py --va-root …` when va moves forward.

### 15.4 What the plan does *not* need to change

- Destination under `business/video/corpus/` — correct for N1.
- Excluding `.git` — correct.
- Expanding SPECs — necessary for coding-agent usability.
- Not rebuilding va as second control plane — correct for N2.

### 15.5 Reviewer recommendation

| Option | When |
|--------|------|
| **GO P0–P1 only** (bulk copy) | Want corpus on disk immediately; SPECs later |
| **GO P0–P2** (copy + SPEC expand) | **Recommended** minimum for “refer-only is fixed” |
| **GO P0–P7** full | Best long-term standalone story |

**Overall score:** **8.5/10** as an execution plan — strong inventory and structure; fix mapping key + link audit + runtime safety before relying on P2 automation.

---

*End migration_plan.md v2.0 — completeness-first, standalone host corpus.*

