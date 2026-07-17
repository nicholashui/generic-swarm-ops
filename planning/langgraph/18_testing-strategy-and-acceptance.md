# LG-18 — Testing Strategy and Acceptance

**Unit ID:** LG-18  
**Layer:** Backend + Frontend  
**Priority:** P0  
**Depends on:** all implementation units  

---

## 1. Goal

Define a **layered test matrix** so LangGraph adoption cannot ship “empty graphs” that pass smoke but fail multi-agent reality.

---

## 2. Requirements

| ID | Requirement |
|----|-------------|
| FR-18-01 | Unit tests for compiler, patterns, bridge, tools, state reducers. |
| FR-18-02 | Integration tests with MemorySaver (no external network). |
| FR-18-03 | Postgres checkpointer tests gated on DATABASE_URL. |
| FR-18-04 | E2E E1 dual-engine. |
| FR-18-05 | FE unit tests for graph status mapping + approval interrupt UI. |
| FR-18-06 | Optional Playwright: graph console visible after run. |
| FR-18-07 | CI job `langgraph` or marker `lg` for new tests. |
| NFR-18-01 | No live LLM required for CI (heuristic nodes / fakes). |
| NFR-18-02 | Tests hermetic: no paid LangSmith. |

---

## 3. Design — test pyramid

```text
        E2E (E1, video spine)
       /                    \
  API integration        FE component
       \                    /
        Unit: compiler, patterns, broker, state
```

### Suggested paths

```text
backend/app/tests/unit/test_lg_compiler.py
backend/app/tests/unit/test_lg_supervisor.py
backend/app/tests/unit/test_lg_hitl_bridge.py
backend/app/tests/unit/test_lg_checkpointer.py
backend/app/tests/e2e/test_e1_operator_path.py  # parametrize engine
frontend/tests/unit/graph-status.test.ts
frontend/tests/unit/interrupt-panel.test.ts
```

---

## 4. Tasks

| ID | Task |
|----|------|
| T-18-01 | Create test file skeleton + fixtures |
| T-18-02 | CI marker/docs for running lg suite |
| T-18-03 | Coverage checklist vs LG-01…17 ACs |
| T-18-04 | Failure taxonomy (compile / authorize / interrupt / budget) |

---

## 5. Program acceptance (ship bar)

| Gate | Pass condition |
|------|----------------|
| G1 | Dual-engine E1 green |
| G2 | ≥1 supervisor multi-agent test green |
| G3 | FE graph console shows nodes for langgraph run |
| G4 | HITL interrupt ×2 on onboarding |
| G5 | Security denial tests green |
| G6 | Default can remain legacy; flagship opt-in langgraph documented |

---

## 6. Traceability

| Item | Link |
|------|------|
| Existing e2e | `app/tests/e2e/` |
| structure.md | §11.6 verification |

*End LG-18.*
