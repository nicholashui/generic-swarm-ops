# Add a Domain Pack — Runbook

**Host:** generic-swarm-ops  
**Wave:** 4 (N2 multi-pack proof)  
**Related:** `docs/domain-packs.md`, `docs/domain-pack-versioning-matrix.md`

## Goal

Onboard a new multi-agent domain under `business/<domain_id>/` **without forking** the FastAPI runtime, evolution, or FE ops console.

## Preconditions

- [ ] Read N1/N2/N3 in `adoption.md`
- [ ] Schemas available under `business/schemas/`
- [ ] Video inventory (if touching video) still owned by N3 — **do not** drop agents to “make room”

## Steps

### 1. Scaffold

```text
business/<domain_id>/
  manifest.json
  README.md
  agents/<agent_id>/agent_spec.json
  workflows/wf_<domain>_….dna.json
  evals/golden/
  tools/          # optional adapters notes
  knowledge/seeds/
```

Copy from `business/example_research/` or `business/example_education/` (lite).

### 2. Fill manifest

Required: `domain_id`, `version`, `display_name`, `requires_alc`, `agents`, `workflows`.  
Optional: `default_risk_tier`, `api_hooks.tool_namespace`.

### 3. Agent Learning Contract (ALC)

Each agent intended for `active` must have:

- `requires_alc: true` (or false only for throwaway fixtures)
- `alc_version`
- `allowed_memory_scopes` including `agent`
- `hooks.reflect: true`
- Namespaced `allowed_tools` (fail closed)

### 4. Validate

```bash
# Manifest / pack dry-run register
python scripts/business/register_domain.py --manifest business/<domain_id>/manifest.json --dry-run
```

### 5. Register (draft agents)

```http
POST /api/v1/domains/register
{ "manifest_path": "business/<domain_id>/manifest.json" }
```

Agents load as draft/registered — **not** auto-activated.

### 6. Activate (ALC gate)

`PATCH /api/v1/agents/{id}` → `active` only after ALC fields pass.

### 7. Evals & isolation

- Add pack golden under `business/<domain_id>/evals/golden/`
- Corpus overlay merges when DNA `domain` matches (see `corpus_eval.PACK_SUITE_DIRS`)
- Lessons must carry `agent_id` — never share secrets across packs

### 8. Tools

- Prefer stub adapters first (Wave 2 video pattern)
- Register in `business/security/tool-permissions/tool-permission-register.json`
- **Never** grant foreign pack agents ops tools (`billing_system`, `crm`) by default

### 9. FE

Domain filter on ops console Domain Pack panel picks up `domain_id` on agents automatically.

### 10. CI gates

| Gate | Command / check |
|------|-----------------|
| Video inventory (N3) | `python scripts/business/inventory_check.py` → PASS 114 |
| Unit suite | `pytest backend/app/tests/unit -q` |
| Multipack / security | `pytest …/test_wave4_multipack.py` |

## Anti-patterns

| Do not | Why |
|--------|-----|
| Put video business logic in `backend/app/` | Breaks N1 |
| Drop video agents for a new pack | Breaks N3 |
| Auto-promote evolution/skills | Sandbox discipline |
| Expand allow-list from user prompt text | Injection / tool misuse |

## Examples in-repo

| Pack | Role |
|------|------|
| `business/video/` | Full N3 video MMA (114) |
| `business/example_research/` | Wave 1 second pack |
| `business/example_education/` | Wave 4 third pack |

## Versioning

See `docs/domain-pack-versioning-matrix.md`.
