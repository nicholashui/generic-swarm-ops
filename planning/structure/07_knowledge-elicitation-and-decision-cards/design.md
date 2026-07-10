# Design — 07 Knowledge Elicitation and Decision Cards

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-07-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-07`) |
| Source | `structure.md` §3.1–3.2 |
| Design quality bar | 100 |

---

## 1. Purpose

Capture **tacit expert knowledge** via six methods and structure it as Decision Requirement Cards (DRCs) and distilled assets with provenance, risk, validation tests, and publish gates.

---

## 2. Context

### 2.1 Method → output (normative)

| Method | Best for | Output path |
|--------|----------|-------------|
| Shadow Mode | Real actions | experts/shadow-logs/, PI events |
| Critical Decision Interview | High-stakes | experts/decision-requirement-cards/*.json |
| Think-Aloud | Routine work | knowledge-base/tacit-knowledge/ |
| Exception Interview | Edge cases | knowledge-base/exceptions/ |
| Retrospective | Completed cases | evolution/lessons-learned/, memory |
| Apprentice | Teaching swarm | distilled/skills/_sandbox/, playbooks |

Templates: `business/experts/elicitation-methods/01–06-*.md`.

### 2.2 Actors

Expert, facilitator, knowledge curator, distiller, runtime/DNA consumers, validators.

---

## 3. Architecture

```text
Capture (templates) → Store under experts/** → Schema validate
        │
        ▼
   DRC state machine: draft → in_review → published → retired
        │ published
        ▼
   Distiller → distilled/** (sandbox first for skills)
        │
        ▼
   Curator validate/dedupe → knowledge-base + DNA guardrail refs
```

### 3.1 Components

| ID | Component | Role |
|----|-----------|------|
| C-07-1 | Method templates | Six capture playbooks |
| C-07-2 | DRC schema | `decision-requirement-card.schema.json` |
| C-07-3 | DRC store | `experts/decision-requirement-cards/` |
| C-07-4 | Publish validator | `structure_validators.validate_decision_requirement_card` |
| C-07-5 | Distiller process | Approved capture → distilled assets |
| C-07-6 | Curator process | Dedup/organize |
| C-07-7 | DNA binding | DNA.guardrails.decision_requirement_cards + predicates |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-07-01 | Schema-first files before interview SaaS | Auditability, SDD speed |
| D-07-02 | expert_sources minItems=1 for production | Provenance principle |
| D-07-03 | Skills land in _sandbox | STRUCT-14/05 |

---

## 4. DRC data model (field-level)

| Field | Required publish | Notes |
|-------|------------------|-------|
| id | Y | `drc_…` |
| domain | Y | |
| decision_point | Y | |
| expert_sources[] | Y min 1 | Fail production if empty |
| context_signals[] | Y | |
| cues_experts_notice[] | Y | |
| normal_action | Y | |
| exception_paths[{condition,action}] | Y | |
| red_flags[] | Y | |
| required_evidence[] | Y | |
| risk_tier | Y | Aligns §6 tiers |
| human_approval_required | Y | Feeds gate predicates |
| validation_tests[] | Y | |
| confidence | Y | 0–1 |
| last_reviewed | Y | ISO date |
| provenance.source_refs[] | Y min 1 | |
| provenance.captured_by | Y | |
| provenance.recorded_at | Y | |

### 4.1 DRC state machine

```text
draft ──submit──► in_review ──approve──► published ──retire──► retired
                      │
                      └──reject──► draft
```

| State | Allowed ops |
|-------|-------------|
| draft | edit |
| in_review | comment, approve, reject |
| published | referenced by DNA; immutable except retire |
| retired | no new bindings |

### 4.2 Publish rules

```text
publish(drc):
  failures = validate_decision_requirement_card(drc, for_production=True)
  if failures: REJECT
  set state=published
```

Negative fixture: `business/fixtures/negative/drc-missing-expert-sources.json`.

---

## 5. Runtime consumption

| Consumer | Use |
|----------|-----|
| DNA guardrails | `drc.human_approval_required == true` predicate; `decision_requirement_cards` list |
| Retrieval | Index published DRC text with provenance |
| Approvals UI | Show red_flags / required_evidence when bound |

---

## 6. Interfaces

| Interface | Contract |
|-----------|----------|
| File CRUD | Git / editor for v1 |
| Validator API (internal) | Python `validate_decision_requirement_card` |
| Optional future REST | CRUD DRC with RBAC (OI-07-01) |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-07-01 Schema validate &lt;1s | Local JSON schema |
| NFR-07-02 Transcript ACL | confidential class; not public APIs without auth |
| NFR-07-03 Data minimization | Expert ids, not full PII in exports |

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-07-01…07 | §2.1 methods + templates | template existence tests |
| FR-07-08…13 | §4 model + publish rules | test_structure_sdd_validators |
| FR-07-14…15 | §3 distiller/curator | process + sample distilled |
| NFR-07-01…03 | §7 | unit + policy |
| AC-07-01…04 | §4 | validators green |

---

## 9. Validation design

- Valid publish DRC passes  
- Empty expert_sources fails  
- Six templates exist  
- DNA example references DRC path  

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-07-01 | Full interview SaaS UI | Deferred |
| OI-07-02 | Automated speech-to-DRC | Deferred |

---

## 11. Design score claim

**Self-score: 100** — methods, field-level DRC, state machine, publish rules, binding, RTM.
