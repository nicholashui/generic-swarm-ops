# PR priority lattice checklist (STRUCT-01)

Ordered design priorities (must not invert):

1. **Safety**
2. **Auditability**
3. **Correctness**
4. **Efficiency**
5. **Autonomy**

## Before merge — reviewer checks

- [x] Change does not increase autonomy without eval evidence and gates.
- [x] Change does not weaken auditability for efficiency.
- [x] Evolution path cannot mutate production DNA directly / no `auto_promote`.
- [x] New tools are allow-listed; irreversible steps have human gates + rollback.
- [x] High-impact memory/knowledge writes carry provenance.
- [x] If trade-off exists, higher lattice priority wins (document in PR body).

## Evidence hooks

| Principle | Hook |
|-----------|------|
| Sandbox evolution | evolution APIs + `business:evolution:check` |
| Everything testable | `business:eval` + unit/e2e |
| Bounded autonomy | risk tiers + approvals |
| Provenance | retrieval `source_refs` + memory provenance |
