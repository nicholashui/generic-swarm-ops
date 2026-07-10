# 19 — Accessibility, Loading, Empty, and Error States

| Field | Value |
|-------|-------|
| Spec ID | `FE-19` |
| Source | `frontend.md` — §22 Loading/Empty/Error States, §23 Accessibility Requirements, §29 product ideas (UX quality) |
| Related architecture | WCAG 2.2 AA target; structure human–AI interaction |
| Priority order | 19 |
| Status | Specification |
| Owner | Frontend platform |

---

## 1. Scope

### 1.1 In scope
- Cross-cutting loading, empty, and error state patterns (§22).
- Accessibility requirements (§23): keyboard, focus, labels, contrast targets (WCAG 2.2 AA intent).
- Consistent error presentation including request_id.
- Preferential use of design-system state components (FE-03).

### 1.2 Out of scope
- Full legal compliance certification.
- Domain-specific content for every empty state narrative beyond patterns.

### 1.3 System under specification
UX quality system for states and accessibility.


---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|---|---|---|
| STK-19-01 | All users | Understand loading, empty, and failure conditions. |
| STK-19-02 | Users of assistive tech | Keyboard and screen-reader operable console. |
| STK-19-03 | Support | Errors include correlatable request IDs. |


---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|---|---|
| FR-19-01 | Every major data page shall implement loading, empty, and error states. |
| FR-19-02 | Error states shall show human-readable messages and request_id when the API provides one. |
| FR-19-03 | Interactive controls shall be keyboard operable for primary flows. |
| FR-19-04 | Form inputs shall have accessible labels. |
| FR-19-05 | Focus shall be managed for modals and drawers (trap/restore as appropriate). |
| FR-19-06 | Status information shall not rely on color alone. |
| FR-19-07 | Empty states shall include guidance on next actions when applicable. |
| FR-19-08 | The frontend shall target WCAG 2.2 Level AA practices for core operator flows. |


---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|---|---|
| NFR-19-01 | Loading skeletons shall avoid layout thrash where practical. |

### 4.2 Security
| ID | Statement |
|---|---|
| NFR-19-02 | Error messages shall not dump stack traces or secrets to end users in production builds. |


---

## 5. Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-19-01 | Representative pages (dashboard, runs, approvals) show all three states. |
| AC-19-02 | Primary forms have labels; modals keyboard-dismissible. |
| AC-19-03 | Production errors omit secrets/stack traces. |


---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| FE-03, FE-04 | All pages (cross-cutting UX quality) |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|---|---|---|
| TV-19-01 | Manual keyboard pass on shell + one form. | Manual / a11y |
| TV-19-02 | Unit: ErrorState renders request_id. | Unit |
| TV-19-03 | Optional axe scan on key routes. | Automated |


---

## 8. Traceability

| frontend.md | This spec |
|---|---|
| §22 Loading/Empty/Error | FR-19-01 … FR-19-02, FR-19-07 |
| §23 Accessibility | FR-19-03 … FR-19-06, FR-19-08 |
| §25/§24 message safety | NFR-19-02 |


