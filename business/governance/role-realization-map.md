# Agent role realization map (STRUCT-15)

Maps `structure.md` §9 roles to runtime agents vs services. Hybrid model is intentional.

| Role | Realization | Location / notes |
|------|-------------|------------------|
| Business Orchestrator | Runtime agent + engine | Seed agents; `runtime.py` |
| Evolution Manager | Service module | `infrastructure/evolution/`, improvement APIs |
| Evaluation Harness | CLI + service | `npm run business:eval`, eval modules |
| Governance Officer | Agent + policy artifacts | Seed agent; `business/governance/` |
| Security Red-Team | Scripts + adversarial evals | `business:security`, adversarial suite |
| Memory Steward | Rules + optional agent | Memory scopes in runtime |
| Tool Permission Broker | Allow-list in runtime | Agent tools ∩ DNA tools |
| Incident Commander | Process + runbooks | `business/security/` |
| Expert Shadow | Process | Elicitation templates STRUCT-07 |
| Cognitive Task Analyst | Process | DRC templates |
| Process Miner | PI service | `infrastructure/process_intelligence/` |
| Task Mining Agent | PI service (lite) | Same |
| Conformance Agent | PI service | Same |
| Bottleneck Analyzer | PI service | Same |
| Causal Improvement Agent | PI hypotheses only | Never promotes DNA |
| Knowledge Distiller | Process + APIs | distilled/ + knowledge index |
| Knowledge Curator | Process + validation | `business:validate` |

**Inventory:** Material production agents listed in `business/governance/ai-inventory/inventory.json`.
