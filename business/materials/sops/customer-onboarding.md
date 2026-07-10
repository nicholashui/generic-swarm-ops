# SOP: Customer Onboarding

**ID:** sop_customer_onboarding_v1  
**Owner:** operations  
**Risk tier:** tier_4_execute_with_gate  
**Last reviewed:** 2026-07-09

## Purpose

Onboard a signed customer with verified contract data, CRM record creation, billing activation (human-gated), and a welcome packet — with full audit and rollback.

## Preconditions

1. Contract status is signed.
2. Customer risk score is within policy threshold, or legal approval is recorded.
3. Billing details are present.

## Steps

1. **Verify contract** — compliance review of signed terms.
2. **Create CRM record** — reversible customer master data write.
3. **Activate billing** — irreversible commercial action; **human approval required**.
4. **Send welcome packet** — customer communication.
5. **Audit and close** — verification checks and audit log completeness.

## Guardrails

- Human approval required when risk tier is high, contract exceptions are detected, or the tool action is irreversible.
- Rollback: disable customer record, void initial invoice, notify ops owner.

## Provenance

- Structure reference: `structure.md` §4 Workflow DNA.
- Example DNA: `business/examples/workflow-dna.example.json`.
