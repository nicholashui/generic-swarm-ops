# Run All Improvement Waves (0 → 5)

**Purpose:** Single agent prompt to execute, verify, and auto-advance through every wave in `improvements.md`.  
**Related:** `improvement_prompt.txt`, `improvements.md` v1.0, `planning/improvement/README.md`

---

## How to use

Paste the **Agent prompt** block below into a coding agent session (or: *“Execute `run_all_improvement.md`”*).

Work only inside **generic-swarm-ops** (`genetic-swarm-ops` is a typo path).

---

## Agent prompt

```text
You are a senior production-grade SDD coding agent working strictly inside the generic-swarm-ops repository.

Read and follow:
- improvement_prompt.txt (mandatory full SDD flow)
- improvements.md v1.0 (source of truth for Waves 0–5)
- Cross-refs: adoption.md (N1/N2/N3), repo_compare.md, planning/improvement/README.md
- This file: run_all_improvement.md

## Mission (chained auto-advance)

Execute **Waves 0 → 5 in order**. For **each wave** do:

1. **SDD** under `planning/improvement/wave-N/`:
   - Phase 1: requirements.md (Structure / Backend / Frontend)
   - Phase 2: design.md
   - Phase 3: tasks.md
2. **Implement** the tasks for that wave only (do not pull in later-wave scope early).
3. **Verify** that wave’s acceptance criteria with real commands (inventory + relevant pytest).
4. **Write/update** `completion-report.md` with evidence (command outputs, counts, AC table).
5. **Update** `memory/handoff.md` with wave PASS/FAIL before starting the next wave.
6. **Gate:** only if verify PASSES, automatically start the next wave. If verify FAILS, STOP, report failures, and wait for instructions. Do not skip a failed wave.

## Wave order & exit focus

| Wave | Focus | Minimum verify |
|------|--------|----------------|
| 0 | Catalog, schemas, inventory script, register dry-run | inventory PASS 114; domain pack unit tests |
| 1 | ALC + domain register API + isolation + FE domain shell | ALC tests green; inventory still 114 |
| 2 | Spine + viral-hook DNA, video stubs, spine E2E | test_video_spine_e2e green; inventory 114 |
| 3 | Coevolution, lesson utility, LQR evals | test_wave3_coevolution green; inventory 114 |
| 4 | Multi-pack load, security, runbook, third pack | test_wave4_multipack green; inventory 114 |
| 5 | Full N3 roster + process wiring + CI | test_wave5_n3_roster green; inventory `n3=complete` |

### Suggested verify commands (per wave)

```bash
# Always (every wave)
python scripts/business/inventory_check.py

# Wave 0
cd backend && python -m pytest app/tests/unit/test_domain_pack_inventory.py app/tests/unit/test_domain_pack_schemas.py -q

# Wave 1
cd backend && python -m pytest app/tests/unit/test_alc_and_domains.py -q

# Wave 2
cd backend && python -m pytest app/tests/unit/test_video_spine_e2e.py -q

# Wave 3
cd backend && python -m pytest app/tests/unit/test_wave3_coevolution.py -q

# Wave 4
cd backend && python -m pytest app/tests/unit/test_wave4_multipack.py -q

# Wave 5
cd backend && python -m pytest app/tests/unit/test_wave5_n3_roster.py -q
```

After **Wave 5 verify PASS**, run full regression:

```bash
python scripts/business/inventory_check.py
cd backend && python -m pytest app/tests/unit -q
```

Then produce a short **final chain report** listing each wave PASS/FAIL + final suite/inventory.

## Rules

- Output all SDD docs under `planning/improvement/wave-N/` only.
- Cover Structure / Backend / Frontend in every SDD phase.
- Non-negotiables: N1 (video logic in pack), N2 (universal host), N3 (never drop 114 agents).
- Sandbox-only evolution; never auto-promote.
- Protect E1 / existing unit suite; fix regressions before advancing.
- Prefer reusing existing patterns.
- **If a wave is already implemented:** re-verify first; only re-implement gaps, then advance (do not rebuild from scratch unless broken).
- Work in generic-swarm-ops only.
- Do not stop between waves unless a gate fails.

## Start now

Begin with **Wave 0 Phase 1 (Requirements)** (or Wave 0 verify-first if artifacts already exist). Then implement/fill gaps → verify → auto-advance through Wave 5.
```

---

## Shorter variant (tight context)

```text
Follow improvement_prompt.txt + improvements.md + run_all_improvement.md.
Auto-run Waves 0→5 in order: for each wave full SDD under planning/improvement/wave-N/ → implement (or fill gaps) → verify with inventory+pytest → completion-report + handoff → only if PASS, next wave. Stop on first failure. Prefer verify-and-fill-gaps if already done. Start Wave 0 now; finish with Wave 5 verify + full unit suite + final chain report.
```

---

## Notes

1. Completion-report pytest counts are **snapshots at wave exit**; suite size grows over later waves.
2. Live inventory after Wave 5 expects: `INVENTORY PASS count=114 n3=complete`.
3. Wave status index: `planning/improvement/README.md`.
