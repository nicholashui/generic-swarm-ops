# Elicitation methods (STRUCT-07)

Map each capture method to outputs under `business/`. Templates live in this folder.

| Method | Template | Primary output |
|--------|----------|----------------|
| Shadow Mode | `01-shadow-mode.md` | `experts/shadow-logs/`, PI event logs |
| Critical Decision Interview | `02-critical-decision-interview.md` | `experts/decision-requirement-cards/` |
| Think-Aloud Session | `03-think-aloud.md` | `knowledge-base/tacit-knowledge/` |
| Exception Interview | `04-exception-interview.md` | `knowledge-base/exceptions/` |
| Retrospective Review | `05-retrospective-review.md` | `evolution/lessons-learned/`, decision memory |
| Apprentice Mode | `06-apprentice-mode.md` | `distilled/skills/`, `distilled/playbooks/` |

**Publish rule:** Decision requirement cards require non-empty `expert_sources` and `provenance` before production use (schema + `test_structure_sdd_validators.py`).
