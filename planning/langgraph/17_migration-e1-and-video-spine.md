# LG-17 — Migration: E1 Onboarding + Video Spine

**Unit ID:** LG-17  
**Layer:** Backend + Frontend  
**Priority:** P0  
**Depends on:** LG-04 … LG-14  

---

## 1. Goal

Prove LangGraph is not empty: migrate **customer onboarding (E1)** and **video viral-hook spine** to `engine=langgraph`, keep human gates, and flip defaults only after gates pass.

---

## 2. Problem / gap

Without migrating real product paths, the dual engine stays academic and FE stays list-shaped.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-17-01 | `wf_customer_onboarding_v12` runs on LangGraph with ≥2 interrupt gates. |
| FR-17-02 | E1 automated test supports `GENERIC_SWARM_ENGINE_DEFAULT=langgraph`. |
| FR-17-03 | Video viral-hook DNA/graph completes with stubs + package gate. |
| FR-17-04 | FE Run now + Approvals + Graph console work for both paths. |
| FR-17-05 | Feature flag per workflow for gradual flip. |
| FR-17-06 | Rollback: set engine legacy without data loss. |
| NFR-17-01 | Performance: onboarding complete < 30s local stubs. |
| NFR-17-02 | No regression in inventory N3. |

---

## 4. Design — migration steps

```text
1. Compile onboarding DNA → pipeline + interrupt gates
2. Shadow mode: run both engines offline compare (optional)
3. Enable langgraph for admin-only workflows
4. Migrate E1 test
5. Migrate video spine pack graph
6. Default new workflows to langgraph
7. Deprecate legacy for flagship ids
```

### Rollback

`workflow.execution_engine=legacy` or env default; checkpoints retained for forensics.

---

## 5. Tasks

| ID | Task |
|----|------|
| T-17-01 | Onboarding graph IR + compile fixtures |
| T-17-02 | Port E1 test to langgraph (parametrized dual) |
| T-17-03 | Video spine graph + e2e |
| T-17-04 | FE manual checklist sign-off |
| T-17-05 | Flip flag for flagship workflows in seed data |
| T-17-06 | Deprecation warning on legacy path for those ids |

---

## 6. Acceptance criteria

- [ ] Parametrized E1 passes for both engines  
- [ ] Video spine e2e passes on langgraph  
- [ ] Operator checklist: login → run → see graph → approve ×2 → complete  
- [ ] Rollback drill documented and tested once  

---

## 7. Traceability

| Item | Link |
|------|------|
| E1 test | `test_e1_operator_path.py` |
| Video spine | `test_video_spine_e2e.py` |
| structure.md | §11.5 operator path |

*End LG-17.*
