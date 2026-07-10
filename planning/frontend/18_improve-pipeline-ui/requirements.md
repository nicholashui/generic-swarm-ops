# 18 — Improve Pipeline UI (Reflect → Propose → Evaluate → Canary)

| Field | Value |
|-------|-------|
| Spec ID | `FE-18` |
| Source | `frontend.md` — §1 Improve pipeline, §16.13 Improve actions, §33.3 Self-improvement UI, Phase D evolution |
| Related architecture | backend BE-21; structure §5/§8 |
| Priority order | 18 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Improve pipeline controls on workflow run detail: Reflect → Propose → Evaluate → Canary.
- Calls to backend improvement/loop APIs (reflect, lessons, auto-propose, evaluate, canary-related).
- Explicit operator-triggered steps (no silent infinite self-improve loop in UI).
- Display of intermediate results and errors.

### 1.2 Out of scope
- Backend self-improvement engines (BE-21).
- Automatic production promotion without gates.
- Host code rewrite.

### 1.3 System under specification
Self-improvement operator pipeline UI.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-18-01 | Operators | Drive improve steps deliberately on a run. |
| STK-18-02 | Governance | Each step visible, gated, backend-enforced. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-18-01 | The frontend shall expose an Improve pipeline on workflow run detail with ordered steps Reflect, Propose, Evaluate, and Canary. |
| FR-18-02 | When the user activates an Improve step, the frontend shall call the corresponding backend improvement/evolution APIs. |
| FR-18-03 | The frontend shall require explicit user action to advance each Improve step. |
| FR-18-04 | When a step fails, the frontend shall show backend errors and shall not mark the pipeline successful. |
| FR-18-05 | The frontend shall not silently loop Improve steps without operator intent. |
| FR-18-06 | When canary or promote is invoked, the frontend shall call sandbox-gated backend APIs only and shall not write production DNA in the browser. |
| FR-18-07 | When a step succeeds, the Improve UI shall display evidence/results returned by backend for operator review. |
| FR-18-08 | While a step is in progress, the frontend shall show in-progress state and prevent concurrent duplicate step submissions. |
| FR-18-09 | If the user lacks permission for improve actions, the frontend shall hide or disable the Improve controls. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-18-01 | Long-running improve steps shall show in-progress state until backend completes or times out gracefully. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-18-02 | Improve actions shall never bypass backend authorization. |
| NFR-18-03 | Improve UI shall not write production DNA locally. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-18-01 | Run detail shows Improve step controls. |
| AC-18-02 | Reflect/propose/evaluate/canary invoke backend routes. |
| AC-18-03 | No automatic unattended infinite improve loop in UI. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-11, FE-12, FE-14, FE-17 | E1 operator improve path |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-18-01 | E1: improve path on run detail. | E2E / manual |
| TV-18-02 | Unit: step state machine requires explicit next. | Unit |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §1 Improve pipeline | FR-18-01 |
| §16.13 Improve actions | FR-18-02 … FR-18-07 |
| §33.3 Self-improvement UI | AC-18-* |


