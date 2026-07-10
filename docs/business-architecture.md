# Business Architecture

The business operating system mirrors `structure.md` through first-party directories under `business/`, risk-tiered workflow DNA, explicit governance artifacts, and sandboxed evolution controls.

## Layout (shipped)

| Path | Role |
|------|------|
| `business/process-intelligence/` | Event logs + discovered / conformance / bottleneck artifacts |
| `business/knowledge-base/` | Rules, provenance, retrieval policy, federation exports |
| `business/distilled/` | Skills / SOPs (sandbox under `_sandbox/` until promote) |
| `business/evolution/` | DNA variants, successful variants, lessons-learned |
| `business/evals/` | Golden (≥20), regression, adversarial, historical-replay |
| `business/governance/` | Inventory, model cards, assurance, approval policy |
| `business/security/` | Controls, red-team notes |
| `business/schemas/` + `examples/` | Machine-readable contracts |

## How it connects to runtime

- FastAPI **RuntimeStore** (Postgres JSONB) holds live agents, workflows, runs, memory, knowledge graph nodes/edges, evolution variants, lessons, loop runs.
- Disk under `business/` is the **audit-friendly corpus** for PI outputs, evals, and governance documents.
- FE ops console is a thin client: lists, forms, Improve pipeline, Evolution archive.

## Design priorities

Safety → Auditability → Correctness → Efficiency → Autonomy.

See `docs/architecture.md` and `docs/self-improvement-and-orchestration.md`.
