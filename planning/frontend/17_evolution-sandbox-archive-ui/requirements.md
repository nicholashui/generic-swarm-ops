# 17 — Evolution Sandbox Archive UI

| Field | Value |
|-------|-------|
| Spec ID | `FE-17` |
| Source | `frontend.md` — §16.13a Evolution Archive Page, §4.1 Evolution section, §33.3 Evolution UI |
| Related architecture | backend BE-20; structure §5 |
| Priority order | 17 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Evolution archive page at `/app/evolution`.
- Display of sandbox variants, fitness ranking, archive metadata from backend.
- Actions that call backend evolution APIs only (evaluate, promote, rollback as exposed).
- Explicit sandbox-only messaging; no production DNA rewrite UI.

### 1.2 Out of scope
- Evolution engine implementation (BE-20).
- DGM-style host self-rewrite UI (§33.5).
- Silent production activation from FE.

### 1.3 System under specification
Evolution sandbox archive operator UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-17-01 | Evolution operators | Browse sandbox population and fitness. |
| STK-17-02 | Governance | No path to silent production DNA mutation from UI. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-17-01 | The frontend shall provide an evolution archive page under `/app/evolution`. |
| FR-17-02 | The page shall list sandbox variants and fitness/ranking data returned by backend evolution APIs. |
| FR-17-03 | When evaluate/promote/rollback actions are available, the frontend shall call backend evolution endpoints only. |
| FR-17-04 | The frontend shall not implement client-side production DNA mutation or host application self-rewrite. |
| FR-17-05 | UI copy shall communicate sandbox / gated promotion semantics when promoting variants. |
| FR-17-06 | Permission-aware UI shall gate evolution admin actions. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-17-01 | Archive lists shall paginate when populations grow. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-17-02 | Evolution mutations shall require authenticated, authorized backend calls. |
| NFR-17-03 | If a UI path would skip backend sandbox validation, it shall be rejected in design. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-17-01 | `/app/evolution` renders archive from backend or empty state. |
| AC-17-02 | No client DNA rewrite module exists. |
| AC-17-03 | Promote/rollback only via backend APIs. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07 | FE-18 canary/promote views |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-17-01 | Manual: open evolution archive. | Manual |
| TV-17-02 | Review: grep FE for production DNA write — none. | Review |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.13a Evolution Archive | FR-17-01 … FR-17-03 |
| §4.2 / §33.3 Evolution UI | FR-17-04 … FR-17-05 |
| structure.md §5 | FR-17-04 |


