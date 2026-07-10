# Handoff

## Current status

- Product bar **~100** with E1 operator path **PASS** (`reviews/e1_operator_checklist.md`, `test_e1_operator_path`).
- Full self-improvement backlog + guided Improve → Evaluate → Canary UI.
- Docs: `docs/self-improvement-and-orchestration.md`
- **Adoption `adoption.md` v2.3 rethink:** N3 kept; L0/L1/L2 maturity; catalog ≠ full SPEC; ALC hard-gate on active; process index before DNA depth; `video.*` vs ops orchestrator namespace.
- **`adoption_plan.md` v3.2 rethink:** §0 principles + critical path §0.3; §15 playbooks as reference depth; avoid SPEC/DNA theater.
- **`adoption_plan_hk.md`:** Traditional Chinese full translation of `adoption_plan.md` v3.2.

### Shipped backlog

| Item | How |
|------|-----|
| Auto-reflect | On every terminal run status (`GENERIC_SWARM_AUTO_REFLECT=true`) |
| FE Improve | Run detail: Reflect + Propose sandbox variant |
| LLM critic | Optional `GENERIC_SWARM_LLM_CRITIC_ENABLED` + API base |
| Population archive | `/app/evolution` + `GET /api/v1/evolution/archive` |
| Embeddings | Hashing Tier-0 embed; optional `GENERIC_SWARM_PGVECTOR_ENABLED` |
| Federation | `POST /api/v1/knowledge/graph/federate` → Cypher/JSON (+ optional Neo4j) |
| Skill sandbox | `/api/v1/improvement/skills/*` → `_sandbox/` then explicit promote |

### Tests

- Backend unit suite green (includes `test_full_improvement_backlog`)
- Frontend typecheck + vitest green

### Seed login

- `admin@example.com` / `admin-password`
