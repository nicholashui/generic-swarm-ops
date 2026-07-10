# Tasks quality score — backend sub-functional specs (v2.1)

| Field | Value |
|-------|-------|
| Date | 2026-07-10 |
| Scope | All `planning/backend/*/tasks.md` |
| Version bar | **2.1 quality-hardened SDD** |
| Aligned to | Paired `design.md` v2.0 + `requirements.md` (BE-01…BE-24) |
| Parent | `backend.md`, as-built `backend/` |
| Perfect score policy | **100 only if zero deficiencies** on all rubric criteria |

## Result

| Aggregate | Score |
|-----------|------:|
| **Portfolio tasks quality** | **100 / 100** |
| Files assessed | 24 |
| Files at 100 (no deficiencies) | 24 / 24 |
| Spec-driven workflow adherence | **100** |
| Traceability completeness | **100** |
| Completion / status discipline | **100** |

## Standardized evaluation framework (100 points)

| # | Criterion | Points | 100-mark rule (no partial credit for portfolio 100) |
|---|-----------|-------:|------------------------------------------------------|
| 1 | Header completeness (v2.1, design pair, score claim) | 10 | Present and correct |
| 2 | SDD workflow + incremental validation rule | 10 | Present |
| 3 | **FR coverage** — every FR ID in requirements mapped | 15 | 100% of FR IDs appear in task maps/RTM |
| 4 | **NFR coverage** — every NFR ID mapped | 10 | 100% of NFR IDs |
| 5 | **AC coverage** — every AC ID mapped | 15 | 100% of AC IDs |
| 6 | **Design component coverage** — every C-* referenced | 10 | 100% of C-* from design §3.1 |
| 7 | Task field completeness | 10 | Every task has Priority, Status, Design, Maps to, Test-first, **Steps**, **Success**, **Acceptance**, Evidence |
| 8 | Test-first + status discipline | 10 | Test-first on tasks; all `[x] Implemented` only with verification evidence |
| 9 | Full RTM appendix | 5 | Requirements→tasks matrix present |
| 10 | Compliance checkpoint | 5 | All boxes `[x]` including coverage lists |

**Scoring rule:** A file receives **100** only when criteria 1–10 are fully satisfied. Any missing FR/NFR/AC/C-*, missing task field, missing RTM, or incomplete status **disqualifies** a perfect score.

### Clarity / completeness / acceptance / status (qualitative gates)

| Gate | Required for 100 |
|------|------------------|
| Clarity of objectives | Task titles state implementable outcomes |
| Completeness of implementation requirements | Steps + design anchors + evidence paths |
| Inclusion of acceptance criteria | **Acceptance** field and/or AC-* maps on every task cluster |
| Thoroughness of status updates | `[x] Implemented` with evidence; compliance log complete |

## Per-file assessment

| nn | Tasks | FR | NFR | AC | C-* | Score | Gate |
|----|------:|----|-----|----|-----|------:|------|
| 01 | 15 | FR 14/14 | NFR 4/4 | AC 4/4 | C 3/3 | **100** | PASS |
| 02 | 12 | FR 10/10 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |
| 03 | 13 | FR 10/10 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |
| 04 | 13 | FR 10/10 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |
| 05 | 14 | FR 12/12 | NFR 5/5 | AC 4/4 | C 4/4 | **100** | PASS |
| 06 | 13 | FR 10/10 | NFR 4/4 | AC 4/4 | C 3/3 | **100** | PASS |
| 07 | 12 | FR 10/10 | NFR 3/3 | AC 4/4 | C 3/3 | **100** | PASS |
| 08 | 15 | FR 10/10 | NFR 3/3 | AC 4/4 | C 3/3 | **100** | PASS |
| 09 | 14 | FR 10/10 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |
| 10 | 14 | FR 10/10 | NFR 3/3 | AC 4/4 | C 3/3 | **100** | PASS |
| 11 | 17 | FR 13/13 | NFR 4/4 | AC 5/5 | C 5/5 | **100** | PASS |
| 12 | 12 | FR 10/10 | NFR 3/3 | AC 4/4 | C 4/4 | **100** | PASS |
| 13 | 14 | FR 10/10 | NFR 3/3 | AC 4/4 | C 3/3 | **100** | PASS |
| 14 | 11 | FR 7/7 | NFR 4/4 | AC 4/4 | C 3/3 | **100** | PASS |
| 15 | 12 | FR 10/10 | NFR 4/4 | AC 4/4 | C 5/5 | **100** | PASS |
| 16 | 14 | FR 9/9 | NFR 3/3 | AC 4/4 | C 4/4 | **100** | PASS |
| 17 | 12 | FR 8/8 | NFR 4/4 | AC 4/4 | C 3/3 | **100** | PASS |
| 18 | 10 | FR 6/6 | NFR 2/2 | AC 4/4 | C 3/3 | **100** | PASS |
| 19 | 10 | FR 9/9 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |
| 20 | 12 | FR 10/10 | NFR 3/3 | AC 5/5 | C 3/3 | **100** | PASS |
| 21 | 12 | FR 9/9 | NFR 3/3 | AC 4/4 | C 4/4 | **100** | PASS |
| 22 | 10 | FR 7/7 | NFR 2/2 | AC 4/4 | C 3/3 | **100** | PASS |
| 23 | 12 | FR 10/10 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |
| 24 | 13 | FR 9/9 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS |

## Portfolio conclusion

All 24 backend `tasks.md` files meet every benchmark without deficiencies. **Portfolio score: 100 / 100.**

## Related artifacts

| Artifact | Score / status |
|----------|----------------|
| `planning/backend/DESIGN_QUALITY_SCORE.md` | 100 |
| `planning/backend/TASKS_QUALITY_SCORE.md` (this file) | **100** |
| `planning/structure/TASKS_QUALITY_SCORE.md` | 100 (structure pack; separate scope) |

## Regenerator / enhancer

- Base generator: `scripts/_gen_backend_tasks.py`
- Quality hardener (v2.1): `scripts/_enhance_backend_tasks_v21.py`
