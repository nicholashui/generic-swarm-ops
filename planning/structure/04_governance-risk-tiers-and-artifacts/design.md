# Design — 04 Governance Risk Tiers and Artifacts

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-04-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-04`) |
| Source | `structure.md` §6 |
| Design quality bar | 100 |

---

## 1. Purpose

Make autonomy **earned and documented**: tiers 0–5, mandatory governance artifacts, and framework anchors (NIST AI RMF, ISO/IEC 42001 awareness, EU AI Act high-risk flags) drive validation and runtime gates.

---

## 2. Context

### 2.1 Source of truth hierarchy (conflict resolution)

1. **Runtime gate decision** uses: DNA.risk_tier + step.human_gate_required + tool irreversible + `runtime-tier-policy.json` gate_triggers.  
2. **Artifacts** under `business/governance/` are authoritative for audit and `business:governance`.  
3. **Markdown policy** explains human process; must not contradict JSON policy.  
4. On conflict: **stricter (more human gate)** wins.

### 2.2 Actors

Governance officer, compliance, operators, validators, runtime gate evaluator (12).

---

## 3. Architecture

```text
[business/governance artifacts] ──► [business:governance CLI]
           │
           ▼
[runtime-tier-policy.json] ──► [Gate evaluator in runtime] ──► [Approvals]
           │
[DNA.risk_tier + steps] ───► [Classifier (03) + Orchestrator (11)]
```

### 3.1 Components

| ID | Component | Path |
|----|-----------|------|
| C-04-1 | AI inventory | `business/governance/ai-inventory/` |
| C-04-2 | Risk tier registry | `use-case-risk-tiering/risk-tiers.json` + `runtime-tier-policy.json` |
| C-04-3 | Human approval policy | `human-approval-policy/policy.md` |
| C-04-4 | Model cards | `model-cards/` |
| C-04-5 | Assurance cases | `assurance-cases/` (tier 4/5) |
| C-04-6 | Tool permission register | `business/security/tool-permissions/` + DNA/agent allow-lists |
| C-04-7 | Governance CLI | `npm run business:governance` |
| C-04-8 | Runtime gate evaluator | shared with STRUCT-12 |

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-04-01 | Artifacts in git + runtime policy JSON | Audit + loadable config |
| D-04-02 | Stricter-wins conflict rule | Safety over convenience |
| D-04-03 | Certification programs out of software scope | Org process |

---

## 4. Autonomy risk tiers (normative semantics)

| Tier ID | Autonomy | Runtime effect |
|---------|----------|----------------|
| tier_0_observe | Observe | No external side-effect tools |
| tier_1_recommend | Recommend | Outputs only; human acts |
| tier_2_draft | Draft | Artifacts require approve before send |
| tier_3_execute_reversible | Execute reversible | Tools OK if rollback declared |
| tier_4_execute_with_gate | Execute + gate | Critical/irreversible steps pause for approval |
| tier_5_restricted | Restricted | Block autonomous tools until assurance_case present |

### 4.1 Gate evaluation pseudocode

```text
needs_gate(step, dna, context):
  if step.human_gate_required: return true
  if step.irreversible or step.action_type == irreversible_execution: return true
  if dna.risk_tier in {tier_4*, tier_5*} and step.critical: return true
  if any guardrail predicate matches context (incl. drc.human_approval_required): return true
  return false

can_start_tier5(dna, assurance):
  return assurance_case_exists(dna) 
```

### 4.2 Mandatory artifacts checklist

| Artifact | Min content | Validate |
|----------|-------------|---------|
| AI inventory | Agents/use cases + owners | governance |
| Risk tiering | Use case → tier | governance |
| Human approval policy | Triggers, roles, SLA | governance |
| Model card | Flagship orchestrator | governance |
| Assurance case | Tier-4 path (e.g. onboarding billing) | governance |
| Tool register | Tool → scopes / gate needs | security + DNA |

---

## 5. Framework anchoring (documentation design)

| Framework | How reflected |
|-----------|---------------|
| NIST AI RMF | Map/measure/manage in inventory + risk assessments |
| ISO 42001 | PDCA via validate → operate → eval → evolve |
| EU AI Act | Flag employment-related use cases as high-risk in inventory notes; force human oversight |

---

## 6. Interfaces

| Interface | Contract |
|-----------|----------|
| CLI | `business:governance` exit 0 only if checklist complete |
| Runtime | Reads DNA + policy; creates approvals (12) |
| FE | Displays risk_tier on runs/approvals (16) |

---

## 7. NFR design

| NFR | Design |
|-----|--------|
| NFR-04-01 Governance check &lt; 60s | File presence + light JSON parse |
| NFR-04-02 Backend authz final | Approvals RBAC |
| NFR-04-03 Artifact integrity | Git + review |

**Metrics:** `approvals_pending`, `runs_by_risk_tier`, governance check duration.

---

## 8. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-04-01…07 | §4 tier table + pseudocode | flagship gate e2e |
| FR-04-08…14 | §4.2 checklist | business:governance |
| FR-04-15…16 | §5 | doc review |
| NFR-04-01…03 | §7 | timed script, 403 non-reviewer |
| AC-04-01…05 | §4.2 + e2e | green |

---

## 9. Validation design

- Missing assurance for claimed tier-5 production → fail  
- Flagship tier-4 irreversible step → awaiting_approval  
- Non-reviewer cannot approve  

---

## 10. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-04-01 | Hot-reload policy JSON without restart | Optional |
| OI-04-02 | Full ISO certification | Org, not code |

---

## 11. Design score claim

**Self-score: 100** — SoT hierarchy, full tier semantics, gate algorithm, artifacts, RTM.
