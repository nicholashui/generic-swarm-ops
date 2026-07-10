# Workflow DNA

Workflow DNA captures bounded state-graph steps, tools, agents, verification, rollback, memory reads and writes, and audit logging requirements.

## Contract (every production DNA)

- Bounded steps with explicit agents + tools
- Memory reads / writes with scopes
- Guardrails (human-approval conditions for high-risk / irreversible actions)
- Verification `required_checks` (and optional `block_on_fail`)
- Rollback / reversibility plan
- Fitness metrics
- Audit-log write requirement

Schemas and examples live under `business/schemas/` and `business/examples/`.

## Runtime execution (shipped)

1. Operator starts a run (`POST` workflow runs or FE **Run now**).
2. Runtime walks the graph; tools call **local adapters** and write durable `tool_effects`.
3. Human gates pause irreversible steps until approval.
4. On terminal status, **auto-reflect** may write lessons and optionally auto-propose a **sandbox-only** variant.
5. Variants never mutate production DNA until evaluate → canary / versioned promote.

## Validation

```bash
npm run business:validate
npm run business:evolution:check
```

Validator rejects production DNA when high-risk actions lack gates, irreversible actions lack rollback, provenance is missing, or audit writes are undeclared.

## Flagship example

Customer onboarding DNA (`wf_customer_onboarding_v12`) exercises intake → tools → billing human gate → complete, and is covered by the E1 operator path test.
