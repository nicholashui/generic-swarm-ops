# Human Approval Policy

## Purpose

Define when a human must approve agent or workflow actions so autonomy stays bounded
(structure.md §6.1–6.2, Safety → Auditability → Correctness).

## Mandatory approval triggers

Human approval is **required** when any of the following hold:

| Trigger | Examples |
|---------|----------|
| Risk tier 2 (Draft) | Preparing outbound content, customer-facing drafts |
| Risk tier 4 (Execute + gate) | Critical/irreversible step in an otherwise executable workflow |
| Risk tier 5 (Restricted) | No autonomous start until an assurance case exists |
| Irreversible tools | Billing activation, production deletes, credentialed external writes |
| Exception paths | Contract exceptions, policy overrides |
| High-impact memory writes | New semantic rules without provenance |
| Tool permission register says so | `approval_requirement` / `requires_approval` on the tool |

## Roles

| Role | Can approve |
|------|-------------|
| owner / admin | Any org-scoped approval |
| manager | Operational approvals for assigned workflows |
| operator | View only (cannot approve unless elevated) |

## Process

1. Runtime pauses step with status `waiting_for_approval` and creates an approval request.
2. Reviewer sees risk tier, step, tools, and evidence refs.
3. Approve → resume run; Reject → fail closed with audit entry.
4. Approvals are immutable audit records (who, when, reason).

## SLAs (MVP defaults)

| Risk tier | Target response |
|-----------|-----------------|
| tier_2_draft | 1 business day |
| tier_4_execute_with_gate | 4 business hours for critical commercial steps |
| tier_5_restricted | No auto-SLA; governance officer assignment required |

## Exceptions

Temporary waiver requires:

- Written reason
- Time-bound expiry
- Owner + governance officer dual acknowledgment
- Entry in audit log

## Related artifacts

- `business/governance/use-case-risk-tiering/risk-tiers.json`
- `business/security/tool-permissions/tool-permission-register.json`
- `business/governance/assurance-cases/`
