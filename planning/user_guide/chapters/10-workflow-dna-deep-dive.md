# Chapter 10: Workflow DNA deep dive

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Intermediate → Advanced  
> **Part:** Part III — Domains & video pack  
> **Est. time:** 60 min  
> **Final path:** `book/user_guide/chapters/10-workflow-dna-deep-dive.md`


## Illustration

![Workflow DNA deep dive](../assets/10-workflow-dna.svg)

*Figure: Workflow DNA deep dive — source `assets/10-workflow-dna.svg`*


## Learning objectives

- Read a .dna.json file and explain each major field
- Describe sandbox → evaluate → canary → promote
- Locate viral-hook DNA and customer onboarding DNA

## Narrative outline (to expand into full prose)

1. DNA as executable process graph (not free-form chat)
2. Step structure: agent, tools, action_type, memory, verification
3. Human gates and risk metadata
4. Versioning and promote rules
5. Validation commands business:validate / evolution checks
6. Authoring checklist before production

## Hands-on labs

- [ ] Diff two DNA files (onboarding vs viral-hook)
- [ ] Run DNA schema/validation tests if available
- [ ] Sketch a 3-step DNA for a toy process on paper

## Primary sources (do not invent beyond these without verifying)

- `docs/workflow-dna.md`
- `rules/100-evolution-sandbox.md`
- `business/video/workflows/`
- `skills workflow-dna`

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
