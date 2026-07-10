# 08 — Dashboard Page

| Field | Value |
|-------|-------|
| Spec ID | `FE-08` |
| Source | `frontend.md` — §16.4 Dashboard Page, Phase 6 Dashboard, §12.1 /app |
| Related architecture | structure.md operator path entry |
| Priority order | 08 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Main dashboard at `/app`.
- Summary cards / attention items (runs needing approval, failed runs, recent activity) per frontend.md §16.4.
- Entry links into domain sections.
- Health-aware empty/error when backend unavailable.

### 1.2 Out of scope
- Full domain CRUD (later specs).
- Backend metrics aggregation design.

### 1.3 System under specification
Operator dashboard home surface.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-08-01 | Operators | Immediate view of what needs attention. |
| STK-08-02 | New users | Clear entry points into agents, workflows, approvals. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-08-01 | The frontend shall provide a dashboard page at `/app` for authenticated users. |
| FR-08-02 | When dashboard data is available, the dashboard shall surface operational attention items including pending approvals and recent or failed workflow runs. |
| FR-08-03 | The dashboard shall provide navigation affordances into primary domains (agents, workflows, approvals, knowledge, evaluations). |
| FR-08-04 | When dashboard data is loading, the frontend shall show loading states (skeletons or equivalent). |
| FR-08-05 | When dashboard data is empty (no agents/workflows), the frontend shall show empty states with an onboarding checklist guidance. |
| FR-08-06 | When dashboard API calls fail, the frontend shall show error states with retry and request_id when available. |
| FR-08-07 | The dashboard shall include a header/summary region and a metric card grid for operational counters when data exists (e.g., active agents, workflows running, pending approvals, failed runs). |
| FR-08-08 | When the user selects a quick action (create agent, create workflow, review approvals, or equivalent), the frontend shall navigate to the corresponding domain route. |
| FR-08-09 | If a dashboard section’s API fails while others succeed, the frontend shall isolate the failure to that section without blanking the entire shell. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-08-01 | Dashboard shall prioritize above-the-fold attention metrics over secondary widgets. |
| NFR-08-03 | Dashboard initial content shall remain interactive within the shell without full-app blocking spinners. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-08-02 | Dashboard shall only show data returned for the authenticated org/user scope. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-08-01 | Authenticated user lands on dashboard after login. |
| AC-08-02 | Loading/empty/error states are implemented. |
| AC-08-03 | Links from dashboard reach domain routes. |
| AC-08-04 | Metric/attention regions match frontend.md §16.4 intent when data is present. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-04, FE-06, FE-07 | Operator entry to domain pages |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-08-01 | Manual E1: post-login dashboard visible. | Manual |
| TV-08-02 | Unit: empty state when API returns empty lists. | Unit |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §16.4 Dashboard | FR-08-01 … FR-08-06 |
| Phase 6 | AC-08-* |


