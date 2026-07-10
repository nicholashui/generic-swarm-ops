# 02 — Business Artifact Repository

| Field | Value |
|-------|-------|
| Spec ID | `STRUCT-02` |
| Source | `structure.md` §3.5 |
| Priority order | 02 |
| Status | Specification |
| Owner | Platform + Knowledge stewardship |

---

## 1. Scope

### 1.1 In scope
- First-party directory layout under `business/` for process intelligence, knowledge, experts, materials, distilled assets, memory, evals, governance, security, and evolution.
- Separation of schemas/examples from runtime state.
- Machine-readable contracts where defined by schemas.

### 1.2 Out of scope
- Runtime database internals (see execution/control-plane implementations).
- Full enterprise content population of every leaf folder.
- External source downloads under `external/sources/`.

---

## 2. Stakeholder Requirements

| ID | Stakeholder | Need |
|----|-------------|------|
| STK-02-01 | Knowledge curator | Predictable places for rules, SOPs, provenance. |
| STK-02-02 | Governance officer | Inventory, policies, model cards, assurance cases on disk. |
| STK-02-03 | Evaluation owner | Golden/regression/adversarial corpora under `evals/`. |
| STK-02-04 | Evolution manager | Sandbox DNA and lessons under `evolution/`. |
| STK-02-05 | Auditor | Traceable artifact paths for compliance review. |

---

## 3. Functional Requirements (EARS)

| ID | Statement (EARS) |
|----|------------------|
| FR-02-01 | The system shall maintain a first-party `business/` tree with the top-level domains defined in structure.md §3.5. |
| FR-02-02 | When process-intelligence outputs are produced, the system shall store them under `business/process-intelligence/` subfolders for event logs, discovered processes, conformance, bottlenecks, and causal hypotheses. |
| FR-02-03 | When knowledge assets are curated, the system shall place rules, decision patterns, exceptions, best practices, tacit knowledge, and provenance under `business/knowledge-base/`. |
| FR-02-04 | When expert capture artifacts are created, the system shall store profiles, shadow logs, decision-requirement cards, and interview transcripts under `business/experts/`. |
| FR-02-05 | When source materials are ingested for distillation, the system shall store documents, regulations, and SOPs under `business/materials/`. |
| FR-02-06 | When skills, prompts, workflows, checklists, or playbooks are distilled, the system shall store them under `business/distilled/`. |
| FR-02-07 | While memory corpus files are retained on disk, the system shall organize episodic, semantic, procedural, decision, and evaluation memory under `business/memory/`. |
| FR-02-08 | The system shall retain evaluation suites under `business/evals/` including golden tasks, regression tests, adversarial tests, human-review sets, and benchmark results. |
| FR-02-09 | The system shall retain governance artifacts under `business/governance/` including AI inventory, risk tiering, human-approval policy, model cards, and assurance cases. |
| FR-02-10 | The system shall retain security artifacts under `business/security/` including threat models, tool permissions, prompt-injection tests, red-team results, and incident reports. |
| FR-02-11 | The system shall retain evolution artifacts under `business/evolution/` including workflow DNA, successful variants, failed experiments, mutation history, and lessons learned. |
| FR-02-12 | If an artifact lacks required provenance metadata where policy demands it, then the system shall reject promotion of that artifact to production use. |

---

## 4. Non-Functional Requirements

### 4.1 Performance
| ID | Statement |
|----|-----------|
| NFR-02-01 | Repository layout validation shall complete in under 30 seconds for the baseline tree on a developer workstation. |
| NFR-02-02 | Artifact paths shall be stable so scripts and evals can address them without hard-coded machine-local paths. |

### 4.2 Security
| ID | Statement |
|----|-----------|
| NFR-02-03 | The repository shall not store live secrets (API keys, passwords) in tracked business artifacts. |
| NFR-02-04 | If a scanned business file matches secret patterns, then the security check shall fail or warn per policy. |
| NFR-02-05 | External untrusted sources shall remain outside `business/` until audited and curated. |

---

## 5. Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC-02-01 | `business/` contains the ten domain roots listed in structure.md §3.5. |
| AC-02-02 | `npm run business:init` (or equivalent) creates missing required folders. |
| AC-02-03 | `npm run business:validate` fails when required schema-backed examples are invalid. |
| AC-02-04 | No production credentials appear in tracked `business/` files. |

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| STRUCT-01 charter | 03–17 (artifact consumers) |
| Starter bootstrap / scripts | Validation tooling |

---

## 7. Test Validation Protocols

| ID | Protocol | Type |
|----|----------|------|
| TV-02-01 | Structural test: assert required directories exist. | Automated |
| TV-02-02 | Schema validation against `business/schemas/*` examples. | Automated |
| TV-02-03 | Secret scan on `business/` via `npm run business:security`. | Automated |
| TV-02-04 | Spot-check: each top-level domain has a README or seed artifact. | Review |

---

## 8. Traceability

| structure.md | This spec |
|--------------|-----------|
| §3.5 Folder Structure | FR-02-01 … FR-02-11 |
| Provenance always (cross-ref §1) | FR-02-12 |
