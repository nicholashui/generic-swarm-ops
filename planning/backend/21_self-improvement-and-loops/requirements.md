# 21 — Self-Improvement and Loops

| Field | Value |
|-------|-------|
| Spec ID | `BE-21` |
| Source | `backend.md` — §7.16, §11.16 Improvement / Loop Endpoints |
| Related architecture | structure.md self-improvement / GEPA-style |
| Priority order | 21 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Reflect on runs, lesson library, auto-propose sandbox variants.
- Optional LLM critic feature flag.
- Skill sandbox write under _sandbox with explicit promote.
- Loop DNA runner start/status.
- Auto-reflect configuration flag.

### 1.2 Out of scope
- Unsupervised auto-promote to production.
- Host code rewriting loops.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-21-01 | Operators | Improve pipeline after runs. |
| STK-21-02 | Researchers | Lessons and reflective loops. |
| STK-21-03 | Risk | All proposals remain sandboxed. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-21-01 | The backend shall support reflecting on a completed or failed run to extract lessons. |
| FR-21-02 | The backend shall maintain a lesson library listable and scorable by utility. |
| FR-21-03 | The backend shall support auto-propose of sandbox DNA variants from lessons without mutating production DNA directly. |
| FR-21-04 | Where GENERIC_SWARM_LLM_CRITIC_ENABLED (or equivalent) is enabled and configured, the backend shall allow an optional LLM critic path. |
| FR-21-05 | The backend shall support skill sandbox writes under a _sandbox area with explicit promote only. |
| FR-21-06 | The backend shall support loop DNA runner start and status endpoints. |
| FR-21-07 | When GENERIC_SWARM_AUTO_REFLECT is enabled, the backend shall auto-reflect on terminal run statuses. |
| FR-21-08 | If a self-improvement action would mutate production DNA directly, then the backend shall reject it and require sandbox proposal instead. |
| FR-21-09 | Self-improvement actions shall be authorized and produce audit/lesson provenance. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-21-01 | Reflect on a single run shall complete within a few seconds local without optional LLM critic. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-21-02 | LLM critic shall not receive secrets from env dumps. |
| NFR-21-03 | Skill promote shall require privileged authorization. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-21-01 | POST reflect creates lessons for a run. |
| AC-21-02 | Auto-propose creates sandbox variant only. |
| AC-21-03 | Skill sandbox write not visible as promoted until promote. |
| AC-21-04 | Loop runner start returns run/loop id. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-11, BE-20, BE-17 | FE Improve pipeline, E1 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-21-01 | test_full_improvement_backlog or equivalent. | Automated |
| TV-21-02 | Reflect → propose chain. | Automated |
| TV-21-03 | E1 improve segment. | E2E |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.16 Self-Improvement | FR-21-01 … FR-21-07 |
| backend.md §11.16 | FR-21-01 … FR-21-06 |
| backend.md §24.3 Self-improvement | FR-21-08 |
