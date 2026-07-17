# LG-11 — Backend API Surface for Graphs

**Unit ID:** LG-11  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-01 … LG-09  

---

## 1. Goal

Expose **graph-aware** control-plane endpoints (topology, state snapshot, resume, cancel) while keeping `/api/v1` the single public surface—no separate LangGraph server required for the product.

---

## 2. Problem / gap

APIs know workflows/runs/approvals but not topology, interrupts, or thread checkpoints. FE cannot build a non-empty orchestration UI without new fields/endpoints.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-11-01 | `GET /workflows/{id}/topology` → nodes, edges, pattern, engine. |
| FR-11-02 | `GET /workflow-runs/{id}` includes engine, thread_id, current_node, interrupt summary. |
| FR-11-03 | `GET /workflow-runs/{id}/graph-state` → redacted HostGraphState snapshot. |
| FR-11-04 | `POST /workflow-runs/{id}/resume` optional alias to approval decision for graph resumes with overrides. |
| FR-11-05 | `POST /workflow-runs/dispatch` remains; may auto-invoke for langgraph engine (document behavior). |
| FR-11-06 | `GET /orchestration/patterns` → pattern catalog. |
| FR-11-07 | OpenAPI updated; FE types regenerable. |
| NFR-11-01 | Graph-state endpoint strips secrets. |
| NFR-11-02 | Rate limits apply to resume/start as today. |

---

## 4. Design

Prefer **extending** existing routers over new microservice.

| Method | Path | Notes |
|--------|------|-------|
| GET | `/api/v1/workflows/{id}/topology` | Compile-time topology |
| GET | `/api/v1/workflow-runs/{id}/graph-state` | Checkpoint projection |
| GET | `/api/v1/orchestration/patterns` | Catalog |
| POST | `/api/v1/workflow-runs/{id}/resume` | Optional convenience |

Start/run body extension:

```json
{
  "input_payload": { "case_id": "..." },
  "engine": "langgraph",
  "orchestration": { "pattern": "supervisor" }
}
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-11-01 | Topology route + service |
| T-11-02 | Graph-state route + redaction |
| T-11-03 | Patterns catalog route |
| T-11-04 | Extend run schema in OpenAPI |
| T-11-05 | Contract tests for FE |

---

## 6. Acceptance criteria

- [ ] OpenAPI lists new paths  
- [ ] Topology for onboarding returns ≥5 nodes when compiled  
- [ ] Graph-state redacts configured sensitive keys  

---

## 7. Traceability

| Item | Link |
|------|------|
| Router | `backend/app/api/v1/router.py` |
| OpenAPI export | existing scripts |

*End LG-11.*
