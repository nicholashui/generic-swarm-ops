# Improvement Waves — Planning Index

**Source of truth (strategy):** `improvements.md` v1.0  
**SDD protocol:** `improvement_prompt.txt`  
**Product host:** generic-swarm-ops  

Each wave folder contains the mandatory SDD quartet:

| File | Phase |
|------|--------|
| `requirements.md` | Phase 1 |
| `design.md` | Phase 2 |
| `tasks.md` | Phase 3 |
| `completion-report.md` | Post-implement evidence |

---

## Status (current)

| Wave | Theme | SDD | Implement | N3 impact |
|------|--------|-----|-----------|-----------|
| **0** | Catalog, schemas, inventory script | Done | Done | L0 114 dirs |
| **1** | ALC + domain register + FE pack panel | Done | Done | ALC gate |
| **2** | Spine + viral-hook DNA, stubs, E2E | Done | Done | L2 spine |
| **3** | Coevolution, lesson utility, LQR eval | Done | Done | Learning |
| **4** | Multi-pack load, security, runbook | Done | Done | N2 proof |
| **5** | Full roster + process wiring | Done | Done | **N3 complete** |

**Live gates (re-run anytime):**

```bash
python scripts/business/inventory_check.py
# → INVENTORY PASS count=114 n3=complete

cd backend && python -m pytest app/tests/unit -q
```

---

## How to read completion reports

- **Verification numbers** (e.g. “87 passed”) are **snapshots at wave exit**, not forever-current suite sizes.
- Later waves intentionally grow the unit suite and tighten inventory (Wave 5 adds N3 gates + CI workflow).
- **Residual** sections are forward-looking at the time of writing; check newer wave completion reports for supersession.

---

## Doc correctness review (2026-07-12)

Review of all 24 markdown files under `planning/improvement/`:

### Correct (verified against repo)

- Wave 0–5 SDD folders complete with completion reports.
- Artifact paths for DNA, packs (`video`, `example_research`, `example_education`), coevolution, isolation helpers, N3 status API, FE panels exist.
- Inventory **114** + `n3=complete`; DNA workflow count **14**; process_coverage `va_only_count=0`.
- N1/N2/N3 statements consistent with `adoption.md` / `improvements.md` intent.
- API surfaces documented in Wave 3–5 match routes (`/evolution/coevolution/run`, `/improvement/lesson-utility`, `/domains/video/n3-status`, etc.).

### Issues found and fixed in this review

| Issue | Fix |
|-------|-----|
| Wave 3 tasks: wrong inventory command `python -m scripts.inventory_check` | → `python scripts/business/inventory_check.py` |
| Wave 3/4 tasks: acceptance checkboxes still `[ ]` after completion | Marked `[x]` / status completed |
| Wave 3 design: test name `test_coevolution_multi_generation` ≠ code | Aligned to `…_sandbox_only` + helper test |
| Wave 2 tasks: standby field `active_candidate` (never used) | → `"spine": true` |
| Wave 2 completion: brittle “9 spine flags” claim | Softened; pytest path made explicit |
| Wave 0 residual risks stale (CLI-only register, no CI) | Annotated as superseded by Wave 1 / 5 |
| Wave 5 tasks.md underspecified vs SDD prompt | Expanded with paths + completed AC checkboxes |
| Missing folder-level index | This `README.md` |

### Residual doc caveats (intentional, not bugs)

1. **Historical suite counts** in older completion reports stay as-of-exit (do not rewrite to 104).
2. **Wave 0–2 residual sections** still mention “next wave” work that is now done — keep for audit trail; use this README for current status.
3. **Thin DNA** (Wave 5) is explicit N3 representation depth, not full specialist L2 production polish — called out in Wave 5 requirements/completion.
4. Some early tasks.md (Wave 2 original) remain shorter than later waves; content is still accurate after the standby fix.

---

## Related

- `docs/domain-packs.md`
- `docs/add-domain-pack-runbook.md`
- `docs/domain-pack-versioning-matrix.md`
- `business/video/PROCESSES.md`
- `memory/handoff.md`
