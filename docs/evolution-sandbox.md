# Evolution Sandbox

Evolution only proposes, tests, compares, requests approval, canaries, and rolls back. It **never mutates production DNA directly**.

## Shipped loop

```text
propose (sandbox_only)
  → sandbox_evaluate (disk corpus: golden / regression / adversarial / historical)
  → fitness_metrics on variant
  → canary approve  OR  versioned promote (new versions[] entry)
  → rollback restores previous active_version
```

## APIs

- `POST /api/v1/evolution/variants` — propose (blocks `direct_production_mutation`)
- `POST /api/v1/evolution/variants/{id}/evaluate` — corpus eval
- `POST /api/v1/evolution/variants/{id}/promote` — `mode=canary|promote`
- `POST /api/v1/evolution/variants/{id}/rollback`
- `GET /api/v1/evolution/archive` — population ranked by fitness

## Self-improvement entry points

- Auto-reflect after terminal runs (`GENERIC_SWARM_AUTO_REFLECT`)
- `POST /api/v1/improvement/auto-propose` — build sandbox variant from failures
- FE: Improve pipeline on run detail; archive at `/app/evolution`

## Code

- `backend/app/infrastructure/evolution/corpus_eval.py`
- Runtime methods on `RuntimeServices` (`propose_evolution_variant`, `sandbox_evaluate_variant`, …)
- Tests: `test_p3_pi_evolution.py`, `test_scorecard_controls.py`, E1 e2e

## Policy

- `auto_promote` always forbidden
- Full promote requires owner/admin
- Rollback plan recorded on canary variants
