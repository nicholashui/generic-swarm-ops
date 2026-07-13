# Domain Packs

**Host:** generic-swarm-ops  
**Strategy:** `adoption.md` v2.3 · `improvements.md` · `repo_compare.md`  

## Purpose

A **Domain Pack** is a self-contained MMA system under `business/<domain_id>/` that plugs into the host runtime **without forking** FastAPI/runtime/governance/evolution.

## Non-negotiables

| ID | Rule |
|----|------|
| **N1** | Domain business logic stays in the pack path; agents gain ALC for autonomous learning. |
| **N2** | Any domain onboard via manifest + artifacts; host remains universal. |
| **N3** | Video pack retains **all 114** va agents + process index; inventory CI enforces. |

## Layout

```text
business/<domain_id>/
  manifest.json
  agents/<pack_id>/{agent_spec.json,SPEC.md,...}
  workflows/
  tools/
  evals/
  knowledge/seeds/
  policies/
  ui/
```

## Schemas

- `business/schemas/domain-manifest.schema.json`
- `business/schemas/agent-spec.schema.json`
- `business/schemas/learning-log.schema.json`

## Registration

### CLI (validate + optional receipt)

```bash
python scripts/business/register_domain.py --manifest business/video/manifest.json --dry-run
```

### API (Wave 1)

```http
POST /api/v1/domains/register
{ "manifest_path": "business/example_research/manifest.json" }
```

or inline `{ "manifest": { ...domain-manifest... } }`.

Loads agents into the org catalog as **draft/registered** with ALC fields from `agent_spec.json`. Does **not** auto-activate.

### ALC activation gate (Wave 1)

`PATCH /api/v1/agents/{id}` to `active` is denied unless:

- `requires_alc` is false, **or**
- `alc_version` set, `allowed_memory_scopes` includes `agent`, `hooks.reflect` is true

Lessons carry `agent_id`; list with `GET /api/v1/improvement/lessons?agent_id=…` and metrics via `GET /api/v1/improvement/metrics?agent_id=…`.

### Wave 3 — Coevolution, lesson utility, governance

Sandbox multi-generation learning on pack goldens (no production DNA mutation, never auto-promote):

| Surface | Path |
|---------|------|
| Coevolution experiment | `POST /api/v1/evolution/coevolution/run` body: `{ generations, domain_id, agent_ids?, base_workflow_id? }` |
| Lesson utility dashboard | `GET /api/v1/improvement/lesson-utility?agent_id=&limit=` |
| Governance review (list only) | `GET /api/v1/evolution/governance/review` |
| Skill sandbox (video ok) | `POST /api/v1/improvement/skills/propose` with optional `domain` |
| Pack eval overlay | corpus loads `business/<domain>/evals/*` when DNA `domain` matches (video LQR golden) |

FE: Evolution page shows **Lesson utility** panel beside the population archive.

Fitness composite (deterministic): `0.6 * suite_pass_rate + 0.2 * knowledge_growth_norm + 0.2 * lesson_reuse_norm`.

## Inventory (video N3)

```bash
python scripts/business/inventory_check.py
```

Fails if agent directories ≠ 114, ROSTER/MAP/agent_spec incomplete, standby/router/process_coverage incomplete, required DNA missing, or agents not `registered|active`. CI: `.github/workflows/n3-inventory.yml`.

N3 status API: `GET /api/v1/domains/video/n3-status` (roster 114, DNA count, orphans, `n3_complete`).

## Isolation rules

- Tool namespaces: e.g. `video.*` vs ops tools.
- Memory scopes: agent / organization; no cross-pack bleed (Wave 1 tests).
- Ops `business_orchestrator` ≠ `video.orchestrator`.

## Reuse playbook (other projects)

1. Copy `business/example_research/` or `business/example_education/` skeleton → `business/<your_domain>/`.
2. Fill manifest + agents (ALC fields) + one workflow DNA.
3. Validate schemas; register draft.
4. Wave 1+: ALC activation, evals, FE domain view.

Full operator steps: **[Add a Domain Pack runbook](./add-domain-pack-runbook.md)** · **[Versioning matrix](./domain-pack-versioning-matrix.md)**

### Wave 4 — Multi-pack proof

| Pack | Role |
|------|------|
| `video` | N3 full roster (inventory 114) |
| `example_research` | Wave 1 second pack |
| `example_education` | Wave 4 third lite pack |

Isolation: agent-scoped lessons/episodes; corpus overlays by `domain_id`; tool allow-list enforced outside the model (red-team: no allow-list expansion from injection).

Security evidence stub: `business/security/red-team-results/wave-4-tool-misuse.json`.

## Related

- Video pack: `business/video/README.md`
- Runbook: `docs/add-domain-pack-runbook.md`
- Versioning: `docs/domain-pack-versioning-matrix.md`
- Planning: `planning/improvement/wave-0/` … `wave-4/`
