# 14 — Evolution Sandbox Engine

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-14` |
| Source | `structure.md` §5 |
| Priority order | 14 |
| Status | Specification |
| Owner | Evolution Manager |

---

## 1. Scope

### 1.1 In scope
- Non-negotiable rule: never mutate production DNA directly.
- Fitness function dimensions and offline scoring.
- Pipeline: observe → detect → generate → offline test → security/adversarial → compliance → historical replay → human review → canary → monitor → promote/rollback → store lessons.
- Promotion rule checklist.
- Reflective natural-language improvement loops only inside sandbox gates.

### 1.2 Out of scope
- Host application self-rewriting (DGM-style code mutation of the platform).
- Unattended production promotion.
- Full multi-objective Pareto UI (fitness scalars first; Pareto optional later).

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-14-01 | Risk / compliance | Production DNA never silently rewritten. |
| STK-14-02 | Ops | Canary and rollback available. |
| STK-14-03 | Product | Measurable improvement via fitness, not vibes. |
| STK-14-04 | Engineers | Clear proposal → eval → canary API/UI path. |

---

## 3. Functional Requirements (EARS)

### 3.1 Non-negotiable rule

| ID | Statement (EARS) |
|----|------------------|
| FR-14-01 | The evolution manager shall never mutate production workflow DNA directly. |
| FR-14-02 | When evolution generates a change, the system shall create a sandbox-only variant proposal. |
| FR-14-03 | If a client requests direct production mutation or auto_promote without policy, then the system shall reject the request. |

### 3.2 Fitness

| ID | Statement (EARS) |
|----|------------------|
| FR-14-04 | When scoring a variant, the system shall compute fitness using quality, safety, compliance, efficiency, and human satisfaction rewards minus risk, latency, and cost penalties. |
| FR-14-05 | Where objectives conflict, the system shall support multi-metric comparison rather than unconstrained single-metric cheating. |

### 3.3 Pipeline

| ID | Statement (EARS) |
|----|------------------|
| FR-14-06 | When opportunities or failures are detected, the system shall allow generation of variants (prompt, workflow, tool-use, role, or expert-pattern crossover). |
| FR-14-07 | When a variant is proposed, the system shall test it offline against golden tasks. |
| FR-14-08 | When a variant is proposed, the system shall run security and adversarial checks before canary eligibility. |
| FR-14-09 | When a variant is proposed, the system shall run compliance checks before canary eligibility. |
| FR-14-10 | When historical cases exist, the system shall support replay simulation prior to canary. |
| FR-14-11 | When risk tier requires it, the system shall require human review before canary or promote. |
| FR-14-12 | When canary is approved, the system shall deploy the variant only to a limited scope. |
| FR-14-13 | When canary metrics fail thresholds, the system shall support rollback to the previous active version. |
| FR-14-14 | When a variant is promoted or rejected, the system shall store lessons in evolution memory. |

### 3.4 Promotion rule

| ID | Statement (EARS) |
|----|------------------|
| FR-14-15 | If a variant does not improve target metrics, then the system shall not promote it. |
| FR-14-16 | If a variant regresses safety or compliance, then the system shall not promote it. |
| FR-14-17 | If regression or adversarial tests fail, then the system shall not promote it. |
| FR-14-18 | If rollback plan is missing, then the system shall not promote it. |
| FR-14-19 | If audit logs are incomplete for the promotion decision, then the system shall not promote it. |
| FR-14-20 | If risk tier requires human sign-off and sign-off is missing, then the system shall not promote it. |

### 3.5 Reflective optimization

| ID | Statement (EARS) |
|----|------------------|
| FR-14-21 | Where reflective natural-language diagnosis is used, the system shall confine reflection-driven changes to sandbox proposals. |
| FR-14-22 | When runs terminate, the system may extract lessons and optionally auto-propose sandbox variants without applying them to production. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-14-01 | Offline corpus evaluation for a single variant against baseline golden set shall complete within 15 minutes locally for the reference corpus size. |
| NFR-14-02 | Population archive listing shall return within 2 seconds for baseline variant counts. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-14-03 | Sandbox variants shall not receive production credentials beyond those allowed for eval fixtures. |
| NFR-14-04 | Evolution artifacts shall remain auditable under `business/evolution/` and runtime stores. |
| NFR-14-05 | Skill/prompt evolution shall land in sandbox paths until explicit promote. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-14-01 | Direct production DNA mutation API/path is blocked. |
| AC-14-02 | Propose → evaluate → canary → rollback path exists and is tested. |
| AC-14-03 | Fitness metrics recorded for evaluated variants. |
| AC-14-04 | Promotion requires checklist conditions (tests + rollback + audit). |
| AC-14-05 | Lessons stored after terminal runs / evolution decisions. |
| AC-14-06 | Operator UI or API exposes archive and improve pipeline. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01, STRUCT-06, STRUCT-10, STRUCT-11, STRUCT-13 | STRUCT-16 Improve UI, STRUCT-17 rollout phase 61–90 |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-14-01 | Unit: auto_promote blocked. | Automated |
| TV-14-02 | Integration: corpus eval + canary + rollback. | Automated |
| TV-14-03 | E2E: reflect → propose → evaluate → canary. | Automated |
| TV-14-04 | `npm run business:evolution:check`. | Automated |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §5.1 Non-negotiable rule | FR-14-01 … FR-14-03 |
| §5.2 Fitness | FR-14-04 … FR-14-05 |
| §5.3 Pipeline | FR-14-06 … FR-14-14, FR-14-21 … FR-14-22 |
| §5.4 Promotion rule | FR-14-15 … FR-14-20 |
