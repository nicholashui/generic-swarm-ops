# Skill: Self-improvement loop (governed)

## When to use

After a failed, gated, or completed workflow run when you want the system to learn
without mutating production DNA.

## Steps

1. `POST /api/v1/improvement/reflect/{run_id}` — extract lessons.
2. Review `GET /api/v1/improvement/lessons`.
3. Optionally `POST /api/v1/improvement/auto-propose` with `{ "workflow_id", "run_id" }`.
4. Run sandbox eval + canary path only (never auto-promote).
5. Or run a full Loop: `POST /api/v1/loops/run` with workflow_id and stop conditions.

## Guardrails

- Sandbox variants only for DNA changes.
- Human gates for tier ≥4 irreversible steps.
- Provenance on every lesson and graph node.

## Provenance

- frameworks: self-evolving agents, loop engineering, agents-k1 lite
- captured_by: improvement_implementation
- recorded_at: 2026-07-09
