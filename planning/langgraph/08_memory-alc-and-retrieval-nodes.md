# LG-08 — Memory, ALC, and Retrieval Nodes

**Unit ID:** LG-08  
**Layer:** Backend  
**Priority:** P1  
**Depends on:** LG-02, LG-07  

---

## 1. Goal

Add graph nodes for **pre-act memory retrieve**, **post-act memory write**, and **ALC lesson inject** so multi-agent runs learn per-agent without hollow empty state.

---

## 2. Problem / gap

ALC and memory scopes exist on the host but are not first-class graph stages. Supervisor handoffs lose opportunities to inject specialist lessons.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-08-01 | `memory_read` node loads scoped items into `state.memory_hits`. |
| FR-08-02 | `memory_write` node writes episodic/decision items with provenance. |
| FR-08-03 | ALC pre-act: if agent requires ALC, inject top-k lessons by `agent_id`. |
| FR-08-04 | ALC post-act: optional reflect hook writes lesson with `agent_id`. |
| FR-08-05 | Retrieval tier-0 (and tier-1 when configured) available as nodes. |
| FR-08-06 | DNA `memory_reads` / `memory_writes` map to these nodes automatically in compiler. |
| NFR-08-01 | High-impact writes respect risk tier / human review policy. |
| NFR-08-02 | Memory content treated as untrusted for prompt injection (isolate from system instructions). |

---

## 4. Design

```text
… → memory_read(agent) → agent_reason → host_tools → memory_write → …
                 ↑ ALC lessons
```

### Modules

```text
backend/app/infrastructure/langgraph_engine/nodes/
  memory_read.py
  memory_write.py
  alc_inject.py
  retrieve.py
```

---

## 5. Tasks

| ID | Task |
|----|------|
| T-08-01 | Implement memory_read/write nodes against host memory service |
| T-08-02 | ALC inject/retrieve integration tests |
| T-08-03 | Compiler auto-insert for DNA memory fields |
| T-08-04 | Injection isolation test (hostile memory text cannot expand tools) |

---

## 6. Acceptance criteria

- [ ] Agent with ALC receives ≥1 lesson in state before act (fixture)  
- [ ] Memory write appears in host memory list with provenance  
- [ ] Hostile memory cannot add `billing_system` to allow-list  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §3.3, §3.4, §0.3 ALC |
| ALC tests | `test_alc_and_domains.py` |

*End LG-08.*
