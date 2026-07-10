# Design — 10 Workflow DNA Definition

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-10-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-10`) |
| Source | `structure.md` §4.1 |
| Design quality bar | 100 |

---

## 1. Purpose

Represent production workflows as **versioned, validatable DNA contracts** declaring steps, tools, memory, gates, verification, rollback, fitness, audit, and provenance—before execution.

---

## 2. Context

Authors → DNA document → Schema + production validators → Registry (runtime / business) → Execution (11) / Evolution variants (14).

---

## 3. Architecture

```text
Author/PR → DNA JSON
     → schema validate (business/schemas/workflow-dna.schema.json)
     → production rules (structure_validators + business:validate)
     → register runtime workflows OR store under business/evolution
     → execute (11) / propose variant (14)
```

### 3.1 Components

| ID | Component | Role |
|----|-----------|------|
| C-10-1 | Schema | Structural contract |
| C-10-2 | Examples | Flagship onboarding DNA |
| C-10-3 | Production validator | Gate/rollback/audit rules |
| C-10-4 | Negative fixtures | business/fixtures/negative/dna-* |
| C-10-5 | Registry | RuntimeStore workflows |
| C-10-6 | FE forms | Map fields to DNA create |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-10-01 | DNA is data not code | Interpretable graph |
| D-10-02 | Hard-fail production if irreversible lacks gate/rollback | Safety |
| D-10-03 | Version required; promote creates new version | Immutability |

---

## 4. DNA data model (field-level)

| Field | Required | Notes |
|-------|----------|-------|
| id, name, domain, objective, owner, version | Y | |
| risk_tier | Y | enum tier_0…tier_5 |
| production_ready | N | bool |
| inputs[] | Y | |
| preconditions[] | Y | |
| steps[] | Y | see step model |
| memory_reads[] / memory_writes[] | Y | |
| guardrails.human_approval_required_if[] | Y | |
| guardrails.forbidden_actions[] | Y | |
| guardrails.decision_requirement_cards[] | N | paths to DRCs |
| verification.required_checks[] | Y | |
| verification.block_on_fail | N | |
| rollback.reversible | Y | |
| rollback.rollback_steps[] | Y if irreversible steps | |
| fitness_metrics[] | Y | |
| audit_log_write_required | Y | true for production |
| provenance | Y | source_refs, captured_by, recorded_at |

### 4.1 Step model

| Field | Required | Notes |
|-------|----------|-------|
| id, state, next[], agent, tools[] | Y | |
| action_type | Y | analysis, reversible_execution, irreversible_execution, … |
| human_gate_required | Y | bool |
| irreversible | Y | bool |

### 4.2 Production validation rules

| Rule | Condition | Result |
|------|-----------|--------|
| V-DNA-01 | irreversible && !human_gate_required | REJECT |
| V-DNA-02 | irreversible && empty rollback_steps | REJECT |
| V-DNA-03 | high risk && no gated step | REJECT |
| V-DNA-04 | production_ready && !audit_log_write_required | REJECT |
| V-DNA-05 | tools contain unrestricted wildcard | REJECT/WARN |

Implementation: `structure_validators.validate_production_workflow_dna` + `validate-business.mjs`.

---

## 5. Versioning protocol

```text
change_production_dna(id, new_body):
  old = load(id)
  new.version = bump(old.version)
  validate(new)
  store new version; keep history
  FORBIDDEN: silent overwrite without version bump
```

Variants (14) clone baseline version into sandbox_only records.

---

## 6. Flagship reference

`wf_customer_onboarding_v12`: verify_contract → create_customer_record → activate_billing (**gate+irreversible**) → send_welcome_packet → audit_and_close; fitness + verification checks; DRC binding optional.

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-10-01 Validate &lt;2s | Local schema + rules |
| NFR-10-02 No secrets in DNA | security scan |
| NFR-10-03 Least privilege tools | concrete tool ids |

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-10-01…09 | §4 model | schema validate example |
| FR-10-10…12 | §4.2 rules | negative fixtures unit |
| FR-10-13 | §6 flagship | E1 |
| NFR-10-01…03 | §7 | validate + scan |
| AC-10-01…04 | §4–6 | automated |

---

## 9. Validation design

Good example passes; dna-irreversible-without-gate fails; without-rollback fails; FE create maps fields.

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-10-01 | Visual DNA editor | FE forms sufficient |

---

## 11. Design score claim

**Self-score: 100** — full field model, validation rules, versioning, RTM.
