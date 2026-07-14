# Chapter 06: Approvals, risk tiers, and audit

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Intermediate  
> **Part:** Part II — Operator core  
> **Est. time:** 45 min  
> **Final path:** `book/user_guide/chapters/06-approvals-risk-audit.md`


## Illustration

![Approvals, risk tiers, and audit](../assets/06-governance-gates.svg)

*Figure: Approvals, risk tiers, and audit — source `assets/06-governance-gates.svg`*


## Learning objectives

- Decide when a step needs human approval
- Approve/reject with rationale and find audit trail
- Connect risk tiers R0–R4 to operator behavior

## Narrative outline (to expand into full prose)

1. Risk tier model and irreversible actions
2. Approvals queue UX and decision panel
3. Audit logs: what is recorded (who, when, decision, tool_effects)
4. request_id for support / debugging
5. Governance artifacts under business/governance/
6. Rules: 60-human-approval, 90-governance-risk

## Hands-on labs

- [ ] Force a billing gate and approve as reviewer
- [ ] Find the matching audit log entry
- [ ] Reject once and observe run outcome

## Primary sources (do not invent beyond these without verifying)

- `docs/governance.md`
- `docs/security.md`
- `business/governance/`
- `rules/60-human-approval.md`

## Writing checklist (for full draft)

- [ ] Open with 1-paragraph “why this matters”
- [ ] Step-by-step commands that work on Windows PowerShell and bash where possible
- [ ] At least one “Expected result” block per major lab
- [ ] Explicit residual / non-claim callouts where relevant
- [ ] Cross-links to previous/next chapter
- [ ] Embed final SVG from `book/user_guide/assets/` (copied from this plan)

## Navigation

- 繁體中文：[`06-approvals-risk-audit_hk.md`](./06-approvals-risk-audit_hk.md)

- TOC: [../TOC.md](../TOC.md)
- Master: [../user_guide.md](../user_guide.md)
- Plan: [../../../planning/user_guide/00_PLAN.md](../../../planning/user_guide/00_PLAN.md)
