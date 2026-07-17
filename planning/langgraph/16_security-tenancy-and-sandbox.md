# LG-16 — Security, Tenancy, and Sandbox

**Unit ID:** LG-16  
**Layer:** Backend  
**Priority:** P0  
**Depends on:** LG-03, LG-07  

---

## 1. Goal

Hard-enforce **tenant isolation**, **tool blast-radius**, **budget caps**, and **sandbox separation** for LangGraph runs so multi-agent power does not increase attack surface unchecked.

---

## 2. Problem / gap

More nodes and free-form messages increase prompt-injection and cross-tenant risk. Checkpoints and stream payloads can leak data if not redacted.

---

## 3. Requirements

| ID | Requirement |
|----|-------------|
| FR-16-01 | thread_id always org-scoped; cross-org access denied. |
| FR-16-02 | Graph sandbox env for evolution: separate checkpoint namespace `sandbox:`. |
| FR-16-03 | Per-run limits: max nodes visits, max tool calls, max tokens, wall clock. |
| FR-16-04 | Untrusted content (memory, tools, user input) never concatenated into privileged instruction channel without delimiters. |
| FR-16-05 | Red-team tests: tool allow-list expansion attempts, cross-namespace tools. |
| FR-16-06 | Audit every engine start/resume/cancel. |
| NFR-16-01 | Default deny on missing agent/tool binding. |
| NFR-16-02 | Rate limits on run start/resume. |

---

## 4. Design

| Control | Implementation |
|---------|----------------|
| Tenancy | thread_id prefix + authz on all graph APIs |
| Budgets | metrics counters; pre-node hooks abort |
| Sandbox | `checkpoint_ns=sandbox:{variant_id}` |
| Injection | separate state fields; tool broker ignores model-suggested allow-list changes |
| Redaction | graph-state GET filter |

---

## 5. Tasks

| ID | Task |
|----|------|
| T-16-01 | Budget middleware for graph nodes |
| T-16-02 | Sandbox namespace isolation tests |
| T-16-03 | Extend red-team suite for supervisor injection |
| T-16-04 | Audit event catalog update |
| T-16-05 | Threat model note in this file appendix |

---

## 6. Acceptance criteria

- [ ] Cross-org resume fails  
- [ ] Budget exceeded fails run safely  
- [ ] Injection fixture cannot call disallowed tool  

---

## 7. Traceability

| Item | Link |
|------|------|
| structure.md | §7 Security |
| OWASP | LLM01, LLM06, agentic tool misuse |

### Appendix — Threats (short)

| Threat | Control |
|--------|---------|
| Indirect prompt injection via memory | Untrusted channel + broker |
| Tool misuse | Allow-list ∩ DNA ∩ RBAC |
| Checkpoint leakage | Redaction + authz |
| Runaway loops | max_handoffs / max_nodes |
| Sandbox escape | separate ns + no prod write |

*End LG-16.*
