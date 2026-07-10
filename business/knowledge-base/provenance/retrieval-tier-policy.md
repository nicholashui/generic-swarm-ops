# Retrieval tier policy (product bar)

Aligned with `structure.md` §3.4 — **cost-tiered hybrid retrieval**.

## What we ship for mark 100

| Tier | Implementation | Status |
|------|----------------|--------|
| **0** | Keyword search over indexed knowledge docs; **mandatory** `source_refs` / provenance on every hit | **Default** |
| **1** | LightRAG-**lite**: entity-link expansion when query is relational (e.g. “related”, “which policy”) | **Minimal multi-hop** |
| **2** | RAPTOR-style hierarchical summaries | **Deferred** (non-goal) |

## Escalation rule

1. Always run Tier 0.
2. Escalate to Tier 1 only when the query needs relationships / multi-hop **or** `multi_hop=true` is requested.
3. Do not auto-promote retrieval stacks; provenance is required at every tier.

## Non-goals (explicit)

- Full LightRAG vendor install / cloud vector lock-in.
- Pixel-perfect embedding quality vs commercial RAG.
- Tier-2 global synthesis trees.

## Code

- `backend/app/infrastructure/knowledge/retrieval.py`
- `RuntimeServices.search_knowledge`
- Tests: `backend/app/tests/unit/test_retrieval.py`
- Eval fixtures: `business/evals/retrieval/`

## Provenance

- `source_refs`: `structure.md#3.4`, this file
- `captured_by`: p5_retrieval
- `recorded_at`: 2026-07-09
