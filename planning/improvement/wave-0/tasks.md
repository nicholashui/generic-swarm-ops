# Wave 0 Tasks

**Wave:** 0  
**Design:** `planning/improvement/wave-0/design.md`  
**Requirements:** `planning/improvement/wave-0/requirements.md`  

Execute in order. Tag: **[Structure]** | **[Backend]** | **[Frontend]**

---

## Task group A — Structure: catalog export

### T1 — Generator script + ROSTER / MAP / agent dirs  [Structure]
- **Create:** `scripts/business/generate_video_pack_catalog.py`
- **Action:** Embed Appendix A (114 pack_ids from `adoption.md`). Write `business/video/ROSTER.json`, `MAP.md`, and for each pack_id: dir + `agent_spec.json` + `SPEC.md` + `prompts/.gitkeep` + `rubrics/.gitkeep`.
- **Pattern:** Idempotent; skip overwrite of richer agent_spec if already customized (Wave 0: always regenerate minimal is OK once).
- **Acceptance:** count(dirs)==114; ROSTER length 114; unique pack_ids.

### T2 — PROCESSES.md + video README + tree  [Structure]
- **Create:** `business/video/PROCESSES.md`, `business/video/README.md`, skeleton dirs (workflows, tools, evals/*, knowledge/seeds, policies, ui), `tools/adapters.md`, draft `manifest.json`.
- **Acceptance:** PROCESSES covers spine, 6-phase, A–J, LQR, UI, deep modules; README states N3 retention.

### T3 — Domain Pack schemas + fixtures  [Structure]
- **Create:** `business/schemas/domain-manifest.schema.json`, `agent-spec.schema.json`, `learning-log.schema.json`
- **Create:** positive/negative fixtures under `business/fixtures/`
- **Acceptance:** positive fixtures valid; negative fail validation.

### T4 — example_research skeleton  [Structure] (P1)
- **Create:** `business/example_research/{README,manifest,agents/example.researcher,example.reviewer,workflows}`
- **Acceptance:** manifests validate; agents have ALC fields.

### T5 — docs/domain-packs.md + light doc updates  [Structure]
- **Create:** `docs/domain-packs.md`
- **Update:** short Domain Pack note in `structure.md` / `backend.md` / `frontend.md` (or single cross-link section if files huge — minimum: structure.md + docs)
- **Update:** `memory/handoff.md` Wave 0 status
- **Acceptance:** docs reference N1/N2/N3 and inventory CI.

---

## Task group B — Backend: inventory + schema tests + register stub

### T6 — inventory_check.py  [Structure][Backend]
- **Create:** `scripts/business/inventory_check.py`
- **Logic:** Load ROSTER.json; assert 114 dirs; each pack_id has agent_spec with required keys; MAP.md data row count == 114 (or count ROSTER).
- **Exit codes:** 0 pass, 1 fail.
- **Acceptance:** Passes on complete tree; fails if one dir missing (tested via unit).

### T7 — test_domain_pack_inventory.py  [Backend]
- **Create:** `backend/app/tests/unit/test_domain_pack_inventory.py`
- **Action:** Call inventory check functions; assert pass on real tree; assert helper detects missing pack_id.
- **Acceptance:** pytest green.

### T8 — test_domain_pack_schemas.py  [Backend]
- **Create:** `backend/app/tests/unit/test_domain_pack_schemas.py`
- **Action:** Validate fixtures against schemas (stdlib json + simple required-field validator if no jsonschema).
- **Acceptance:** pytest green.

### T9 — register_domain.py stub  [Structure][Backend]
- **Create:** `scripts/business/register_domain.py`
- **Action:** `--manifest path --dry-run` validates domain-manifest schema; prints draft receipt JSON.
- **Acceptance:** succeeds for video + example_research manifests.

### T10 — Do not change runtime.py engine  [Backend]
- **Constraint:** No ALC hard-gate / no lesson agent_id wiring.
- **Acceptance:** Existing unit suite still green.

---

## Task group C — Frontend

### T11 — No FE code required  [Frontend]
- **Action:** None (verify no accidental FE breakage by not touching frontend/).
- **Acceptance:** N/A for Wave 0 feature; FE tests optional if time.

---

## Task group D — Verification & report

### T12 — Run tests  [Backend]
- `python scripts/business/inventory_check.py`
- `python scripts/business/register_domain.py --manifest business/video/manifest.json --dry-run`
- `python -m pytest backend/app/tests/unit/test_domain_pack_inventory.py backend/app/tests/unit/test_domain_pack_schemas.py -q`
- Optionally full unit suite smoke.
- **Acceptance:** All exit 0.

### T13 — completion-report.md  [Structure]
- **Create:** `planning/improvement/wave-0/completion-report.md` with evidence, counts, residual risks.

---

## Explicit breakdown by part

| Part | Tasks |
|------|-------|
| Structure | T1–T5, T6/T9 scripts, T13 |
| Backend | T6–T10, T12 |
| Frontend | T11 (no-op) |

---

## Test matrix (Wave 0)

| Test | Type | Path |
|------|------|------|
| Inventory complete | Unit/script | inventory_check + test_domain_pack_inventory |
| Schema positive/negative | Unit | test_domain_pack_schemas |
| Register dry-run | Script | register_domain.py |
| E1 / unit regression | Unit (optional full) | app/tests/unit |

*End of Phase 3 tasks.*
