# LG-10 — Domain Pack Graph Packages

**Unit ID:** LG-10  
**Layer:** Backend (+ pack assets)  
**Priority:** P1  
**Depends on:** LG-05, LG-07  

---

## 1. Goal

Allow domain packs to ship **graph definitions** (or DNA with orchestration metadata) so video and future packs get real multi-agent spines without polluting host core.

---

## 2. Problem / gap

Video has 114 agents + DNA files, but execution depth is thin stubs. Pack-specific supervisor topologies are not first-class loadable packages.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-10-01 | Pack may include `business/<domain>/graphs/*.graph.json` **or** DNA `orchestration` block. |
| FR-10-02 | Host compiler loads pack graphs by `domain_id` + graph id. |
| FR-10-03 | Video spine graph: planner → orchestrator → specialists via router/standby. |
| FR-10-04 | Viral-hook path remains runnable with stubs + HITL package gate. |
| FR-10-05 | Inventory/N3 rules unchanged (agents retained). |
| FR-10-06 | Example second pack can register a tiny supervisor graph (N2 proof). |
| NFR-10-01 | Pack graphs cannot reference host-only secrets. |
| NFR-10-02 | Cross-namespace tools still fail closed. |

---

## 4. Design

```text
business/video/
  workflows/*.dna.json      # portable IR (keep)
  graphs/
    video_spine.graph.json  # optional explicit topology
    viral_hook.graph.json
```

`pack_spine` pattern loads entry agents from pack manifest / archetype registry.

---

## 5. Tasks

| ID | Task |
|----|------|
| T-10-01 | Define pack graph JSON schema |
| T-10-02 | Loader + compiler integration |
| T-10-03 | Port viral-hook to LangGraph pack_spine |
| T-10-04 | Example_research mini supervisor graph |
| T-10-05 | Tests: inventory still 114; spine e2e on langgraph engine |

---

## 6. Acceptance criteria

- [ ] Video viral-hook completes on `engine=langgraph` with stubs  
- [ ] Second pack graph registers without host code change beyond loader  
- [ ] N3 inventory still complete  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §0.3 Domain packs |
| Video DNA | `business/video/workflows/` |
| Spine tests | `test_video_spine_e2e.py` |

*End LG-10.*
