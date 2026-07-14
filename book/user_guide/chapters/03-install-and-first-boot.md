# Chapter 03: Install and first boot

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Beginner  
> **Part:** Part I — Foundations  
> **Est. time:** 45–90 min  
> **Final path:** `book/user_guide/chapters/03-install-and-first-boot.md`


## Illustration

![Install and first boot](../assets/03-install-boot.svg)

*Figure: Install and first boot — source `assets/03-install-boot.svg`*


## Learning objectives

- Bootstrap the repo and pass doctor checks
- Start backend and hit health/ready
- Start frontend with live APIs (demoMode off)

## Narrative outline (to expand into full prose)

1. Prerequisites (OS, Node, Python, pnpm, optional Docker Postgres)
2. npm run bootstrap / doctor / sync
3. Backend: pip install -e ., uvicorn, .env and DATABASE_URL options
4. JSON-file mode vs Postgres (when degraded is OK for learning)
5. Frontend: NEXT_PUBLIC_DEMO_MODE must not be true for real product path
6. Seed login admin@example.com / admin-password
7. Troubleshooting first boot (ports, CORS, PYTHONPATH)

## Hands-on labs

- [ ] Lab A: backend health/live/ready curl or browser
- [ ] Lab B: frontend login and land on Dashboard
- [ ] Lab C: intentionally set demoMode true, see mock behavior, then restore false

## Primary sources (do not invent beyond these without verifying)

- `docs/installation.md`
- `docs/usage.md`
- `backend/docs/postgres-runbook.md`
- `frontend/README.md`
- `frontend/.env.example`

## Writing checklist (for full draft)

- [ ] Open with 1-paragraph “why this matters”
- [ ] Step-by-step commands that work on Windows PowerShell and bash where possible
- [ ] At least one “Expected result” block per major lab
- [ ] Explicit residual / non-claim callouts where relevant
- [ ] Cross-links to previous/next chapter
- [ ] Embed final SVG from `book/user_guide/assets/` (copied from this plan)

## Navigation

- 繁體中文：[`03-install-and-first-boot_hk.md`](./03-install-and-first-boot_hk.md)

- TOC: [../TOC.md](../TOC.md)
- Master: [../user_guide.md](../user_guide.md)
- Plan: [../../../planning/user_guide/00_PLAN.md](../../../planning/user_guide/00_PLAN.md)
