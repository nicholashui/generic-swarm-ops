# Wave 1 Design — Domain Pack SDK + ALC

**Requirements:** `planning/improvement/wave-1/requirements.md`  
**Prior:** Wave 0 schemas + video L0 catalog  

---

## 1. High-level architecture and data flow

```text
Domain Pack disk (business/<domain>/)
        │ manifest + agent_spec.json
        ▼
POST /domains/register ──validate schema──► RuntimeStore agents[] (status draft/registered, domain_id, ALC fields)
        │
        ▼
update_agent_status(active) ──ALC gate──► active | reject alc_required
        │
Workflow run step
        │ pre-step: LessonLibrary.retrieve(agent_id=…)
        │ inject → step_record.injected_lessons
        ▼
tool/LLM execution (existing adapters)
        │
reflect_on_workflow_run
        │ per-step agent_id → improvement_lessons[]
        ▼
GET /improvement/lessons?agent_id=  /  metrics?agent_id=
```

```text
propose_evolution_variant(variant_type=agent_genome)
        │ force sandbox_only=true
        ▼
evolution_variants[]  (never production DNA unless promote path)
```

---

## 2. Key schemas / models / interfaces

### 2.1 Lesson (extended)
- Fields: existing + `agent_id: str | None`
- Dedup key: `(text, workflow_id, agent_id, organization_id)`
- `retrieve(workflow_id=, agent_id=, k=)`

### 2.2 ALC readiness check
```text
is_alc_ready(agent) :=
  requires_alc is not True  OR (
    alc_version present AND
    "agent" in allowed_memory_scopes AND
    hooks.reflect is True
  )
```
Used by `update_agent_status(..., "active")` and optional production_ready DNA check.

### 2.3 Domain register payload
- Body: path-based `{ "domain_id": "video", "manifest_path": "business/video/manifest.json" }`  
  or inline `{ "manifest": { ... } }`
- Response: `{ status: "draft", domain_id, agents_loaded, agents: [...] }`

### 2.4 Domain catalog (store)
- Collection `domain_packs`: `{ domain_id, version, organization_id, requires_alc, registered_at, agent_ids[] }`

### 2.5 Agent genome variant
- `variant_type: "agent_genome" | "workflow_dna" (default)`
- `agent_id` required for agent_genome
- `sandbox_only` always True on propose

---

## 3. Component breakdown

| Component | Location | Role |
|-----------|----------|------|
| LessonLibrary | self_improvement/lessons.py | agent-scoped store/retrieve |
| alc_validator | infrastructure/governance/alc_validator.py | pure ALC checks |
| RuntimeServices | runtime.py | reflect, inject, gate, register, metrics |
| domains router | api/v1/routes/domains.py | HTTP register/list |
| improvement routes | improvement.py | agent reflect, lessons filter, metrics |
| evolution | runtime propose | agent_genome |
| FE DomainPackPanel | components/domain/domain-pack-panel.tsx | roster + ALC |
| Isolation tests | tests/unit/test_alc_and_domains.py | AC proof |

---

## 4. N1 / N2 / N3 enforcement

| N | Design |
|---|--------|
| N1 | ALC gate + agent-scoped lessons; video agents load only from `business/video` specs |
| N2 | register API domain-agnostic; example_research isolation tests |
| N3 | Inventory unchanged; register may load subset listed in manifest but does not delete disk dirs |

---

## 5. Reuse patterns

- Wave 0 `schema_validate` + domain-manifest schema
- Existing `reflect_on_run`, LessonLibrary, evolution propose
- FE Section + DataTable + StatusBadge patterns on agents page
- `_write_memory` already supports `agent=` for scope checks

---

## 6. New / modified files

```text
planning/improvement/wave-1/{requirements,design,tasks,completion-report}.md
backend/app/infrastructure/self_improvement/lessons.py          # MOD
backend/app/infrastructure/governance/alc_validator.py          # NEW
backend/app/runtime.py                                          # MOD
backend/app/api/v1/routes/domains.py                            # NEW
backend/app/api/v1/routes/improvement.py                        # MOD
backend/app/api/v1/router.py                                    # MOD
scripts/business/register_domain.py                             # MOD (optional API-aligned)
business/example_research/workflows/wf_example_research_v1.dna.json  # NEW
business/example_research/evals/golden/example-research-brief.json   # NEW
backend/app/tests/unit/test_alc_and_domains.py                  # NEW
frontend/src/components/domain/domain-pack-panel.tsx            # NEW
frontend/src/lib/routes/paths.ts                                # MOD
frontend/src/app/app/[...slug]/page.tsx                        # MOD (agents section)
docs/domain-packs.md                                            # MOD
```

---

## 7. Sandbox / evolution

- agent_genome always sandbox_only.
- Promote genome reuses existing promote path only after evaluation (Wave 1: propose + block direct mutation is enough).
- Skill sandbox unchanged.

---

## 8. Structure / Backend / Frontend impact

### Structure
- example_research DNA + golden; docs update; video pack untouched as catalog.

### Backend
- Core ALC + domains implementation.

### Frontend
- Additive domain pack panel on `/app/agents` (and optional `/app/domains` path alias).

---

## 9. Critic notes

- Seed ops agents may set `requires_alc: false` or receive ALC fields so E1 still activates them.
- Pre-step inject uses org lessons filtered by agent_id; empty list is OK.
- Register loading all 114: load agent_spec from disk for each pack_id in manifest.agents (may be list of 114 strings).

*End of Phase 2 design.*
