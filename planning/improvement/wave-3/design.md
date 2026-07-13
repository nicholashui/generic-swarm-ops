# Wave 3 Design — Coevolution, Lesson Utility & Quality Evals

**Wave:** 3  
**Implements:** `planning/improvement/wave-3/requirements.md`  
**Date:** 2026-07-12  

---

## 1. High-level architecture and data flow

```text
┌─────────────────────────────────────────────────────────────────┐
│ Structure                                                        │
│  business/video/evals/golden/*  (+ LQR/consistency)              │
│  business/video/workflows/*.dna.json (Wave 2 baseline)           │
│  business/distilled/skills/_sandbox/* (skill proposals)          │
└────────────────────────────┬────────────────────────────────────┘
                             │ load_eval_corpus + pack overlay
┌────────────────────────────▼────────────────────────────────────┐
│ Backend                                                          │
│  run_coevolution_experiment(generations=N, domain_id?, ...)      │
│    ├─ propose agent_genome (planner)     ─┐                      │
│    ├─ propose agent_genome (aesthetics)  ─┼─► sandbox_evaluate   │
│    ├─ optional workflow_dna sibling      ─┘     + ALC fitness    │
│    ├─ composite fitness → elite seed next gen                    │
│    └─ audit + coevolution_runs[] store                           │
│                                                                  │
│  lesson_utility_dashboard  → ranked lessons + aggregate metrics   │
│  governance_review_learned_artifacts → pending variants/skills   │
│  propose_skill_sandbox(domain=video, skill_name=video-*)         │
└────────────────────────────┬────────────────────────────────────┘
                             │ REST
┌────────────────────────────▼────────────────────────────────────┐
│ Frontend                                                         │
│  LessonUtilityPanel (+ EvolutionArchivePanel existing)           │
└─────────────────────────────────────────────────────────────────┘
```

**Invariant:** Coevolution and skill proposals never write production workflow DNA or production skill paths without explicit promote/canary APIs already present.

---

## 2. Key schemas, models, interfaces

### 2.1 Coevolution run record (store: `coevolution_runs`)

```json
{
  "id": "coevo_<hex>",
  "organization_id": "...",
  "domain_id": "video",
  "generations_requested": 2,
  "generations": [
    {
      "generation": 1,
      "variant_ids": ["var_...", "var_..."],
      "elite_variant_id": "var_...",
      "elite_fitness": 0.72,
      "fitness_metrics": { "suite_pass_rate": 1.0, "knowledge_growth_norm": 0.1, "lesson_reuse_norm": 0.0, "composite_fitness": 0.72 }
    }
  ],
  "agent_ids": ["video.planner", "video.aiqaconsistency"],
  "base_workflow_id": "wf_video_arch_a_viral_hook_v1",
  "sandbox_only": true,
  "auto_promote": false,
  "created_at": "ISO-8601",
  "created_by": "user_id"
}
```

### 2.2 Composite fitness

```text
composite = 0.6 * suite_pass_rate
          + 0.2 * knowledge_growth_norm
          + 0.2 * lesson_reuse_norm
```

Normalization (deterministic):

- `knowledge_growth_norm = min(1.0, knowledge_growth_count / 10.0)`
- `lesson_reuse_norm = min(1.0, lesson_reuse_rate / 5.0)` (reuse_rate is uses/lessons)

ALC metrics sourced from `improvement_metrics(agent_id=...)` for genomes under evaluation; if no agent_id, ALC terms default to 0.

### 2.3 Lesson utility dashboard payload

```json
{
  "lessons": [ { "id", "text", "agent_id", "utility", "uses", "wins", ... } ],
  "aggregates": {
    "total_lessons": 0,
    "knowledge_growth_count": 0,
    "lesson_reuse_rate": 0.0,
    "by_agent": { "video.planner": { "count": 1, "avg_utility": 0.5 } }
  },
  "limit": 20,
  "agent_id": null
}
```

Reuse existing `LessonLibrary` utility ranking from `list_improvement_lessons`.

### 2.4 Governance review payload

```json
{
  "pending_variants": [ { "id", "name", "status", "sandbox_only", "fitness_metrics", "variant_type" } ],
  "pending_skills": [ { "id", "skill_name", "status", "sandbox_only", "sandbox_path" } ],
  "policy": "human_signoff_required",
  "auto_promote": false
}
```

Pending = variant status in `{sandbox_proposed, sandbox_evaluated, approved_for_canary}` and skill status `sandbox_proposed` (not `promoted`).

### 2.5 API surface

