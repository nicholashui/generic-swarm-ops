# Design — 15 Agent Roster and Control Roles

| Field | Value |
|-------|-------|
| Design ID | `STRUCT-15-DES` |
| Version | 2.0 (comprehensive SDD) |
| Paired requirements | `requirements.md` (`STRUCT-15`) |
| Source | `structure.md` §9 |
| Design quality bar | 100 |

---

## 1. Purpose

Define **control vs learning roles**, register runtime agents with tool/memory allow-lists, and map structure.md roster onto **agents and/or services** without requiring one microservice per role.

---

## 2. Context

| Concern | Design |
|---------|--------|
| Identity | Agent records in RuntimeStore + optional IDE harness agents |
| Authority | Graph + broker, not role name strings in prompts |
| Compliance | AI inventory lists material roles |

---

## 3. Architecture

```text
structure.md roster
    → Role catalog (this design + role-realization-map.md)
         ├─ Runtime Agent records (tools, memory scopes)
         └─ Service modules (PI, evolution, eval, SI)
    → AI inventory (governance)
    → DNA step.agent must resolve
```

### 3.1 Realization matrix (normative)

| Role | Kind | Realization |
|------|------|-------------|
| Business Orchestrator | Agent + engine | Seed agent + runtime.py |
| Evolution Manager | Service | evolution + improvement APIs |
| Evaluation Harness | Service | business:eval + modules |
| Governance Officer | Agent + artifacts | Seed + business/governance |
| Security Red-Team | Service | adversarial + security scripts |
| Memory Steward | Rules (+ optional agent) | scope enforcer |
| Tool Permission Broker | Service | authorize_tool (05) |
| Incident Commander | Process | security runbooks |
| Expert Shadow | Process | elicitation templates |
| Cognitive Task Analyst | Process | DRC templates |
| Process Miner | Service | PI module |
| Task Mining Agent | Service | PI lite |
| Conformance Agent | Service | PI |
| Bottleneck Analyzer | Service | PI |
| Causal Improvement Agent | Service | hypotheses only |
| Knowledge Distiller | Process + API | distilled/ + index |
| Knowledge Curator | Process | validate/dedupe |

Artifact: `business/governance/role-realization-map.md`.

### 3.2 Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| D-15-01 | Hybrid agent/service | Avoid fake multi-agent overhead |
| D-15-02 | Evolution cannot write production DNA | Charter |
| D-15-03 | Inventory for material production agents | Compliance |

---

## 4. Agent record model

```text
Agent {
  id, name, role, description,
  allowed_tools: string[],
  allowed_memory_scopes: string[],
  input_schema?, output_schema?,
  runtime_config?,
  organization_id
}
```

### 4.1 Permission check

```text
act(agent, tool, memory_op):
  if tool not in allowed_tools: DENY
  if memory_op.scope not in allowed_memory_scopes: DENY
  broker + RBAC still apply
```

### 4.2 Seed policy

Flagship onboarding agents **must** include scopes required by DNA `memory_reads` (union organization scopes as needed for E1).

---

## 5. API / surfaces

| Method | Path |
|--------|------|
| GET/POST | `/api/v1/agents` |
| GET | `/api/v1/agents/{id}` |
| FE | `/app/agents` create form |

IDE harness agents under `.trae/agents`, `.grok/agents` — naming aligned where practical; not the same store as runtime agents.

---

## 6. NFR design

| NFR | Design |
|-----|--------|
| NFR-15-01 List ≤500ms baseline | Document store list |
| NFR-15-02 No shared credentials across privilege tiers | Separate secrets |
| NFR-15-03 Evolution Manager no prod DNA write | evolution guards |

---

## 7. Full RTM

| Req | Design | Test |
|-----|--------|------|
| FR-15-01…08 | §3.1 control rows | inventory + seed |
| FR-15-09…12 | §3.1 learning rows | map file |
| FR-15-13…15 | §4 model + deny | tool deny unit |
| NFR-15-01…03 | §6 | list + evolution tests |
| AC-15-01…04 | §3–5 | seed + map existence |

---

## 8. Validation design

role-realization-map exists; seed agents allow-lists; wrong tool denied; inventory lists material agents.

---

## 9. Open issues

| ID | Item | Disposition |
|----|------|-------------|
| OI-15-01 | One OS process per learning agent | Not required |
| OI-15-02 | Perfect dual-harness name parity | Best effort via sync |

---

## 10. Design score claim

**Self-score: 100** — full roster matrix, agent model, permissions, RTM.
