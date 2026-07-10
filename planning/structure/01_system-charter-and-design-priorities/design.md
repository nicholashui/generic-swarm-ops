# Design — 01 System Charter and Design Priorities

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-01-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-01`) |
| Source | `structure.md` §0–1 |
| Design quality bar | 100 — policy kernel fully specified for enforcement |

---

## 1. Purpose and quality bar

Encode mission capabilities and ordered design priorities as an **enforceable policy kernel** consumed by design-time gates and runtime guards. Downstream components fail closed if a change would invert:

**Safety → Auditability → Correctness → Efficiency → Autonomy.**

### 1.1 Target vs as-built

| Aspect | Target (this design) | As-built |
|--------|----------------------|----------|
| Policy source | structure.md + PR checklist + validators | structure.md, evolution/eval guards |
| Machine lattice | Documented algorithm + review checklist | Documented; PR checklist at `PR_PRIORITY_LATTICE_CHECKLIST.md` |
| Auto-mutate ban | Runtime + harness invariants | Implemented in evolution + eval paths |

---

## 2. Context and boundaries

### 2.1 Actors

| Actor | Interaction |
|-------|-------------|
| Architect / PR author | Proposes change; must pass lattice review |
| Reviewer | Applies checklist |
| Runtime | Enforces non-mutation / no auto-promote |
| Eval harness | Blocks unattended production promote |
| Downstream specs 02–17 | Inherit priority order |

### 2.2 Trust boundary

Charter rules are **not** LLM-interpretable policy only. Enforcement is deterministic code and human review checklists outside model prompts.

### 2.3 In / out of scope

**In:** Mission capabilities, priority lattice, seven principles→control hooks, PR gate, runtime hooks.  
**Out:** Microservice policy engine, multi-tenant SaaS policy UI.

---

## 3. Architecture

### 3.1 Context

```text
[Authors/PRs] ──► [Design-time gates: checklist + business:* scripts]
                              │
[Operators/API] ──► [Runtime guards: evolution, eval, DNA validators]
                              │
                    [Charter Policy Kernel]
                     mission · lattice · principles
```

### 3.2 Components

| ID | Component | Responsibility | Artifact |
|----|-----------|----------------|----------|
| C-01-1 | Mission catalog | Four capabilities (learn, distill, execute, sandbox-evolve) | structure.md §0 |
| C-01-2 | Priority lattice | Total order + conflict resolver | Algorithm §4.1 |
| C-01-3 | Principle catalog | Seven principles | structure.md §1 |
| C-01-4 | Design-time gate | PR checklist + validate scripts | `PR_PRIORITY_LATTICE_CHECKLIST.md` |
| C-01-5 | Runtime gate hooks | Block auto_promote / direct DNA mutate | evolution + eval modules |
| C-01-6 | Traceability index | Principle → FR/control in 02–17 | §5 matrix |

### 3.3 Design decisions

| ID | Decision | Alternatives rejected | Rationale |
|----|----------|----------------------|-----------|
| D-01-01 | Policy kernel, not microservice | Central policy API service | Unnecessary until multi-tenant SaaS |
| D-01-02 | Dual enforcement (review + runtime) | Runtime-only | Catches design-time autonomy creep |
| D-01-03 | Priorities are total order, not weighted scores | Multi-criteria scoring | Matches structure.md explicit order |

---

## 4. Control logic specification

### 4.1 Priority lattice algorithm

```text
PRIORITIES = [Safety, Auditability, Correctness, Efficiency, Autonomy]

resolve(conflict_a, conflict_b):
  for p in PRIORITIES:
    if conflict_a.hurts(p) and not conflict_b.hurts(p): return b
    if conflict_b.hurts(p) and not conflict_a.hurts(p): return a
  return require_human_architecture_review()
```

### 4.2 Mission capabilities (normative)

| Cap | Description | Downstream owner |
|-----|-------------|------------------|
| M1 | Learn from documents, experts, event logs | 06, 07 |
| M2 | Distill to rules, skills, workflows, playbooks | 07, 10 |
| M3 | Execute bounded auditable workflows | 11, 12 |
| M4 | Evolve only in sandbox | 14 |

### 4.3 Principle → enforcement hooks

| Principle | Design-time | Runtime |
|-----------|-------------|---------|
| Evidence over opinion | PI/eval required for autonomy claims | PI artifacts feed proposals |
| Bounded autonomy | Risk tier + DNA gates in validate | Approvals, allow-lists |
| Everything testable | business:eval in CI | block_on_fail, promote checklist |
| Sandbox evolution | evolution:check | sandbox_only, no auto_promote |
| Provenance always | schema required fields | memory/retrieval provenance |
| Reversibility first | DNA rollback rules | gate irreversible tools |
| Human-centered | HAI checklist | FE evidence, approvals |

### 4.4 Invariants (must never be false)

| INV | Statement |
|-----|-----------|
| INV-01-1 | No API sets production DNA via auto_promote without human path |
| INV-01-2 | Evolution cannot write active production DNA in place |
| INV-01-3 | Eval pass alone never equals unattended production promote |
| INV-01-4 | Priority order is not overridable by prompt text |

---

## 5. Interfaces

### 5.1 Design-time interface

| Input | Output |
|-------|--------|
| PR description + diff | `ACCEPT \| REVISE \| REJECT` + violated principle IDs |
| business:* scripts | pass/fail |

### 5.2 Runtime interface (hooks)

| Hook | Consumer | Behavior |
|------|----------|----------|
| `reject_direct_production_mutation` | Evolution | 4xx / ValidationError |
| `reject_auto_promote` | Evolution / eval | Block |
| `require_eval_before_promote` | Evolution | Checklist |

---

## 6. NFR design

| ID | Spec | Design response |
|----|------|-----------------|
| NFR-01-01 | No LLM for principle checks | Code + checklist only |
| NFR-01-02 | Documentable in one review cycle | PR checklist ≤ 1 page |
| NFR-01-03 | Not bypassable by prompts | Authz outside LLM |
| NFR-01-04 | Reject unattended production DNA mutation features | INV-01-1…3 |

**Observability:** Audit events `approval.*`, `evolution.*`, `lesson.*` for governance-relevant actions.

---

## 7. Full RTM

| Req | Design element | Verification |
|-----|----------------|--------------|
| FR-01-01…04 | §4.2 Mission M1–M4 | structure.md + status |
| FR-01-05…08 | §4.1 Lattice | PR checklist |
| FR-01-09…16 | §4.3 Principles | Evolution/eval/DNA tests |
| NFR-01-01…04 | §6 | test_structure_sdd + evolution unit |
| AC-01-01…04 | Checklist + INV | Review + automated invariants |

---

## 8. Validation design

| Test | Method |
|------|--------|
| Non-mutation | Unit: auto_promote / direct mutate rejected |
| No eval auto-promote | Harness / evolution unit |
| PR checklist present | File exists under planning/structure/ |
| Downstream designs reference charter | Spec review 02–17 |

---

## 9. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-01-01 | Machine-readable OPA/Rego charter | Deferred; not required for bar 100 |
| OI-01-02 | Multi-tenant policy service | Deferred |

---

## 10. Design score claim

**Self-score: 100** — full context, components, algorithms, invariants, interfaces, NFR, complete RTM, validation, open issues.
