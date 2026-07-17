# LG-12 — Frontend Graph Run Console

**Unit ID:** LG-12  
**Layer:** Frontend  
**Priority:** P0  
**Depends on:** LG-09, LG-11  

---

## 1. Goal

Replace the “empty” run experience with a **live multi-agent graph console**: topology, node statuses, event timeline, and artifacts—so operators *see* orchestration.

---

## 2. Problem / gap

`WorkflowRunConsole` / run pages emphasize logs and scaffold copy. There is no graph canvas, handoff visualization, or node-level status for supervisor teams.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-12-01 | Run detail shows interactive graph (nodes + edges) from topology API. |
| FR-12-02 | Nodes color by status: pending / running / waiting / completed / failed / interrupted. |
| FR-12-03 | Event timeline consumes stream events (handoffs highlighted). |
| FR-12-04 | Side panel: selected node state snippet + tools used. |
| FR-12-05 | Works for `engine=langgraph`; legacy shows linear step graph fallback. |
| FR-12-06 | Accessible: keyboard focus for nodes; not canvas-only. |
| NFR-12-01 | First meaningful paint without waiting for full history. |
| NFR-12-02 | Demo mode shows mock topology if backend empty. |

---

## 4. Design

### Components

```text
frontend/src/components/domain/graph/
  graph-canvas.tsx          # layout (dagre or simple ranked)
  graph-node.tsx
  graph-run-console.tsx     # composes canvas + timeline + panel
  use-graph-stream.ts
```

### Route

Enhance `/app/workflow-runs/[id]` to render `GraphRunConsole` when topology available.

### Data flow

```text
GET topology → static layout
GET run + stream → status overlays
GET graph-state (on node click) → panel
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-12-01 | API client methods: topology, graph-state, patterns |
| T-12-02 | Graph canvas MVP (SVG or light lib; avoid heavy vendor lock if possible) |
| T-12-03 | Stream hook integration |
| T-12-04 | Legacy linear fallback view |
| T-12-05 | Unit tests for status color mapping |
| T-12-06 | Manual UX checklist for empty/loading/error |

---

## 6. Acceptance criteria

- [ ] Operator can identify current node without reading raw JSON  
- [ ] Handoff events appear in timeline for supervisor fixture  
- [ ] Legacy runs still usable  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §10 HAI |
| Current console | `WorkflowRunConsole` component |
| Paths | `frontend/src/lib/routes/paths.ts` |

*End LG-12.*