| Method | Path | Runtime method |
|--------|------|----------------|
| POST | `/api/v1/evolution/coevolution/run` | `run_coevolution_experiment` |
| GET | `/api/v1/evolution/governance/review` | `governance_review_learned_artifacts` |
| GET | `/api/v1/improvement/lesson-utility` | `lesson_utility_dashboard` |

Existing: skill propose/promote, variant evaluate/promote, improvement metrics/lessons.

---

## 3. Component breakdown and cross-part interactions

| Component | Part | Role |
|-----------|------|------|
| LQR golden + rubrics | Structure | Pack eval corpus for consistency quality |
| `corpus_eval.load_eval_corpus` / evaluate | Backend | Optionally merge `business/video/evals/**` when DNA domain=video |
| `coevolution.py` | Backend | Generation loop pure helpers (propose payloads, elite select, fitness merge) |
| `RuntimeServices` | Backend | Orchestrate store, propose, evaluate, ALC metrics, audit |
| Evolution / improvement routes | Backend | Thin HTTP adapters |
| `LessonUtilityPanel` | Frontend | Display utility dashboard |
| `EvolutionArchivePanel` | Frontend | Existing; coevolution results appear as variants in archive |

**Cross-part:** Structure fixtures → Backend corpus → fitness → FE archive/utility panels. No FE write paths for promote in Wave 3.

---

## 4. N1 / N2 / N3 enforcement

| N | Design mechanism |
|---|------------------|
| **N1** | Video goldens and rubrics only under `business/video/`; genomes bind `agent_id`; learning via ALC metrics + lessons, not core hard-coded video business rules. |
| **N2** | `run_coevolution_experiment(domain_id=..., agent_ids=..., base_workflow_id=...)` is pack-agnostic; video is default proving configuration only. |
| **N3** | No roster mutation; inventory CI unchanged; process docs optional update only. |

Sandbox: every proposed variant sets `sandbox_only: true`, `auto_promote: false`; evaluate path already forbids direct production mutation.

---

## 5. Reuse of existing patterns

| Existing | Reuse |
|----------|--------|
| `propose_evolution_variant` + `agent_genome` | Wave 1 genome path |
| `sandbox_evaluate_variant` + `evaluate_variant_against_corpus` | Wave/P3 evolution |
| `improvement_metrics` / `list_improvement_lessons` / `LessonLibrary` | Wave 1 ALC |
| `propose_skill_sandbox` / `write_skill_sandbox` | Existing skill sandbox |
| `evolution_archive` | DGM-lite archive UI |
| Video DNA + golden from Wave 2 | Baseline for coevolution targets |
| FE `EvolutionArchivePanel` / API client | Mount utility panel similarly |

---

## 6. New files / folders

```text
planning/improvement/wave-3/
  requirements.md
  design.md
  tasks.md
  completion-report.md

business/video/evals/golden/video-lqr-consistency.json
business/video/evals/rubrics/lqr-consistency.md

backend/app/infrastructure/evolution/coevolution.py
backend/app/infrastructure/evolution/corpus_eval.py   # extend
backend/app/runtime.py                                # methods
backend/app/api/v1/routes/evolution.py                # coevolution + review
backend/app/api/v1/routes/improvement.py              # lesson-utility
backend/app/tests/unit/test_wave3_coevolution.py

frontend/src/components/domain/lesson-utility-panel.tsx
frontend/src/lib/api/client.ts                        # if helpers needed
frontend/src/app/app/[...slug]/page.tsx              # mount panel

docs/domain-packs.md                                  # short coevolution note
```

---

## 7. Coevolution algorithm (lite, deterministic)

```text
function run_coevolution_experiment(G, domain_id, planner_id, aesthetics_id, base_wf):
  elite_genomes = default seeds (generation counter 0)
  for g in 1..G:
    payloads = [
      agent_genome(planner_id, mutate(elite_genomes.planner, g)),
      agent_genome(aesthetics_id, mutate(elite_genomes.aesthetics, g)),
    ]
    optionally: workflow_dna sibling clone of base_wf with sandbox markers
    for each payload:
      v = propose_evolution_variant(...)
      v = sandbox_evaluate_variant(v.id)
      enrich fitness with ALC metrics for v.agent_id
      set composite_fitness on variant.fitness_metrics
    elite = max(variants, key=composite_fitness)
    seed next genomes from elite
    record generation summary
  persist coevolution_runs
  audit evolution.coevolution_completed
  return run record
```

**Mutation (sandbox only):** increment `genome.generation`, bump a numeric `genome.temperature` or `genome.version` field; attach `lineage` from prior elite variant id. No LLM required.

