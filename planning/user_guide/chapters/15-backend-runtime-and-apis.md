# Chapter 15: Backend runtime and APIs

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Expert  
> **Part:** Part V — Expert & production  
> **Est. time:** 75 min  
> **Final path:** `book/user_guide/chapters/15-backend-runtime-and-apis.md`


## Illustration

![Backend runtime and APIs](../assets/02-system-overview.svg)

*Figure: Backend runtime and APIs — source `assets/02-system-overview.svg`*


## Learning objectives

- Locate runtime entry points and route modules
- Authenticate and call core APIs with request_id awareness
- Explain store backends (Postgres vs JSON)

## Narrative outline (to expand into full prose)

1. app.main and middleware
2. RuntimeServices responsibilities
3. Route map: auth, workflows, runs, approvals, domains, improvement…
4. OpenAPI export
5. Workers and long jobs (if any)
6. Testing pyramid: unit vs e2e
7. Reading tool_effects and runtime.json snapshot

## Hands-on labs

- [ ] Export or open OpenAPI; find recommend-workflow
- [ ] Trace recommend_video_workflow in runtime.py
- [ ] Run targeted pytest for special skills + archetype

## Primary sources (do not invent beyond these without verifying)

- `backend/README.md`
- `backend.md / book/design_phase/book.backend_hk.md`
- `backend/app/api/v1/routes/`
- `backend/app/runtime.py`

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
