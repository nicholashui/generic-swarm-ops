# Evaluation

Evaluation cards report quality, compliance, cycle time, escalation, hallucination, unauthorized tool attempts, and cost per case. **Promotion stays manual** — the harness never auto-promotes production DNA.

## Corpus (shipped)

Under `business/evals/`:

| Suite | Role |
|-------|------|
| `golden-tasks/` | ≥20 golden cases for primary workflows |
| `regression/` | Prevent known-good behavior from regressing |
| `adversarial/` | Prompt injection, tool misuse, boundary abuse |
| `historical-replay/` | Replay completed runs / fixtures |
| Retrieval fixtures | Tier-0/1 search quality checks |

Root harness: `npm run business:eval` (and dry-run variants).

## Runtime evaluation

- Workflow DNA may set `block_on_fail` so failed required checks stop the run.
- Evolution **sandbox eval** scores variants against the disk corpus before canary.
- Fitness metrics feed the population archive (`GET /api/v1/evolution/archive`).
- Self-improvement **reflect** extracts lessons from terminal runs; optional LLM critic.

## Frontend

- Evaluations list/detail under `/app/evaluations`.
- Run detail **Improve** pipeline: Reflect → Propose → Evaluate → Canary.
- Evolution archive at `/app/evolution`.

## Evidence

- `mark_100_verification.md`
- Backend unit tests including evolution / improvement suites
- E1 checklist: `reviews/e1_operator_checklist.md`