**Measurable improvement guarantee for tests:** Seed one or more high-utility lessons for planner before gen 2, or inject ALC growth between gens so composite can non-decrease; tests assert `generations>=2`, audit present, and either elite composite non-decreasing **or** all generations recorded with valid fitness (acceptance FR-W3-11).

---

## 8. Sandbox / evolution considerations

- `auto_promote` hard-coded false on coevolution runs and evaluations.
- Production DNA version check: snapshot base workflow before experiment; assert version unchanged after.
- Skill proposals: `domain` field optional on proposal dict; production_path still under distilled skills; write only `_sandbox`.
- Governance review is **read-only** list; promote uses existing explicit endpoints.

---

## 9. Detailed design impact by part

### 9.1 Structure

- **LQR golden:** targets `wf_video_arch_a_viral_hook_v1` (or spine), expected human gate + consistency rubric fields (`expected` structural checks compatible with `_eval_golden`).
- Rubric markdown documents LQR consistency dimensions (aesthetics, consistency, psychological alignment) for humans/eval harness provenance.
- No DNA production_ready flip to true as part of Wave 3.

### 9.2 Backend

#### `coevolution.py`

Pure helpers:

- `default_agent_pair(domain_id) -> (planner_id, aesthetics_id)`
- `build_genome_payload(agent_id, generation, parent_genome) -> dict`
- `composite_fitness(suite_metrics, alc_metrics) -> float`
- `select_elite(variants) -> variant`
- `summarize_generation(generation, variants) -> dict`

#### Runtime methods

```python
def run_coevolution_experiment(self, user, *, generations=2, domain_id="video",
    agent_ids=None, base_workflow_id="wf_video_arch_a_viral_hook_v1") -> dict: ...

def lesson_utility_dashboard(self, user, *, agent_id=None, limit=20) -> dict: ...

def governance_review_learned_artifacts(self, user) -> dict: ...
```

#### Fitness enrichment

In `sandbox_evaluate_variant` (or post-eval hook inside coevolution):

```python
alc = self.improvement_metrics(user, agent_id=variant.get("agent_id"))
fitness["knowledge_growth"] = alc["knowledge_growth_count"]
fitness["lesson_reuse"] = alc["lesson_reuse_rate"]
fitness["knowledge_growth_norm"] = min(1.0, growth / 10)
fitness["lesson_reuse_norm"] = min(1.0, reuse / 5)
fitness["composite_fitness"] = 0.6*suite + 0.2*kg_norm + 0.2*reuse_norm
```

Apply when `agent_id` present; for pure workflow DNA variants, ALC terms 0 unless `domain_id` aggregate metrics requested.

#### Corpus eval pack path

```python
def load_eval_corpus(repo_root, *, domain_id=None) -> ...
# if domain_id == "video" or dna.domain == "video":
#   also load business/video/evals/golden, regression, adversarial
```

`evaluate_variant_against_corpus` accepts domain from DNA metadata:

```python
domain = (dna.get("domain") or dna.get("domain_id") or "").lower()
```

Merge pack goldens into golden list (dedupe by id).

### 9.3 Frontend

- `LessonUtilityPanel`: fetch `GET /improvement/lesson-utility`, show aggregates + top N lessons (agent_id, utility, uses).
- Demo mode: static DEMO_UTILITY fixture.
- Mount below or beside `EvolutionArchivePanel` on the evolution slug page.
- Optional: show composite fitness fields already on archive if present (no archive redesign required).

---

## 10. Test design

| Test | Asserts |
|------|---------|
| `test_coevolution_multi_generation_sandbox_only` | gens≥2, variants created, sandbox_only, host DNA version stable |
| `test_fitness_includes_alc_when_lessons` | after seeding lesson for agent, fitness has knowledge_growth / composite |
| `test_lesson_utility_dashboard_ranked` | order by utility desc |
| `test_video_skill_sandbox_propose` | path contains `_sandbox`, sandbox_only |
| `test_governance_review_lists_pending` | includes proposed variant/skill |
| `test_corpus_loads_video_pack_goldens` | LQR golden present when domain=video |
| `test_composite_fitness_helper` | pure composite/enrich helpers |
| Inventory + full unit | regression gate |

---

## 11. Internal critic (Phase 2)

| Risk | Design response |
|------|-----------------|
| Over-engineered GA | Lite genome mutation + fixed composite weights |
| Breaking corpus for non-video DNA | Pack overlay only when domain=video |
| FE blocked on auth | Demo mode + graceful error |
| Double fitness formulas | Single `composite_fitness` helper in coevolution.py used by runtime |

*End Phase 2 — Design.*
