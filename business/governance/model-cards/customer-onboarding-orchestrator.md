# Model Card — Customer Onboarding Orchestrator

| Field | Value |
|-------|--------|
| **Model / system name** | Customer Onboarding Multi-Agent Workflow |
| **Identifier** | `wf_customer_onboarding_v12` + agents (`business_orchestrator`, `finance_ops_agent`, …) |
| **Version** | 1.2 (runtime DNA; local control plane) |
| **Owner** | Platform / Operations (generic-swarm-ops demo org) |
| **Status** | Active MVP — Postgres-backed control plane; local tool adapters |
| **Risk tier coverage** | Up to **tier_4_execute_with_gate** (billing activation) |
| **Approved use cases** | Guided customer onboarding: contract verify → CRM → gated billing → welcome → audit |
| **Out of scope** | Fully autonomous tier-5 actions; silent production DNA mutation; external CRM/billing without adapters |

## Intended use

- Execute the flagship onboarding workflow under risk-tier and human-gate controls.
- Produce durable audit, tool_effects, memory writes, and evaluation records.
- Support sandbox evolution with canary-only promotion (never auto-promote).

## Known limitations

- Tool adapters are **local/file side-effect** implementations (not live vendor CRM/email).
- Retrieval is keyword/provenance-first (Tier-0); multi-hop graph retrieval is optional later.
- Demo static bearer tokens are smoke-only; ops should use password login.

## Evaluation evidence

| Suite | Location |
|-------|----------|
| Golden tasks (≥20) | `business/evals/golden-tasks/` |
| Regression | `business/evals/regression-tests/` |
| Adversarial | `business/evals/adversarial-tests/` |
| Historical replay | `business/evals/historical-replay/` |
| Backend controls | `backend/app/tests/unit/test_scorecard_controls.py`, `test_real_execution.py`, `test_p3_pi_evolution.py` |

## Security controls

- Agent `allowed_tools` enforced outside the model.
- Memory scope read/write checks.
- Human gate on irreversible billing step.
- Evolution: direct production mutation blocked; versioned canary promote + rollback.
- Request ids (`X-Request-ID`) on API mutations for audit correlation.

## Review cadence

- Before any canary promote: sandbox eval must pass corpus suites.
- After material DNA change: re-run golden + regression + adversarial.
- Inventory update when risk tier max or owner changes.

## Provenance

- `source_refs`: `structure.md#4`, `structure.md#6`, `business/materials/sops/customer-onboarding.md`, this model card
- `captured_by`: p4_governance_seed
- `recorded_at`: 2026-07-09
