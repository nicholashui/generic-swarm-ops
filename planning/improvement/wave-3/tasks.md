# Wave 3 Tasks — Implementation Checklist

**Wave:** 3  
**Implements:** `requirements.md` + `design.md`  
**Date:** 2026-07-12  

Execute in order. Tag legend: **[Structure]** / **[Backend]** / **[Frontend]**.

---

## Structure

### T1 — LQR / consistency golden + rubric
**Paths:**
- Create `business/video/evals/golden/video-lqr-consistency.json`
- Create `business/video/evals/rubrics/lqr-consistency.md`

**Pattern:** Mirror Wave 2 `video-spine-viral-hook.json` (id, workflow_id, domain, expected structural fields, rubrics, provenance).

**Acceptance:**
- [x] JSON valid; `domain: video`; rubrics include consistency/LQR dimensions
- [x] Rubric markdown documents human-readable criteria
- [x] Provenance refs improvements.md Wave 3 + va LQR sense

### T10 — Docs + SDD completion report
**Paths:**
- Update `docs/domain-packs.md` (short coevolution / utility / governance note)
- Write `planning/improvement/wave-3/completion-report.md`

**Acceptance:**
- [x] Docs mention sandbox-only coevolution + lesson utility + governance review
- [x] Completion report lists evidence (pytest, inventory)

---

## Backend

### T2 — Corpus eval loads video pack goldens
**Paths:**
- Modify `backend/app/infrastructure/evolution/corpus_eval.py`

**Work:**
- Extend `load_eval_corpus(repo_root, *, domain_id=None)`
- When `domain_id == "video"`, also read:
  - `business/video/evals/golden`
  - `business/video/evals/regression` (if present)
  - `business/video/evals/adversarial` (if present)
- `evaluate_variant_against_corpus`: derive domain from DNA; pass through
- Dedupe by fixture `id`

**Acceptance:**
- [x] Video DNA eval sees LQR golden after T1
- [x] Non-video DNA still loads platform `business/evals/*` only (or unchanged default)

### T3 — Coevolution module + runtime experiment
**Paths:**
- Create `backend/app/infrastructure/evolution/coevolution.py`
- Modify `backend/app/runtime.py` → `run_coevolution_experiment`
- Modify `backend/app/api/v1/routes/evolution.py` → `POST /coevolution/run`

**Reuse:** `propose_evolution_variant`, `sandbox_evaluate_variant`, audit append, store collections.

**Acceptance:**
- [x] ≥2 generations default
- [x] Planner + aesthetics agent_genome variants (or configurable agent_ids)
- [x] `coevolution_runs` persisted; audit event
- [x] `auto_promote: false`, `sandbox_only: true`
- [x] Production workflow version unchanged after run

### T4 — Fitness ALC enrichment
**Paths:**
- `coevolution.py` composite helper
- `runtime.sandbox_evaluate_variant` and/or coevolution post-eval enrichment

**Acceptance:**
- [x] When `agent_id` present, fitness includes knowledge_growth / lesson_reuse (raw + norms) + composite_fitness
- [x] Suite pass rate preserved

### T5 — Lesson utility dashboard
**Paths:**
- `runtime.lesson_utility_dashboard`
- `routes/improvement.py` → `GET /lesson-utility`

**Reuse:** `list_improvement_lessons`, `improvement_metrics`.

**Acceptance:**
- [x] Ranked lessons by utility
- [x] Aggregates include growth/reuse and optional by_agent

### T6 — Governance review of learned artifacts
**Paths:**
- `runtime.governance_review_learned_artifacts`
- `routes/evolution.py` → `GET /governance/review`

**Acceptance:**
- [x] Lists pending variants + skill proposals
- [x] Does not promote or mutate status
- [x] Documents `auto_promote: false`

### T7 — Video skill sandbox coverage
**Paths:**
- Optionally pass `domain` through `propose_skill_sandbox` payload
- Tests under T9

**Acceptance:**
- [x] Propose video-named skill → `_sandbox` path, sandbox_only
- [x] Promote still separate explicit API (no auto)

### T9 — Unit tests
**Path:** `backend/app/tests/unit/test_wave3_coevolution.py`

**Cases:**
1. Multi-generation coevolution + production DNA stable
2. Fitness ALC enrichment with seeded lesson
3. Lesson utility dashboard ranking
4. Governance review pending list
5. Video skill sandbox propose
6. Corpus loads video pack golden for domain=video

**Acceptance:**
- [x] All new tests pass
- [x] Full unit suite green
- [x] `python scripts/business/inventory_check.py` → PASS 114

---

## Frontend

### T8 — LessonUtilityPanel
**Paths:**
- Create `frontend/src/components/domain/lesson-utility-panel.tsx`
- Wire API client if needed (`frontend/src/lib/api/client.ts`)
- Mount in `frontend/src/app/app/[...slug]/page.tsx` near evolution archive

**Pattern:** Follow `evolution-archive-panel.tsx` (demo mode, error, refresh).

**Acceptance:**
- [x] Renders aggregates + top lessons
- [x] Demo fallback works
- [x] No typecheck/lint regression on touched files

---

## Task order (recommended)

1. T1 Structure fixtures  
2. T2 Corpus pack load  
3. T4 Fitness helpers (with T3)  
4. T3 Coevolution runner + route  
5. T5 Lesson utility  
6. T6 Governance review  
7. T7 Skill domain metadata (light)  
8. T9 Tests  
9. T8 FE panel  
10. T10 Docs + completion report  

---

## Acceptance criteria matrix (wave-level)

| AC | Tasks |
|----|-------|
| AC-1 Coevolution ≥2 gens + audit | T3, T9 |
| AC-2 Fitness suite + ALC | T4, T9 |
| AC-3 Utility ranked | T5, T9 |
| AC-4 Skill sandbox | T7, T9 |
| AC-5 Governance list | T6, T9 |
| AC-6 LQR golden + corpus | T1, T2, T9 |
| AC-7 No prod DNA mutation | T3, T9 |
| AC-8 Inventory + unit suite | T9 |
| AC-9 FE panel | T8 |
| AC-10 Completion report | T10 |

---

## Out of scope (do not implement in Wave 3)

- Load tests / multi-pack concurrency (Wave 4)
- Red-team security suite expansion (Wave 4)
- Full roster activation cats 2–10 (Wave 5)
- Real media provider adapters
- Auto-promote of any kind

*End Phase 3 — Tasks.*
