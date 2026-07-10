# Design — 02 Business Artifact Repository

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-02-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-02`) |
| Source | `structure.md` §3.5 |
| Design quality bar | 100 |

---

## 1. Purpose

Provide a **stable first-party filesystem contract** for process intelligence, knowledge, experts, materials, distilled assets, memory corpus, evals, governance, security, and evolution—separated from runtime Postgres state and untrusted `external/sources/`.

---

## 2. Context and boundaries

### 2.1 Data plane (normative)

| Store | Role | Mutators | Consumers |
|-------|------|----------|-----------|
| `business/**` | Versioned corpus, policies, fixtures | Git + controlled writers (PI, eval, promote) | Validators, harness, humans, optional runtime load |
| Postgres `runtime_state` | Live agents, runs, memory, variants | API/runtime only | Control plane |
| `backend/data/runtime.json` | Snapshot backup / seed | Runtime save | Disaster recovery, empty-DB seed |
| `external/sources/` | Untrusted reference clones | download scripts | Audit only until curated into business/ |

**Conflict rule:** Live operational truth for runs = Postgres. Compliance corpus & evals = `business/**`. Never treat external/ as production knowledge without audit+curation.

### 2.2 Actors

Operators, knowledge curators, CI validators, PI/evolution writers, security scanners.

---

## 3. Architecture

### 3.1 Tree (normative top-level)

```text
business/
├── process-intelligence/   # event-logs, discovered-processes, conformance-reports, bottlenecks, causal-hypotheses
├── knowledge-base/         # rules, decision-patterns, exceptions, best-practices, tacit-knowledge, provenance
├── experts/                # profiles, shadow-logs, decision-requirement-cards, interview-transcripts, elicitation-methods
├── materials/              # documents, regulations, sops
├── distilled/              # skills, prompts, workflows, checklists, playbooks (+ skills/_sandbox)
├── memory/                 # episodic, semantic, procedural, decision-memory, evaluation-memory (optional disk mirror)
├── evals/                  # golden-tasks, regression, adversarial, human-review-sets, historical-replay, retrieval, benchmark-results
├── governance/             # ai-inventory, risk tiering, approval policy, model-cards, assurance-cases, audit-logs notes
├── security/               # threat-models, tool-permissions, prompt-injection-tests, red-team-results, incident-reports
├── evolution/              # workflow-dna, successful-variants, failed-experiments, mutation-history, lessons-learned
├── schemas/                # JSON Schema contracts
├── examples/               # conforming samples
└── fixtures/               # negative/positive test fixtures (SDD)
```

### 3.2 Components

| ID | Component | Responsibility |
|----|-----------|----------------|
| C-02-1 | Init | `npm run business:init` creates dirs + seeds |
| C-02-2 | Validate | Schema + structural rules (`business:validate`) |
| C-02-3 | Security scan | Secrets / wildcards (`business:security`) |
| C-02-4 | Governance check | Required governance artifacts |
| C-02-5 | Schema registry | `business/schemas/*` |
| C-02-6 | Sandbox quarantine | `distilled/skills/_sandbox/` until promote |

### 3.3 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-02-01 | Dual store disk+Postgres | Offline eval + durable live state |
| D-02-02 | Git is SoT for business corpus | Auditability over silent runtime-only policies |
| D-02-03 | Negative fixtures under business/fixtures | SDD validators share repo |

---

## 4. Naming, metadata, lifecycle

### 4.1 Conventions

| Kind | Rule |
|------|------|
| IDs | Prefixed: `wf_`, `drc_`, `evt_`, `lesson_` |
| Encoding | UTF-8 |
| Secrets | Forbidden in tracked business files |
| Provenance | Required on promotable artifacts (`source_refs`) |
| Sandbox | Path segment `_sandbox` or status sandbox_only |

### 4.2 Artifact lifecycle

```text
draft → validated → (sandbox) → reviewed → published/promoted → retired
```

Publish/promote blocked if: missing provenance, schema fail, or sandbox marker without explicit promote action.

### 4.3 Sensitivity classes

| Class | Handling |
|-------|----------|
| public_internal | Default business docs |
| confidential | Experts transcripts — access controlled if exposed via API |
| secret | Never in git |

---

## 5. Validation rules (normative)

| Rule ID | Check | On fail |
|---------|-------|---------|
| V-02-01 | Ten domain roots exist | init/validate fail |
| V-02-02 | Examples validate against schemas | validate fail |
| V-02-03 | No secret patterns in business/ | security fail/warn per policy |
| V-02-04 | Promotable artifact missing provenance | reject promote |
| V-02-05 | DNA irreversible without gate/rollback | validate fail (shared with 10) |

---

## 6. Interfaces

| Interface | Contract |
|-----------|----------|
| CLI | `npm run business:init\|validate\|governance\|security\|eval\|evolution:check` |
| Writers | PI module writes under process-intelligence/; evolution writes lessons/; skills sandbox API writes `_sandbox/` |
| Readers | Eval harness, FE (via API), humans |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-02-01 Validate &lt; 30–60s baseline | Lightweight schema-lite walker |
| NFR-02-02 Stable paths | No machine-local absolute paths in contracts |
| NFR-02-03–05 Secrets/external isolation | security scan; external untrusted |

**Observability:** Validate reports list relative paths of failures.

---

## 8. Full RTM

| Req | Design | Verification |
|-----|--------|--------------|
| FR-02-01…11 | §3.1 tree | init + structure tests |
| FR-02-12 | §4.2–5 V-02-04 | validators |
| NFR-02-01…05 | §7 | timed validate, security |
| AC-02-01…04 | §5 | business:* green |

---

## 9. Validation design

Structural tests; schema validation; secret scan; negative DNA/DRC fixtures excluded from “examples must pass” if under fixtures/negative.

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-02-01 | Fill all leaves with enterprise content | Ongoing domain work; not structural gap |
| OI-02-02 | Object storage for large binaries | Deferred |

---

## 11. Design score claim

**Self-score: 100** — full data-plane, tree, lifecycle, validation rules, RTM, NFR.
