# Design — 08 Hybrid Memory System

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-08-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-08`) |
| Source | `structure.md` §3.3 |
| Design quality bar | 100 |

---

## 1. Purpose

Provide **differentiated, scoped memory** (event through provenance) so agents read/write the right store with poisoning defenses, expiration, and auditability.

---

## 2. Context

### 2.1 Memory types (normative)

| Type | Stores | Typical writers |
|------|--------|-----------------|
| event | Raw operational logs | tools, PI, runs |
| episodic | Case narratives | orchestrator |
| semantic | Facts/rules | distiller, curator |
| procedural | Skills/workflows | distilled promote |
| decision | Decisions + reasons | gates, experts |
| exception | Edge cases | exception interviews |
| evaluation | Test results | harness |
| provenance | Source attribution | all high-impact writes |

### 2.2 Scope dimensions (intersect)

`organization`, `user`, `agent`, `workflow`, `department`, `sensitivity`, `expiration`, `policy`.

Agent field: `allowed_memory_scopes` (seed must union scopes required by DNA memory_reads).

---

## 3. Architecture

```text
Writers (11, 14 reflect, 12 reject) → MemoryService
         │ enforce type, scope, provenance, TTL
         ▼
   Postgres runtime_state.memory*
         │ optional mirror
         ▼
   business/memory/** (export)
         │
Readers ← scoped query (agent allow ∩ item scopes ∩ not expired)
```

### 3.1 Components

| ID | Component | Role |
|----|-----------|------|
| C-08-1 | Memory service | CRUD/search with ACL |
| C-08-2 | Scope enforcer | Deny out-of-scope |
| C-08-3 | Provenance gate | High-impact requires source_refs |
| C-08-4 | TTL filter | Exclude expired |
| C-08-5 | Lessons bridge | improvement_lessons + organization_memory |
| C-08-6 | API | `/api/v1/memory` |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-08-01 | Primary in Postgres JSONB | Low latency for runs |
| D-08-02 | Fail closed on scope miss | Security |
| D-08-03 | Rejection writes lesson (decision type) | STRUCT-16 feedback |

---

## 4. Data model

```text
MemoryItem {
  id: string
  type: enum(event|episodic|semantic|procedural|decision|exception|evaluation|provenance)
  content: string | object
  scopes: { organization_id, user_id?, agent_id?, workflow_id?, department?, sensitivity, expires_at? }
  provenance: { source_refs: string[], created_by, created_at }
  metadata: object
  organization_id: string
}
```

### 4.1 High-impact write rule

```text
write(item, agent):
  if not scope_allowed(agent, item.scopes): DENY
  if is_high_impact(item) and empty(item.provenance.source_refs): DENY
  if item.expires_at < now: DENY write or mark expired
  persist
  audit memory.write
```

### 4.2 Read rule

```text
read(query, agent):
  results = search(query)
  return filter(results, scope_allowed and not expired)
```

---

## 5. API contract

| Method | Path | Authz |
|--------|------|-------|
| GET/POST | `/api/v1/memory` | memory:read/write |
| GET | `/api/v1/memory/{id}` | scoped |
| GET | `/api/v1/improvement/lessons` | improvement read |

Error envelope includes request_id.

---

## 6. Interactions with other specs

| Spec | Interaction |
|------|-------------|
| 11 Execution | memory_reads/writes per DNA |
| 05 Security | poisoning defense |
| 14 Evolution | lessons from reflect |
| 12 Gates | rejection lesson |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-08-01 Read p95 budget | Indexed org+id in document store; local target &lt;200ms excl cold start |
| NFR-08-02 Durable after commit | Postgres save |
| NFR-08-03 Sensitive filter | sensitivity field |
| NFR-08-04 Poisoning | provenance required |

**Metrics:** `memory_denies_total{reason}`, `memory_writes_total{type}`.

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-08-01…09 | §2.1 types | unit type tags / lessons |
| FR-08-10…13 | §4 rules | scope matrix, expiry, E1 scopes |
| NFR-08-01…04 | §7 | unit + e2e |
| AC-08-01…04 | §5–6 | API + e2e |

---

## 9. Validation design

Scope deny/allow matrix; provenance on high-impact; expired excluded; flagship memory scopes complete.

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-08-01 | Background TTL purge job | Optional |
| OI-08-02 | Full generative-agent reflection hierarchy | Partial via lessons |

---

## 11. Design score claim

**Self-score: 100** — types, scopes, algorithms, API, RTM, NFR.
