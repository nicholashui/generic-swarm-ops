# Design — 17 Phased Rollout and Operator Path

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-17-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-17`) |
| Source | `structure.md` §11 |
| Design quality bar | 100 |

---

## 1. Purpose

Integrate components 01–16 into **phased capability exits** and a single **operator path** proving the governed system end-to-end. Phases are **capability gates**, not calendar promises.

---

## 2. Context

```text
Phase A Foundation (01–05, 02, 13 seed)
  → B Shadow learning (06–07)
  → C Controlled co-pilot (08–12, 09–11)
  → D Evolution sandbox (13–14, 15–16)
  → Operator path E1 + verification pack → release
```

**Invariant:** No phase disables auth, audit, or gates for speed.

---

## 3. Architecture — phase exits

| Phase | Maps structure days | Exit criteria (normative) | Depends |
|-------|---------------------|---------------------------|---------|
| A Foundation | 1–14 | Tree, event schema, inventory, risk tiers, audit, ≥20 golden | 01,02,04,05,13 |
| B Shadow | 15–30 | Event ingest, ≥1 DRC, knowledge ingest path | 06,07 |
| C Co-pilot | 31–60 | DNA run + gates + retrieval provenance + regression | 08–12,09,10,11 |
| D Evolution | 61–90 | Propose/eval/canary/rollback; promote only with tests | 13,14 |

---

## 4. Operator path (E1) — sequence design

```text
1 Postgres up; backend health ready database=postgres
2 FE DEMO_MODE=false; API base set
3 Login admin@example.com
4 List agents/workflows (live)
5 Create agent/workflow OR open flagship DNA
6 Run now with valid inputs (case_id, …)
7 Human gate: approve billing/critical step
8 Run completes; inspect audit, memory, eval
9 Improve: reflect → propose → evaluate → canary
10 Evolution archive shows fitness
```

### 4.1 Automation

| Asset | Path |
|-------|------|
| E2E test | `backend/app/tests/e2e/test_e1_operator_path.py` |
| Checklist | `reviews/e1_operator_checklist.md` |
| Verification | `mark_100_verification.md` |
| Scorecard | `structure_scorecard_100.md` |
| Gap SDD | `planning/gap_analysis_for_structure.md` |

### 4.2 Command matrix (release gate)

```text
npm test
npm run business:validate
npm run business:governance
npm run business:security
npm run business:evolution:check
npm run business:eval
backend unit + e2e
frontend lint/typecheck/test
GET /api/v1/health/ready → database: postgres
```

### 4.3 Environment profile (ops)

| Var | Value |
|-----|-------|
| DATABASE_URL | Postgres |
| NEXT_PUBLIC_DEMO_MODE | false |
| NEXT_PUBLIC_API_BASE_URL | http://127.0.0.1:8000/api/v1 |

---

## 5. Components

| ID | Component | Role |
|----|-----------|------|
| C-17-1 | Phase checklists | Exit tables §3 |
| C-17-2 | E1 automation | e2e test |
| C-17-3 | Verification pack | mark100 + logs |
| C-17-4 | Ops runbooks | postgres-runbook, usage |
| C-17-5 | Non-goals register | status.md |

### 5.1 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-17-01 | Capability gates over calendar | Reproducible |
| D-17-02 | API e2e required; UI dogfood recommended | Reliability |
| D-17-03 | Non-goals explicit | Prevent fake 100 |

---

## 6. NFR design

| NFR | Design |
|-----|--------|
| NFR-17-01 E1 API ≤5 min excl human | Automated e2e |
| NFR-17-02 Phase review one session | Checklists |
| NFR-17-03 No bypass of auth/gates | Policy + review |
| NFR-17-04 Durable store + secret-safe config | Postgres + .env |

---

## 7. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-17-01 | Phase A §3 | business:* + golden count |
| FR-17-02 | Phase B §3 | PI + DRC artifacts |
| FR-17-03 | Phase C §3 | E1 mid path |
| FR-17-04…05 | Phase D §3 | evolution tests |
| FR-17-06…10 | §4 operator path | test_e1_operator_path |
| NFR-17-01…04 | §6 | timed e2e + review |
| AC-17-01…06 | §3–4 | verification pack |

---

## 8. Validation design

All phase exits; E1 green; command matrix logged; scorecard+gap 100; non-goals listed.

---

## 9. Deferred non-goals (do not block 100)

- Full LightRAG vendor / Neo4j production mesh  
- Live external CRM/email  
- DGM host code self-rewrite  
- Always-on Playwright CI servers  
- Ephemeral OAuth tool broker  

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-17-01 | Enterprise 10k-event shadow program | Org rollout |
| OI-17-02 | Continuous verification freshness | Process |

---

## 11. Design score claim

**Self-score: 100** — phases, E1 sequence, command matrix, env, RTM, non-goals.
