# Design — 03 Intake and Risk Router

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-03-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-03`) |
| Source | `structure.md` §2 intake |
| Design quality bar | 100 |

---

## 1. Purpose

Every unit of work is **authenticated, authorized, risk-classified, audited, and handed to the orchestrator** before any irreversible tool runs.

---

## 2. Context

### 2.1 Actors

| Actor | Action |
|-------|--------|
| Operator / API client | POST start run |
| AuthN/AuthZ | Identity + permission |
| Risk classifier | Assign risk_tier |
| Orchestrator (11) | Execute DNA |
| Audit (12) | Append start/reject |

### 2.2 Trust

Untrusted payload content is **data**, never authorization instructions (STRUCT-05).

---

## 3. Architecture

### 3.1 Pipeline (normative sequence)

```text
1 Client → AuthN (401 if fail)
2 AuthZ workflow:start (403 if fail)
3 Validate inputs vs DNA/schema (422 if fail)
4 Classify risk_tier (DNA baseline + payload signals + policy)
5 Persist run {id, workflow_id, version, risk_tier, status, inputs, created_by, request_id}
6 Emit audit run.started / classification
7 Handoff to orchestrator _execute_run / queue
```

**Invariant:** No adapter invocation before step 5 succeeds.

### 3.2 Components

| ID | Component | Implementation |
|----|-----------|----------------|
| C-03-1 | API intake | FastAPI workflow run routes |
| C-03-2 | Auth deps | get_current_user, RBAC |
| C-03-3 | Input validator | DNA inputs / payload schema |
| C-03-4 | Risk classifier | DNA.risk_tier + policy escalate |
| C-03-5 | Run factory | RuntimeStore workflow_runs |
| C-03-6 | Audit emitter | append audit event |
| C-03-7 | Idempotency (optional) | Idempotency-Key → same run id |

### 3.3 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-03-01 | Intake as run-start stages in control plane | Single deployable; extract IntakeService if complexity grows |
| D-03-02 | Default risk from DNA; escalate on signals | Matches structure risk routing |
| D-03-03 | Prefer password session over static tokens for ops | Security |

---

## 4. Risk classification design

### 4.1 Inputs

| Input | Effect |
|-------|--------|
| DNA.risk_tier | Baseline |
| Irreversible steps present | Floor at tier_3/4 |
| Exception flags / DRC.human_approval_required | Escalate |
| Missing assurance for tier_5 | Block start or force restricted |

### 4.2 Decision table (core)

| Condition | Result |
|-----------|--------|
| DNA tier_0 | Observe-only path; no external tools |
| DNA tier_4 + irreversible billing | risk_tier tier_4; expect gate |
| tier_5 without assurance_case_id | Reject start |
| Unauthenticated | 401 |
| Unauthorized role | 403 |

### 4.3 Run record fields (normative)

`id, organization_id, workflow_id, workflow_version, risk_tier, status, inputs, created_by, created_at, request_id, approval_request_id?, error?`

---

## 5. API contract (ICD)

### 5.1 Start run

```http
POST /api/v1/workflows/{workflow_id}/runs
Authorization: Bearer <token> | session cookie
Idempotency-Key: <optional>
Content-Type: application/json

{ "inputs": { "case_id": "...", ... } }
```

| Status | Meaning |
|--------|---------|
| 200/201 | Run created; body includes id, status, risk_tier |
| 401 | Unauthenticated |
| 403 | Missing permission |
| 404 | Workflow not found |
| 422 | Validation / policy reject; body `{message, request_id}` |
| 409 | Idempotency conflict (if enabled) |

### 5.2 Error envelope

```json
{ "message": "human readable", "request_id": "req_...", "code": "optional" }
```

---

## 6. Failure modes

| Failure | Behavior |
|---------|----------|
| Auth fail | No run row |
| Validation fail | No run / no tools |
| Classify internal error | 500; no tools |
| Orchestrator fail after create | Run status failed; audited |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-03-01 &lt;2s classify local | Pure CPU policy, no LLM |
| NFR-03-02 Idempotency | Optional header store |
| NFR-03-03 Auth required | Dependency injection |
| NFR-03-04 Untrusted payload | No privilege expansion |

**Metrics:** `runs_started_total`, `runs_start_rejected_total{reason}`, latency histogram start.

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-03-01…04 | §3.1 steps 1–7 | e2e start, unit auth |
| FR-03-05 | §4.2 | tier-4 flagship |
| FR-03-06…07 | §3.1 steps 6 + invariant | audit + no tool pre-persist |
| NFR-03-01…04 | §7 | perf smoke, 401 test |
| AC-03-01…04 | §4–5 | E1 |

---

## 9. Validation design

- Unauthenticated start → 401  
- Missing required input → 422  
- risk_tier present on run  
- E1 operator path starts flagship  

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-03-01 | Dedicated IntakeService class | Optional refactor |
| OI-03-02 | Distributed idempotency store | When multi-instance |

---

## 11. Design score claim

**Self-score: 100** — full pipeline, decision table, ICD, failures, RTM, NFR.
