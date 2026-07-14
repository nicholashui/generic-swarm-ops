# Chapter 05: Your first workflow run (E1 path)

> **Status:** PLAN SCAFFOLD — detailed outline for full prose in `book/user_guide/`  
> **Level:** Beginner → Intermediate  
> **Part:** Part II — Operator core  
> **Est. time:** 60 min  
> **Final path:** `book/user_guide/chapters/05-first-workflow-run-e1.md`


## Illustration

![Your first workflow run (E1 path)](../assets/05-e1-operator-path.svg)

*Figure: Your first workflow run (E1 path) — source `assets/05-e1-operator-path.svg`*


## Learning objectives

- Complete the full E1 path end-to-end
- Supply required payload (case_id) for flagship workflow
- Observe run states and terminal completion

## Narrative outline (to expand into full prose)

1. What E1 proves (product bar)
2. Flagship workflow wf_customer_onboarding_v12
3. Step-by-step UI path: list → run → approve → complete → improve
4. API equivalent curl sequence
5. Reading run events / console
6. Common failures: missing case_id, wrong role, demoMode mocks
7. Automated proof: test_e1_operator_path.py

## Hands-on labs

- [ ] Lab E1-UI: complete path in browser
- [ ] Lab E1-API: login + run via API with token
- [ ] Lab E1-Test: run e2e test and read assertion names

## Primary sources (do not invent beyond these without verifying)

- `docs/usage.md`
- `reviews/e1_operator_checklist.md`
- `backend/app/tests/e2e/test_e1_operator_path.py`
- `EXECUTABLE_PRODUCT.md`

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
