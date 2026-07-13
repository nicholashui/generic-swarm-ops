# Wave 0 Design — Foundations

**Wave:** 0  
**Requirements:** `planning/improvement/wave-0/requirements.md`  
**Sources:** `improvements.md` Wave 0, `adoption.md` v2.3 Appendix A, `business/schemas/workflow-dna.schema.json` pattern  

---

## 1. High-level architecture and data flow

```text
va-agent-swarm (upstream SoT)
    │  agents.md + SYSTEM_REFERENCE + Appendix A pack_ids
    ▼
[Export / materialize]  ──►  business/video/ROSTER.json
                            business/video/MAP.md
                            business/video/PROCESSES.md
                            business/video/agents/<pack_id>/{agent_spec,SPEC}
                            business/video/manifest.json (draft)
    │
    ▼
business/schemas/{domain-manifest,agent-spec,learning-log}.schema.json
    │
    ├── inventory_check (pytest / script) ── fail closed if count≠114
    └── domain register stub (CLI) ── validate manifest → draft OK
```

**Host core (runtime.py, FE shell):** unchanged for execution semantics. Wave 0 adds **artifacts + validation surfaces only**.

---

## 2. Key schemas, models, interfaces

### 2.1 `domain-manifest.schema.json`

Required: `domain_id`, `version`, `display_name`, `requires_alc`, `agents` (array of pack_ids or objects), `workflows` (array).  
Optional: `default_risk_tier`, `knowledge_seed_globs`, `api_hooks` (`tool_namespace`, `on_register` string identifiers).

### 2.2 `agent-spec.schema.json`

Required: `id`, `domain_id`, `name`, `status`, `requires_alc`, `allowed_memory_scopes`, `alc_version`.  
When `requires_alc` is true: scopes **must** include `"agent"`; `hooks.reflect` should be true for future ALC gate.  
Optional: `tools`, `role`, `risk_tier`, `critique_rubric_ref`, `provenance`, `va_id`.

### 2.3 `learning-log.schema.json`

Required: `agent_id`, lesson text (`lesson_text` or `text`), `provenance`.  
Optional: `run_id`, `step_id`, `utility_score`, `reuse_count`, `source_refs`, `captured_by`, `recorded_at`.  
**Note:** Runtime wiring of lessons is Wave 1; schema only in Wave 0.

### 2.4 ROSTER.json entry

```json
{
  "id": 53,
  "name": "OrchestratorAgent",
  "category": "9-Meta",
  "pack_id": "video.orchestrator",
  "va_source": "va-agent-swarm/study/agents.md"
}
```

### 2.5 Register stub interface

CLI: `python scripts/business/register_domain.py --domain video --manifest business/video/manifest.json --dry-run`  
Behavior: load JSON → validate against domain-manifest schema → print `{ "status": "draft", "domain_id": "..." }` or exit 1.  
Does **not** mutate runtime Postgres catalog in Wave 0 (optional write to `business/<domain>/.register-receipt.json` for evidence).

---

## 3. Component breakdown and cross-part interactions

| Component | Owner part | Interaction |
|-----------|------------|-------------|
| ROSTER / MAP / PROCESSES / agents/* | Structure | Source for inventory + future register |
| Schemas + fixtures | Structure | Used by inventory + register stub + future BE |
| `scripts/business/inventory_check.py` | Structure/Backend bridge | Pure filesystem checks |
| `test_domain_pack_inventory.py` | Backend | Invokes inventory check; unit green |
| `register_domain.py` | Structure/Backend | Schema validate only |
| Docs | Structure | Human onboarding |
| FE | Frontend | No code change Wave 0 |

---

## 4. Enforcement of N1 / N2 / N3

| N | Design enforcement |
|---|-------------------|
| **N1 isolation** | All video files under `business/video/`; agent_spec `domain_id: "video"`; ops seed agents unchanged outside pack |
| **N2 universality** | Schemas are domain-agnostic; example_research pack uses same shape; register stub takes any `domain_id` |
| **N3 retention** | 114 dirs generated from Appendix A; inventory fails if any missing; README forbids deletion |

---

## 5. Reuse of existing patterns

- JSON Schema style from `business/schemas/workflow-dna.schema.json` (required arrays, enums for risk tiers).
- Schema validation helpers: `scripts/business/lib/schema-lite.mjs` and/or Python `jsonschema` if available; prefer stdlib + lightweight check for pytest.
- Business scripts under `scripts/business/` (validate-business.mjs pattern).
- Test layout: `backend/app/tests/unit/test_*.py`.
- Provenance object shape from existing business examples.

---

## 6. New files / folders structure

```text
business/
  schemas/
    domain-manifest.schema.json          # NEW
    agent-spec.schema.json               # NEW
    learning-log.schema.json             # NEW
  fixtures/
    positive/
      domain-manifest.video.example.json # NEW
      agent-spec.video.example.json      # NEW
      learning-log.example.json          # NEW
    negative/
      domain-manifest.invalid.json       # NEW
      agent-spec.missing-alc.json        # NEW
  video/                                 # NEW tree
    README.md
    ROSTER.json
    MAP.md
    PROCESSES.md
    manifest.json
    agents/video.*/{agent_spec.json,SPEC.md,prompts/.gitkeep,rubrics/.gitkeep}
    workflows/.gitkeep
    tools/adapters.md
    evals/{golden,regression,adversarial}/.gitkeep
    knowledge/seeds/.gitkeep
    policies/.gitkeep
    ui/.gitkeep
  example_research/                      # NEW (P1)
    README.md
    manifest.json
    agents/example.researcher/agent_spec.json
    agents/example.reviewer/agent_spec.json
    workflows/.gitkeep
docs/domain-packs.md                     # NEW
scripts/business/
  inventory_check.py                     # NEW
  register_domain.py                     # NEW
  generate_video_pack_catalog.py         # NEW (generator)
backend/app/tests/unit/
  test_domain_pack_inventory.py          # NEW
  test_domain_pack_schemas.py            # NEW
planning/improvement/wave-0/
  requirements.md, design.md, tasks.md, completion-report.md
```

---

## 7. Sandbox / evolution considerations

- Wave 0 creates **draft** pack assets only; no evolution variants, no production DNA activation.
- Coding agent sandbox: all pack content is data under `business/` — safe to commit.
- Evolution APIs: **untouched**.
- Future promote of agents to `active` is Wave 1+ with ALC gate.

---

## 8. Structure / Backend / Frontend design impact

### 8.1 Structure

Primary owner of catalog, schemas, docs, generator script. Structure quality gate = inventory count 114 + schema fixtures.

### 8.2 Backend

- Add unit tests only (inventory + schema validation).
- Register stub as script (avoids router/runtime churn). If a route is added later in Wave 1, it reuses the same validate function.
- **Do not** modify `runtime.py` workflow engine for Wave 0.

### 8.3 Frontend

- No component or route changes.
- Document future surface in `docs/domain-packs.md` only.

---

## 9. Critic / rethink (Phase 2)

- Prefer generator script over hand-maintaining 114 folders (reproducible N3).
- Inventory test must load ROSTER.json as truth source, not hard-code 114 alone without pack_id set equality.
- Avoid full FastAPI domains router in Wave 0 to protect E1 surface area.

*End of Phase 2 design.*
