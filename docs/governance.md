# Governance

Governance covers AI inventory, risk tiering, human approval policy, audit logging, model cards, assurance cases, and tool permission controls.

## Artifacts (shipped under `business/governance/`)

| Artifact | Purpose |
|----------|---------|
| AI inventory | Registered agents / use cases |
| Risk tiers | Autonomy ladder (observe → restricted) |
| Human approval policy | When gates fire; SLAs |
| Model card | Flagship orchestrator status |
| Assurance case | Tier-4 / high-impact justification |
| Tool permission controls | Least privilege allow-lists |

## Runtime enforcement

- Risk tier + approval policy drive **human gates** on workflow steps.
- Audit log is append-oriented for actions, tools, approvals, and evolution events.
- Tool adapters are allow-listed per agent/workflow; wildcards discouraged.
- Evolution proposals remain **sandbox-only**; canary / promote require explicit operator action.
- Self-improvement and skill sandbox never rewrite host application code.

## Commands

```bash
npm run business:governance
npm run business:security
npm run business:evolution:check
```

## Operator surfaces

- FE Approvals queue for pending gates
- Audit logs under `/app/audit-logs`
- Evolution archive + Improve pipeline for governed change

See `structure.md` risk tiers and `docs/evolution-sandbox.md`.
