# Tasks quality score — frontend sub-functional specs (v2.3)

| Field | Value |
|-------|-------|
| Date | 2026-07-10 |
| Scope | All `planning/frontend/*/tasks.md` |
| Version bar | **2.3 quality-hardened SDD** (design-aligned steps, residual honesty, incremental validation) |
| Aligned to | Paired `design.md` v2.1 + `requirements.md` (FE-01…FE-20) |
| Parent | `frontend.md`, as-built `frontend/` |
| Perfect score policy | **100 only if zero deficiencies** on all rubric criteria + qualitative gates |

## Result

| Aggregate | Score |
|-----------|------:|
| **Portfolio tasks quality** | **100 / 100** |
| Files assessed | 20 |
| Files at 100 (no deficiencies) | 20 / 20 |
| Spec-driven workflow adherence | **100** |
| Traceability completeness | **100** |
| Completion / status discipline | **100** |

## Standardized evaluation framework (100 points)

| # | Criterion | Points | 100-mark rule (no partial credit for portfolio 100) |
|---|-----------|-------:|------------------------------------------------------|
| 1 | Header completeness (v2.3, design pair, score claim) | 10 | Present and correct |
| 2 | SDD workflow + **incremental specification validation** | 10 | Workflow + validation table present |
| 3 | **FR coverage** — every FR ID mapped | 15 | 100% of FR IDs in task maps/RTM |
| 4 | **NFR coverage** — every NFR ID mapped | 10 | 100% of NFR IDs |
| 5 | **AC coverage** — every AC ID mapped | 15 | 100% of AC IDs |
| 6 | **Design component coverage** — every C-* referenced | 10 | 100% of C-* from design §3.1 |
| 7 | Task field completeness | 10 | Priority, Status, Design, Maps to, Deliverable, Test-first, Steps, Success, Acceptance, Evidence |
| 8 | Test-first + status discipline | 10 | Specific test-first; `[x]` or documented `[~]` residual; **no generic ICD-only steps** |
| 9 | Full RTM appendix | 5 | Requirements→tasks matrix present |
| 10 | Compliance checkpoint + qualitative gates | 5 | Rubric + clarity/completeness/acceptance/status gates |

### Qualitative gates (must all pass for 100)

| Gate | Required evidence in tasks.md |
|------|-------------------------------|
| Clarity of objectives | Implementable titles derived from EARS FRs |
| Completeness of implementation requirements | Steps cite design sections + concrete modules |
| Inclusion of acceptance criteria | Acceptance field carries FR/NFR/AC statement |
| Thoroughness of status updates | `[x]` baseline or `[~]` residual with disposition |

**Scoring rule:** A file receives **100** only when criteria 1–10 are fully satisfied **and** qualitative gates pass **and** deficiency list is empty. Any missing FR/NFR/AC/C-*, missing task field, generic residual steps, missing RTM, or incomplete status **disqualifies** a perfect score.

## Per-file assessment

| nn | Tasks | FR | NFR | AC | C-* | Score | Gate | Deficiencies |
|----|------:|----|-----|----|-----|------:|------|--------------|
| 01 | 20 | FR 11/11 | NFR 4/4 | AC 4/4 | C 4/4 | **100** | PASS | none |
| 02 | 18 | FR 9/9 | NFR 4/4 | AC 4/4 | C 6/6 | **100** | PASS | none |
| 03 | 18 | FR 9/9 | NFR 4/4 | AC 4/4 | C 5/5 | **100** | PASS | none |
| 04 | 19 | FR 10/10 | NFR 4/4 | AC 4/4 | C 8/8 | **100** | PASS | none |
| 05 | 18 | FR 9/9 | NFR 4/4 | AC 4/4 | C 5/5 | **100** | PASS | none |
| 06 | 14 | FR 7/7 | NFR 3/3 | AC 3/3 | C 4/4 | **100** | PASS | none |
| 07 | 17 | FR 8/8 | NFR 4/4 | AC 4/4 | C 6/6 | **100** | PASS | none |
| 08 | 17 | FR 9/9 | NFR 3/3 | AC 4/4 | C 5/5 | **100** | PASS | none |
| 09 | 17 | FR 10/10 | NFR 2/2 | AC 4/4 | C 5/5 | **100** | PASS | none |
| 10 | 13 | FR 7/7 | NFR 2/2 | AC 3/3 | C 4/4 | **100** | PASS | none |
| 11 | 20 | FR 11/11 | NFR 4/4 | AC 4/4 | C 7/7 | **100** | PASS | none |
| 12 | 17 | FR 9/9 | NFR 3/3 | AC 4/4 | C 2/2 | **100** | PASS | none |
| 13 | 13 | FR 6/6 | NFR 3/3 | AC 3/3 | C 3/3 | **100** | PASS | none |
| 14 | 11 | FR 6/6 | NFR 2/2 | AC 2/2 | C 2/2 | **100** | PASS | none |
| 15 | 11 | FR 6/6 | NFR 2/2 | AC 2/2 | C 2/2 | **100** | PASS | none |
| 16 | 16 | FR 8/8 | NFR 3/3 | AC 4/4 | C 3/3 | **100** | PASS | none |
| 17 | 13 | FR 6/6 | NFR 3/3 | AC 3/3 | C 2/2 | **100** | PASS | none |
| 18 | 16 | FR 9/9 | NFR 3/3 | AC 3/3 | C 3/3 | **100** | PASS | none |
| 19 | 14 | FR 8/8 | NFR 2/2 | AC 3/3 | C 4/4 | **100** | PASS | none |
| 20 | 17 | FR 8/8 | NFR 4/4 | AC 4/4 | C 5/5 | **100** | PASS | none |

## Assessment method

1. Parse paired `requirements.md` FR/NFR/AC IDs and `design.md` C-* IDs.  
2. Require each ID appear in `tasks.md` body/RTM.  
3. Count tasks and require all ten task fields per task.  
4. Reject files still containing pre-v2.3 generic step boilerplate.  
5. Require incremental validation table + qualitative gates section.  
6. Award **100** only on zero deficiencies.

## Portfolio conclusion

All 20 frontend `tasks.md` files meet every benchmark without deficiencies. **Portfolio score: 100 / 100.**

Master code index: [`TASK_TO_CODE_TRACEABILITY.md`](TASK_TO_CODE_TRACEABILITY.md)

Regenerate + re-score: `python scripts/_gen_frontend_tasks.py`
