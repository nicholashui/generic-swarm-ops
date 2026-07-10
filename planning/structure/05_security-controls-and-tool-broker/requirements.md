# 05 — Security Controls and Tool Broker

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-05` |
| Source | `structure.md` §7 |
| Priority order | 05 |
| Status | Specification |
| Owner | Security Red-Team + Platform |

---

## 1. Scope

### 1.1 In scope
- Deterministic security outside the LLM.
- OWASP LLM Top 10 (2025) control mapping.
- Agentic controls: tool permission broker, memory-poisoning defense, skill vetting, observability, incident response.
- Blast-radius limits under prompt-injection assumptions.

### 1.2 Out of scope
- Full continuous red-team program staffing.
- Commercial DLP vendor integration (unless later chosen).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-05-01 | CISO / security | Prompt injection assumed possible; blast radius controlled. |
| STK-05-02 | Operators | Tools only run when allowed; failures are auditable. |
| STK-05-03 | Developers | Clear allow-lists and fail-closed adapters. |
| STK-05-04 | Incident responders | Runbook and audit trail for GenAI incidents. |

---

## 3. Functional Requirements (EARS)

### 3.1 Foundational security posture

| ID | Statement (EARS) |
|----|------------------|
| FR-05-01 | The system shall enforce security controls deterministically outside the language model. |
| FR-05-02 | The system shall not treat system prompts as the sole security control. |
| FR-05-03 | When content is retrieved or supplied by users, the system shall treat that content as untrusted data. |
| FR-05-04 | If prompt injection is detected or suspected, then the system shall not expand tool privileges or bypass gates. |

### 3.2 OWASP-aligned controls

| ID | Statement (EARS) |
|----|------------------|
| FR-05-05 | When handling retrieved documents, the system shall separate instructional policy from untrusted document text (LLM01). |
| FR-05-06 | The system shall prevent secrets from being placed in prompts or logs where retention policy forbids (LLM02). |
| FR-05-07 | When integrating models, tools, or adapters, the system shall record registry/provenance metadata (LLM03). |
| FR-05-08 | When writing high-impact memory, the system shall require provenance and apply write filters (LLM04). |
| FR-05-09 | When model output would trigger tool execution, the system shall validate and allow-list the action before execution (LLM05). |
| FR-05-10 | The system shall restrict tool access by agent and risk tier to prevent excessive agency (LLM06). |
| FR-05-11 | The system shall enforce authorization externally so that leaked role text in prompts cannot grant access (LLM07). |
| FR-05-12 | Where vector stores are multi-tenant, the system shall isolate tenants at query time (LLM08). |
| FR-05-13 | When returning knowledge answers, the system shall include source citations for grounding (LLM09). |
| FR-05-14 | The system shall enforce rate limits, timeouts, and/or budget caps on sensitive or unbounded operations (LLM10). |

### 3.3 Agentic controls

| ID | Statement (EARS) |
|----|------------------|
| FR-05-15 | When an agent requests a tool, the tool permission broker shall grant only scoped, task-appropriate permissions. |
| FR-05-16 | If a tool is not on the agent/workflow allow-list, then the system shall deny the tool call and record the attempt. |
| FR-05-17 | When a high-impact memory write is requested, the system shall require provenance and, where policy says so, human review. |
| FR-05-18 | When third-party skills or plugins are introduced, the system shall require vetting and pinning before production use. |
| FR-05-19 | The system shall emit a unified audit trail across model calls, tool calls, and agent workflow steps. |
| FR-05-20 | The system shall provide an AI incident-response runbook path for containment, investigation, and recovery. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-05-01 | Allow-list checks for tool calls shall add less than 50 ms overhead per call in local environments excluding adapter I/O. |
| NFR-05-02 | Security scans of business artifacts shall complete within 2 minutes for the baseline tree. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-05-03 | Adapters shall fail closed on invalid input or unauthorized use. |
| NFR-05-04 | Authentication secrets shall not be committed to the repository. |
| NFR-05-05 | Default tool permissions shall follow least privilege and avoid wildcard scopes. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-05-01 | Unauthorized tool call is denied and audited. |
| AC-05-02 | `npm run business:security` runs without critical secret findings. |
| AC-05-03 | Prompt-injection adversarial fixtures exist under evals/security coverage. |
| AC-05-04 | Tool permission register or allow-list configuration is documented. |
| AC-05-05 | Incident-response artifact or runbook path exists under `business/security/`. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01, STRUCT-04 | STRUCT-08, STRUCT-09, STRUCT-11, STRUCT-12, STRUCT-14 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-05-01 | Unit: deny non-allow-listed tool. | Automated |
| TV-05-02 | Adversarial corpus: injection attempts do not elevate privileges. | Automated |
| TV-05-03 | Secret scan + security script. | Automated |
| TV-05-04 | Red-team checklist review (manual periodic). | Review |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §7 intro / blast radius | FR-05-01 … FR-05-04 |
| §7.1 Control matrix | FR-05-05 … FR-05-14 |
| §7.2 Agentic controls | FR-05-15 … FR-05-20 |
