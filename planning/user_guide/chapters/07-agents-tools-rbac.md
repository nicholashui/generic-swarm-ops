# Chapter 07: Agents, tools, and RBAC

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Intermediate  
> **Part:** Part II — Operator core  
> **Est. time:** 45 min  
> **Final path:** `book/user_guide/chapters/07-agents-tools-rbac.md`


## Illustration

![Agents, tools, and RBAC](../assets/07-agents-tools.svg)

*Figure: Agents, tools, and RBAC — source `assets/07-agents-tools.svg`*


## Learning objectives

- Create or inspect an agent with allowed_tools
- Explain why tools outside allow-list fail
- Map roles to permissions on key screens

## Narrative outline (to expand into full prose)

1. Agent record fields and statuses
2. Tool adapters catalog (ops tools + video stubs)
3. Allow-list enforcement at runtime
4. RBAC permissions types
5. API keys vs user sessions
6. ALC / lessons attachment to agents (preview of ch14)

## Hands-on labs

- [ ] Create an agent via UI form (live mode)
- [ ] Attempt a tool not on allow-list (expect controlled failure)
- [ ] Compare admin vs operator visible nav items

## Primary sources (do not invent beyond these without verifying)

- `docs/agents.md`
- `frontend/src/types/permissions.ts`
- `backend/app/infrastructure/tools/`

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
