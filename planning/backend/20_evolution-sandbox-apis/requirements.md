# 20 — Evolution Sandbox APIs

| Field | Value |
|-------|-------|
| Spec ID | `BE-20` |
| Source | `backend.md` — §7.15, §11.15, §24.3 evolution as-built |
| Related architecture | structure.md §5 evolution sandbox |
| Priority order | 20 |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
- Evolution variants list/propose/evaluate/promote/rollback.
- Fitness/population archive.
- sandbox_only enforcement; no host code rewrite.
- Canary then promote gates.

### 1.2 Out of scope
- DGM-style host application self-rewrite (non-goal).
- Silent production DNA replacement.

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-20-01 | Evolution manager role | Propose and test safely. |
| STK-20-02 | Risk owners | No direct prod mutation. |
| STK-20-03 | Operators | Canary and rollback controls. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-20-01 | The backend shall expose evolution controls that enforce sandbox-only mutation of production Workflow DNA. |
| FR-20-02 | The backend shall support listing and proposing evolution variants marked sandbox_only. |
| FR-20-03 | When a variant is evaluated, the backend shall run corpus/fitness evaluation and persist scores. |
| FR-20-04 | The backend shall support canary promote to limited scope and full promote only after gates. |
| FR-20-05 | The backend shall support rollback of canary/promoted changes. |
| FR-20-06 | The backend shall expose a fitness/population archive endpoint. |
| FR-20-07 | The evolution manager path shall never rewrite host application source code. |
| FR-20-08 | The evolution manager path shall never silently replace production DNA without versioned promote gates. |
| FR-20-09 | If safety or evaluation gates fail, then the backend shall refuse promotion. |
| FR-20-10 | Evolution actions shall be authorized and audited. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-20-01 | Propose variant API returns quickly; heavy eval may be async but must be trackable. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-20-02 | Only authorized roles may promote variants. |
| NFR-20-03 | Sandbox variants shall not execute as production DNA until promoted. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-20-01 | Propose creates sandbox_only variant. |
| AC-20-02 | Evaluate persists fitness result. |
| AC-20-03 | Promote without eval gates fails. |
| AC-20-04 | Rollback restores prior version path. |
| AC-20-05 | Archive lists ranked variants. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| BE-10, BE-17, BE-22 | BE-21, FE /app/evolution |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-20-01 | Evolution API unit/integration suite. | Automated |
| TV-20-02 | Negative: direct prod mutation attempt rejected. | Automated |
| TV-20-03 | Canary/rollback path test. | Automated |

---

## 8. Traceability

| backend.md / structure.md | This spec |
|---|---|
| backend.md §7.15 Evolution | FR-20-01 … FR-20-08 |
| backend.md §11.15 | FR-20-02 … FR-20-06 |
| backend.md §24.3 / non-goals | FR-20-07, scope_out |
