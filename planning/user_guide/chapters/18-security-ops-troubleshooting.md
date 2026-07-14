# Chapter 18: Security, ops, and troubleshooting

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Expert  
> **Part:** Part V — Expert & production  
> **Est. time:** 60 min  
> **Final path:** `book/user_guide/chapters/18-security-ops-troubleshooting.md`


## Illustration

![Security, ops, and troubleshooting](../assets/15-security-production.svg)

*Figure: Security, ops, and troubleshooting — source `assets/15-security-production.svg`*


## Learning objectives

- Apply a production readiness checklist
- Diagnose common boot and run failures
- Apply agentic security basics (tool abuse, prompt injection awareness)

## Narrative outline (to expand into full prose)

1. Auth hardening beyond seed passwords
2. Secrets, CORS, security headers
3. Postgres runbook essentials
4. Doctor / security scripts
5. Troubleshooting matrix (symptom → check)
6. Incident: approval bypass attempts

## Hands-on labs

- [ ] Run npm run doctor and record output
- [ ] Break health with wrong DATABASE_URL; restore
- [ ] Walk rules/110-agentic-security.md highlights

## Primary sources (do not invent beyond these without verifying)

- `docs/security.md`
- `docs/troubleshooting.md`
- `backend/docs/postgres-runbook.md`
- `rules/30-security.md`
- `rules/110-agentic-security.md`

## Writing checklist (for full draft)

- [ ] Open with 1-paragraph “why this matters”
- [ ] Step-by-step commands that work on Windows PowerShell and bash where possible
- [ ] At least one “Expected result” block per major lab
- [ ] Explicit residual / non-claim callouts where relevant
- [ ] Cross-links to previous/next chapter
- [ ] Embed final SVG from `book/user_guide/assets/` (copied from this plan)

## Navigation

- TOC: [../TOC.md](../TOC.md)
- Plan: [../00_PLAN.md](../00_PLAN.md)
