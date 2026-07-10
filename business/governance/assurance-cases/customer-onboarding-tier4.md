# Assurance Case — Tier-4 Customer Onboarding

## Restricted use case

**Customer onboarding with irreversible billing activation** under risk tier  
`tier_4_execute_with_gate` for workflow `wf_customer_onboarding_v12`.

## Claim

The system will not activate billing without an explicit human approval when the step is marked irreversible / human-gated, and will not promote sandbox DNA into production without evaluation and versioning.

## Evidence

| Claim element | Evidence |
|---------------|----------|
| Human gate on billing | Workflow DNA step `activate_billing` has `human_gate_required` + `irreversible`; tests `test_human_gate_on_irreversible_step`, `test_real_execution` |
| Tool allow-list | Agent `allowed_tools` checked in `_execute_run`; `test_tool_not_on_allow_list_denied` |
| No tier-5 start | `test_tier_5_start_denied` |
| Audit trail | `tool.executed` audits + `tool_effects` collection; run audit events |
| Evolution safety | `test_evolution_propose_blocks_direct_mutation`, `test_p3_pi_evolution` canary/rollback |
| Eval corpus | ≥20 golden tasks under `business/evals/golden-tasks/`; regression + adversarial fixtures |
| Durability | Postgres `runtime_state`; `test_postgres_restart` |

## Safety argument

1. **Control plane before model** — tool allow-list, memory scopes, and gates are enforced in the runtime, not left to LLM compliance.
2. **Fail closed** — missing agent/tool/adapter or denied scope fails the step/run.
3. **Separation of evolution** — sandbox variants never write production DNA on propose/evaluate; promote only appends a versioned canary entry; rollback restores prior `active_version`.
4. **Observability** — process intelligence artifacts and audit logs retain provenance for post-incident review.

## Compliance argument

- Aligns with structure.md autonomy risk tiers (§6.1) and human approval policy.
- AI inventory entry covers orchestrator + evolution sandbox systems.
- Model card documents limitations and review cadence.

## Human oversight design

| Trigger | Reviewer role | Action |
|---------|---------------|--------|
| Billing activation step | Reviewer / manager | Approve or reject via approvals API |
| Evolution canary promote | Admin / owner | Explicit promote after sandbox pass |
| Tier-5 workflows | Owner | Start denied |

## Residual risks

- Local adapters may not match real CRM/billing failure modes.
- Demo tokens if left enabled could confuse auth posture (prefer password login).
- Incomplete OpenAPI consumer coverage on some secondary routes.

## Approval decision

| Field | Value |
|-------|--------|
| Decision | **Approved for local ops / canary** (not unrestricted production) |
| Conditions | Demo mode off for ops; Postgres up; human gate retained on billing |
| Approver role | Governance (seed document) |
| Date | 2026-07-09 |

## Provenance

- `source_refs`: `structure.md#6`, `business/governance/human-approval-policy/policy.md`, `business/governance/model-cards/customer-onboarding-orchestrator.md`
- `captured_by`: p4_governance_seed
- `recorded_at`: 2026-07-09
