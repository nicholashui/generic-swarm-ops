# Chapter 16: Frontend deep dive

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Expert  
> **Part:** Part V — Expert & production  
> **Est. time:** 60 min  
> **Final path:** `book/user_guide/chapters/16-frontend-deep-dive.md`


## Illustration

![Frontend deep dive](../assets/04-console-map.svg)

*Figure: Frontend deep dive — source `assets/04-console-map.svg`*


## Learning objectives

- Explain client auth cookie and live-data facade
- Wire a new panel to backendApi safely
- Keep demoMode opt-in only

## Narrative outline (to expand into full prose)

1. App shell, sidebar, slug router
2. backendApi client patterns
3. product-data demo vs live
4. Forms: Zod + RHF + formatMutationError
5. Improve pipeline and evolution panels
6. Vitest + Playwright smoke
7. Adding Domains-style features without forking architecture

## Hands-on labs

- [ ] Read client.ts recommend + special skills methods
- [ ] Run frontend unit product-slice tests
- [ ] Trace env.demoMode default in env.ts

## Primary sources (do not invent beyond these without verifying)

- `frontend/README.md`
- `frontend/src/lib/api/client.ts`
- `frontend/src/lib/config/env.ts`
- `frontend/docs/api/frontend-api-contract.md`

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
