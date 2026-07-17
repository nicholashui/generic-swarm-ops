# LG-13 — Frontend Graph Authoring and Topology

**Unit ID:** LG-13  
**Layer:** Frontend  
**Priority:** P1  
**Depends on:** LG-05, LG-11  

---

## 1. Goal

Let operators **choose orchestration patterns** and inspect/edit high-level topology metadata for workflows (not free-form ungoverned code), so multi-orchestration is productized.

---

## 2. Problem / gap

Workflow detail UI is mostly static description. No pattern picker (supervisor vs pipeline), no specialist multi-select, no topology preview before run.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-13-01 | Workflow detail shows current `orchestration.pattern` and topology preview. |
| FR-13-02 | Pattern picker from `GET /orchestration/patterns`. |
| FR-13-03 | Supervisor config UI: supervisor agent + specialists multi-select (from agents list). |
| FR-13-04 | Save writes workflow metadata / draft DNA orchestration block via existing update APIs (or new PATCH if needed). |
| FR-13-05 | Production activate still blocked if validators fail. |
| FR-13-06 | Domain pack workflows can show pack graph read-only when not owner. |
| NFR-13-01 | Authoring does not allow arbitrary Python. |
| NFR-13-02 | Changes go through RBAC `workflows:update`. |

---

## 4. Design

```text
Workflow detail
  ├─ Topology preview (GraphCanvas read-only)
  ├─ Pattern picker
  ├─ Pattern config form (JSON schema from catalog)
  └─ Save draft → backend validate
```

Optional later: drag edges (P2). MVP is **form-driven pattern config** + live preview.

---

## 5. Tasks

| ID | Task |
|----|------|
| T-13-01 | Patterns client + form schemas |
| T-13-02 | PatternConfigForm components per pattern |
| T-13-03 | Wire save to backend |
| T-13-04 | Preview recompute on config change |
| T-13-05 | FE tests for form validation |

---

## 6. Acceptance criteria

- [ ] User can switch workflow from pipeline → supervisor and see topology change in preview  
- [ ] Invalid specialist id rejected  
- [ ] Viewer role cannot save  

---

## 7. Traceability

| Item | Link |
|------|------|
| Workflow UI | `frontend/src/app/app/[...slug]/page.tsx` workflows section |
| structure.md | §4 DNA |

*End LG-13.*
