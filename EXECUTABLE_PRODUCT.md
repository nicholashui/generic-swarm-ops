# Executable product status

**Date:** 2026-07-13  
**Status:** **EXECUTABLE** for the operator control plane + one video Domain Pack workflow path  
**Host:** `C:\Project\generic-swarm-ops`  
**App name:** generic-swarm-ops  

---

## What “executable” means here

| Proven | Not claimed |
|--------|-------------|
| Backend API boots (FastAPI `app.main:app`) | Live Sora/Veo/Runway media vendors |
| Health / live / ready endpoints return usable JSON | Every A–J DNA `production_ready: true` |
| E1 operator path: login → list → create agent → run workflow → approve gates → complete → improve | Full Discover / production-scale FE gallery |
| Video pack: inventory 114 + corpus standalone 325 | True 100 on all 114 agent scorecards |
| Video DNA **viral-hook** run end-to-end on host runtime (stubs + human package gate) | Multi-week canary/GA of all special skills |
| Knowledge-standalone (no va-agent-swarm primary dependency) | Second LangGraph control plane |

---

## Proven runnable paths

### 1) Control plane (E1)

**Test (shipped):** `backend/app/tests/e2e/test_e1_operator_path.py`  

Path: `GET /api/v1/health/ready` → `POST /api/v1/auth/login` → list workflows/agents/approvals → create agent → run `wf_customer_onboarding_v12` → approve gates → complete → improve metrics.

### 2) Video Domain Pack workflow (viral-hook)

**Test (shipped):** `backend/app/tests/unit/test_video_spine_e2e.py::test_viral_hook_spine_run_with_gate_and_alc`  

Path:

1. Register `business/video/manifest.json`  
2. Activate spine agents (`video.orchestrator`, planner, director, screenwriter, webresearch, aiqaconsistency, producer) with ALC + allow-listed tools  
3. Load DNA `business/video/workflows/wf_video_arch_a_viral_hook_v1.dna.json`  
4. Start run → dispatch → human approve package/publish gate → **completed**  
5. Reflect → stored ALC lessons  

**Tools used (allow-listed stubs, intentional):**  
`audit_log_writer`, `video_script_format`, `video_media_gen_stub`, `video_qc_stub`, `video_package_stub`

### 3) Integrity required for execution

```bash
python scripts/business/inventory_check.py
# INVENTORY PASS count=114 n3=complete
python scripts/business/check_video_corpus_standalone.py
# STANDALONE PASS manifest=325 specs=114
```

---

## How to launch

### Backend (primary control plane)

```bash
cd C:\Project\generic-swarm-ops\backend
python -m pip install -e .
# Optional: set DATABASE_URL for Postgres (see docs/postgres-runbook.md)
# Without Postgres, JSON-file store remains ready for local demo.
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

| Endpoint | Expect |
|----------|--------|
| `GET /api/v1/health` | `{"status":"ok",...}` |
| `GET /api/v1/health/live` | `{"status":"alive",...}` |
| `GET /api/v1/health/ready` | `status` = `ready` or `degraded`; `dependencies.database` = `postgres` or `json-file` |

**Demo login (local):** `admin@example.com` / `admin-password` (see `backend/README.md`).

### Frontend (optional ops console)

```bash
cd C:\Project\generic-swarm-ops\frontend
# follow frontend README; point API at backend
```

### One-command product check

```bash
cd C:\Project\generic-swarm-ops
python scripts/business/check_executable_product.py
```

Runs inventory + standalone + health via TestClient + E1 + video spine tests.

### Targeted tests

```bash
cd C:\Project\generic-swarm-ops\backend
python -m pytest app/tests/e2e/test_e1_operator_path.py app/tests/unit/test_video_spine_e2e.py -q
```

### Video brief → DNA recommend (selection helper)

```bash
python scripts/business/recommend_video_workflow.py "15s viral TikTok hook"
# Then run the recommended dna_id via API / runtime (viral-hook path proven above)
```

---

## Architecture (executable slice)

```text
Operator / TestClient / uvicorn
        │
        ▼
FastAPI app.main  ── health, auth, workflows, runs, approvals
        │
        ▼
runtime  ── DNA steps, tool adapters, ALC, audit
        │
        ├── ops seed workflows (e.g. customer onboarding)
        └── video Domain Pack (business/video/)
                agents (114) + workflows/*.dna.json + corpus (325)
```

N1: video business logic stays in the pack; host executes DNA + tools + gates only.

---

## Residuals (explicit non-claims)

1. Live external media generation APIs  
2. Full deep DNA for C–J / feature film production_ready  
3. Full Discover / production-scale product FE  
4. Fleet true-100 agent migration scores  
5. Cloud/k8s production packaging beyond local executable demo  

---

## Related

- Migration knowledge DoD: `MIGRATION_COMPLETE.md`  
- Backend ops: `backend/README.md`, `docs/postgres-runbook.md`  
- Video pack: `business/video/README.md`  
- E1 checklist: `reviews/e1_operator_checklist.md`  

*End executable product status.*
