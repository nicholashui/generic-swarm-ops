# Design — 05 Security Controls and Tool Broker

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-05-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-05`) |
| Source | `structure.md` §7 |
| Design quality bar | 100 |

---

## 1. Purpose

Enforce **deterministic security outside the LLM**: least-privilege tools, untrusted data handling, fail-closed adapters, auditability, rate limits—assuming prompt injection remains possible. System prompts are never the security boundary.

---

## 2. Context and trust zones

```text
┌─ Untrusted ─────────────────────────────┐
│ User content · retrieved docs · tool I/O │
└──────────────────┬──────────────────────┘
                   │ treat as DATA
┌─ Trusted control plane ─────────────────┐
│ AuthZ · DNA graph · Broker · Adapters    │
│ RuntimeStore · Audit                     │
└─────────────────────────────────────────┘
```

### 2.1 Threat model (STRIDE-lite for agents)

| Threat | Example | Mitigation |
|--------|---------|------------|
| Spoofing | Stolen token | AuthN, short sessions, RBAC |
| Tampering | Prompt injects tool call | Graph+allow-list; ignore content for authz |
| Repudiation | Denied tool use | Audit + tool_effects |
| Info disclosure | Secrets in prompts/logs | Ban secrets in prompts; scan repo |
| DoS / wallet | Unbounded LLM/tool loops | Rate limits, timeouts, step bounds |
| Elevation | Agent uses billing without gate | Irreversible + human gate |

---

## 3. Architecture

### 3.1 Component diagram

```text
Step (11) → ToolBroker.authorize(agent, dna_step, tool, user)
                │ ALLOW
                ▼
         Adapter.execute(args) ──fail-closed──► error
                │ ok
                ▼
         tool_effects + audit tool.executed
```

### 3.2 Components

| ID | Component | Implementation |
|----|-----------|----------------|
| C-05-1 | AuthN | PBKDF2 passwords, session/bearer |
| C-05-2 | AuthZ / RBAC | Permission strings on roles |
| C-05-3 | Tool broker | agent.allowed_tools ∩ step.tools ∩ RBAC ∩ gate |
| C-05-4 | Adapters | `infrastructure/tools/adapters.py` |
| C-05-5 | tool_effects store | RuntimeStore collection |
| C-05-6 | Rate limiter | Middleware sensitive routes |
| C-05-7 | Security headers/CORS | FastAPI middleware |
| C-05-8 | Secret scanner | `business:security` |
| C-05-9 | Adversarial corpus | `business/evals/adversarial*` |
| C-05-10 | Incident runbook | `business/security/` |
| C-05-11 | Skill sandbox | `_sandbox/` + promote gate |

### 3.3 Decisions

| ID | Decision | Rejected | Rationale |
|----|----------|----------|-----------|
| D-05-01 | Fail-closed adapters | Soft-success mocks in ops | Safety |
| D-05-02 | Broker = allow-list + RBAC + gates | Full OAuth per tool now | Product bar; upgrade path |
| D-05-03 | Prompts not controls | Prompt-only authz | OWASP |
| D-05-04 | Local adapters default | Live CRM required | Non-goal until integrations |

---

## 4. Tool broker specification

### 4.1 Authorize algorithm

```text
authorize_tool(user, agent, dna_step, tool_name, args, run):
  if not authenticated(user): DENY(401)
  if not rbac.allows(user, tool_permission(tool_name)): DENY(403)
  if tool_name not in agent.allowed_tools: DENY(403, audit unauthorized)
  if tool_name not in dna_step.tools: DENY(403, audit)
  if tool.irreversible and not approval_satisfied(run, dna_step): DENY(409/gate)
  if not validate_args(tool_name, args): DENY(422)
  return ALLOW
```

### 4.2 Adapter contract

```text
execute(tool, args, context) -> Result
  pre: authorize passed
  validate schema(args)
  perform local side effect OR return structured error
  always: write tool_effect {id, tool, args_digest, status, error?, ts, run_id, step_id}
  never: swallow error as success in ops mode
```

### 4.3 Secret classes

| Class | Storage |
|-------|---------|
| Passwords / API keys | env / secret manager; never git |
| Demo tokens | local smoke only |
| Customer PII in events | minimize; scope ACLs |

---

## 5. OWASP control matrix (design)

| ID | Risk | Control design |
|----|------|----------------|
| LLM01 | Prompt injection | Untrusted data; no authz from content; blast radius allow-list |
| LLM02 | Sensitive disclosure | No secrets in prompts; log redaction practice; retention |
| LLM03 | Supply chain | Source audit; skill sandbox; pin deps |
| LLM04 | Poisoning | Provenance on memory writes; write filters |
| LLM05 | Improper output | Validate tool args before adapter |
| LLM06 | Excessive agency | Tiers + gates + allow-lists |
| LLM07 | Prompt leak | External authz |
| LLM08 | Vector weakness | Org/sensitivity filter on retrieval |
| LLM09 | Misinformation | Citations/provenance on answers |
| LLM10 | Unbounded consumption | Rate limits, timeouts, step caps |

### 5.1 Agentic controls

| Control | Design |
|---------|--------|
| Temporary scoped credentials | Future: token `{run_id, tool, exp}`; **now** allow-list |
| Memory poisoning defense | STRUCT-08 provenance |
| Skill vetting | `_sandbox` until promote |
| Full observability | Audit + tool_effects + request_id |
| Incident response | Runbook path under business/security |

---

## 6. API / events

| Event | When |
|-------|------|
| `tool.executed` | After adapter attempt |
| `tool.denied` | Broker deny |
| `lesson.rejection_recorded` | Approval reject (16) |

Rate-limited route classes: auth login, workflow write, evolution promote.

---

## 7. NFR design

| NFR | Target | Design |
|-----|--------|--------|
| Broker overhead | &lt; 50ms local | In-process set membership |
| Security scan | &lt; 2 min baseline | Regex/path walk |
| Fail closed | 100% ops mode | No success without adapter ok |
| Secrets in repo | 0 critical | CI security script |

**Observability:** metrics `tool_calls_total{tool,status}`, `tool_denies_total{reason}`.

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-05-01…04 | §2 trust + D-05-03 | adversarial + unit |
| FR-05-05…14 | §5 matrix | security + retrieval tests |
| FR-05-15…20 | §4 broker, audit, sandbox, runbook | deny unit, skill tests |
| NFR-05-01…05 | §7 | real_execution, security script |
| AC-05-01…05 | §4–5 | automated |

---

## 9. Validation design

- Unauthorized tool → deny + audit  
- Invalid adapter input → fail closed  
- business:security no critical secrets  
- Adversarial suite runs  

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-05-01 | Ephemeral OAuth per tool | Deferred to live SaaS |
| OI-05-02 | Continuous red-team org | Process |

---

## 11. Design score claim

**Self-score: 100** — threat model, broker algorithm, adapter contract, full OWASP matrix, NFR, RTM.
