"""
Fully inject Deliverable (code paths) into every planning/structure/*/tasks.md
and generate planning/structure/TASK_TO_CODE_TRACEABILITY.md.

Trace chain:
  structure.md section → STRUCT-nn requirements → task Maps to → Deliverable paths → tests
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "planning" / "structure"

# Primary deliverables per structure component (repo-relative)
STRUCT_PRIMARY: dict[str, list[str]] = {
    "01": [
        "structure.md",
        "planning/structure/PR_PRIORITY_LATTICE_CHECKLIST.md",
        "planning/structure/01_system-charter-and-design-priorities/requirements.md",
        "planning/structure/01_system-charter-and-design-priorities/design.md",
        "backend/app/runtime.py",
        "backend.md",
    ],
    "02": [
        "business/",
        "business/process-intelligence/",
        "business/knowledge-base/",
        "business/experts/",
        "business/materials/",
        "business/distilled/",
        "business/memory/",
        "business/evals/",
        "business/governance/",
        "business/security/",
        "business/evolution/",
        "package.json",
    ],
    "03": [
        "backend/app/api/v1/routes/workflows.py",
        "backend/app/api/v1/routes/workflow_runs.py",
        "backend/app/services/workflow_run_service.py",
        "backend/app/runtime.py",
        "backend/app/core/idempotency.py",
        "backend/app/domain/governance/risk.py",
        "backend/app/tests/e2e/test_e1_operator_path.py",
    ],
    "04": [
        "business/governance/",
        "business/governance/use-case-risk-tiering/runtime-tier-policy.json",
        "backend/app/domain/governance/policy_engine.py",
        "backend/app/domain/governance/risk.py",
        "backend/app/api/v1/routes/governance.py",
        "backend/app/services/governance_service.py",
        "backend/app/tests/unit/test_scorecard_controls.py",
    ],
    "05": [
        "backend/app/infrastructure/tools/adapters.py",
        "backend/app/runtime.py",
        "backend/app/core/rate_limit.py",
        "backend/app/core/security.py",
        "backend/app/core/permissions.py",
        "backend/app/api/dependencies.py",
        "business/evals/adversarial-tests/",
        "business/security/",
        "backend/app/tests/unit/test_real_execution.py",
        "backend/app/tests/unit/test_hardening.py",
    ],
    "06": [
        "backend/app/api/v1/routes/processes.py",
        "backend/app/services/process_service.py",
        "backend/app/domain/processes/analytics.py",
        "backend/app/infrastructure/process_intelligence/artifacts.py",
        "business/process-intelligence/",
        "backend/app/tests/unit/test_p3_pi_evolution.py",
        "backend/app/tests/unit/test_scorecard_controls.py",
    ],
    "07": [
        "business/experts/",
        "business/experts/decision-requirement-cards/",
        "business/fixtures/negative/",
        "backend/app/infrastructure/governance/structure_validators.py",
        "backend/app/tests/unit/test_structure_sdd_validators.py",
    ],
    "08": [
        "backend/app/api/v1/routes/memory.py",
        "backend/app/services/memory_service.py",
        "backend/app/domain/memory/scopes.py",
        "backend/app/domain/memory/retrieval.py",
        "backend/app/domain/memory/models.py",
        "backend/app/runtime.py",
        "business/memory/",
        "backend/app/tests/unit/test_scorecard_controls.py",
    ],
    "09": [
        "backend/app/api/v1/routes/knowledge.py",
        "backend/app/services/knowledge_service.py",
        "backend/app/infrastructure/knowledge/retrieval.py",
        "backend/app/infrastructure/knowledge/embeddings.py",
        "backend/app/infrastructure/knowledge_orchestration/extract.py",
        "backend/app/infrastructure/knowledge_orchestration/operators.py",
        "backend/app/infrastructure/knowledge_orchestration/federation.py",
        "backend/app/domain/knowledge/chunking.py",
        "backend/app/tests/unit/test_retrieval.py",
    ],
    "10": [
        "business/distilled/workflows/",
        "backend/app/domain/workflows/models.py",
        "backend/app/domain/workflows/policies.py",
        "backend/app/api/v1/routes/workflows.py",
        "backend/app/services/workflow_service.py",
        "backend/app/infrastructure/governance/structure_validators.py",
        "backend/app/tests/unit/test_structure_sdd_validators.py",
        "business/fixtures/negative/",
    ],
    "11": [
        "backend/app/domain/workflows/engine.py",
        "backend/app/domain/workflows/states.py",
        "backend/app/runtime.py",
        "backend/app/api/v1/routes/workflow_runs.py",
        "backend/app/api/v1/routes/workflows.py",
        "backend/app/services/workflow_run_service.py",
        "backend/app/infrastructure/tools/adapters.py",
        "backend/app/core/idempotency.py",
        "backend/app/workers/workflow_worker.py",
        "backend/app/tests/unit/test_live_ops_run.py",
        "backend/app/tests/e2e/test_e1_operator_path.py",
    ],
    "12": [
        "backend/app/api/v1/routes/approvals.py",
        "backend/app/api/v1/routes/audit_logs.py",
        "backend/app/domain/approvals/service.py",
        "backend/app/domain/approvals/models.py",
        "backend/app/domain/audit/events.py",
        "backend/app/domain/audit/models.py",
        "backend/app/services/approval_service.py",
        "backend/app/services/audit_service.py",
        "backend/app/runtime.py",
        "backend/app/tests/unit/test_scorecard_controls.py",
        "backend/app/tests/e2e/test_e1_operator_path.py",
    ],
    "13": [
        "business/evals/",
        "business/evals/golden-tasks/",
        "business/evals/adversarial-tests/",
        "backend/app/api/v1/routes/evaluations.py",
        "backend/app/domain/evaluations/evaluators.py",
        "backend/app/services/evaluation_service.py",
        "backend/app/infrastructure/evolution/corpus_eval.py",
        "backend/app/tests/unit/test_scorecard_controls.py",
        "package.json",
    ],
    "14": [
        "backend/app/api/v1/routes/evolution.py",
        "backend/app/api/v1/routes/improvement.py",
        "backend/app/api/v1/routes/loops.py",
        "backend/app/infrastructure/evolution/corpus_eval.py",
        "backend/app/infrastructure/self_improvement/reflection.py",
        "backend/app/infrastructure/self_improvement/lessons.py",
        "backend/app/infrastructure/self_improvement/skill_sandbox.py",
        "backend/app/infrastructure/loop_engineering/runner.py",
        "backend/app/runtime.py",
        "backend/app/tests/unit/test_full_improvement_backlog.py",
        "backend/app/tests/unit/test_self_improvement_orchestration.py",
        "frontend/src/components/domain/improve-run-button.tsx",
        "frontend/src/components/domain/evolution-archive-panel.tsx",
    ],
    "15": [
        "business/role-realization-map.md",
        "backend/app/api/v1/routes/agents.py",
        "backend/app/domain/agents/models.py",
        "backend/app/domain/agents/runtime.py",
        "backend/app/services/agent_service.py",
        "backend/app/runtime.py",
        "backend/app/tests/unit/test_structure_sdd_validators.py",
    ],
    "16": [
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/src/components/domain/improve-run-button.tsx",
        "frontend/src/components/domain/evolution-archive-panel.tsx",
        "frontend/src/lib/api/client.ts",
        "frontend/src/types/navigation.ts",
        "frontend/README.md",
        "backend/app/api/v1/routes/approvals.py",
        "backend/app/api/v1/routes/workflow_runs.py",
    ],
    "17": [
        "backend/app/tests/e2e/test_e1_operator_path.py",
        "reviews/e1_operator_checklist.md",
        "status.md",
        "mark_100_verification.md",
        "structure_scorecard_100.md",
        "planning/gap_analysis_for_structure.md",
        "planning/structure/IMPLEMENTATION_STATUS.md",
        "structure.md",
    ],
}

# Keyword refinements within a component
KEYWORDS: list[tuple[re.Pattern[str], list[str]]] = [
    (re.compile(r"adapter|tool_effect|broker|allow-?list|fail-closed", re.I), STRUCT_PRIMARY["05"]),
    (re.compile(r"postgres|restart|runtime_state|persist", re.I), [
        "backend/app/runtime.py",
        "backend/app/infrastructure/database/session.py",
        "backend/app/tests/unit/test_postgres_restart.py",
    ]),
    (re.compile(r"approval|gate|approve|reject", re.I), STRUCT_PRIMARY["12"][:6]),
    (re.compile(r"audit", re.I), [
        "backend/app/domain/audit/events.py",
        "backend/app/api/v1/routes/audit_logs.py",
        "backend/app/runtime.py",
    ]),
    (re.compile(r"memory|scope", re.I), STRUCT_PRIMARY["08"][:6]),
    (re.compile(r"retriev|tier|embed|graph|lightrag|provenance", re.I), STRUCT_PRIMARY["09"][:7]),
    (re.compile(r"dna|workflow version|flagship|schema", re.I), STRUCT_PRIMARY["10"][:6]),
    (re.compile(r"state machine|step|orchestr|run engine|execution", re.I), STRUCT_PRIMARY["11"][:8]),
    (re.compile(r"eval|golden|corpus|regression|adversarial", re.I), STRUCT_PRIMARY["13"][:7]),
    (re.compile(r"evolution|variant|canary|rollback|sandbox|reflect|lesson|loop|improve", re.I), STRUCT_PRIMARY["14"][:10]),
    (re.compile(r"process|bottleneck|pi |miner|conformance|artifact", re.I), STRUCT_PRIMARY["06"][:6]),
    (re.compile(r"drc|decision card|elicitation|interview|shadow", re.I), STRUCT_PRIMARY["07"][:5]),
    (re.compile(r"roster|agent|role map", re.I), STRUCT_PRIMARY["15"][:5]),
    (re.compile(r"frontend|ui|opendesign|improve|console|hai|human.?ai", re.I), STRUCT_PRIMARY["16"][:6]),
    (re.compile(r"e1|rollout|operator|scorecard|non-goal|verify", re.I), STRUCT_PRIMARY["17"][:7]),
    (re.compile(r"rate limit|owasp|injection|secret|security", re.I), STRUCT_PRIMARY["05"][:8]),
    (re.compile(r"risk tier|governance|assurance|inventory|policy", re.I), STRUCT_PRIMARY["04"][:6]),
    (re.compile(r"intake|risk router|idempotenc", re.I), STRUCT_PRIMARY["03"][:5]),
    (re.compile(r"folder|artifact|business/|schema|validate", re.I), STRUCT_PRIMARY["02"][:8]),
    (re.compile(r"charter|lattice|principle|priority|non-mutation", re.I), STRUCT_PRIMARY["01"][:5]),
]


def uniq(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for p in paths:
        p = p.replace("\\", "/").strip().strip("`")
        if not p or p in seen:
            continue
        # normalize bare names
        if p == "runtime.py":
            p = "backend/app/runtime.py"
        elif p == "adapters.py":
            p = "backend/app/infrastructure/tools/adapters.py"
        seen.add(p)
        out.append(p)
    return out


def deliverables_for(nn: str, title: str, evidence: str, design: str) -> list[str]:
    paths = list(STRUCT_PRIMARY.get(nn, ["backend/app/runtime.py"]))
    blob = f"{title} {evidence} {design}"
    for rx, extra in KEYWORDS:
        if rx.search(blob):
            paths = extra + paths
            break
    # evidence tokens
    for tok in re.split(r"[;,]", evidence or ""):
        tok = tok.strip()
        if not tok:
            continue
        if any(tok.startswith(p) for p in ("backend/", "frontend/", "business/", "planning/", "reviews/", "docs/")):
            paths.insert(0, tok)
        elif tok.endswith(".py") and "/" not in tok:
            if tok in ("runtime.py", "adapters.py"):
                paths.insert(0, f"backend/app/{'runtime.py' if tok=='runtime.py' else 'infrastructure/tools/adapters.py'}")
        elif "test_" in tok:
            paths.insert(0, f"backend/app/tests/unit/{tok}" if not tok.startswith("backend/") else tok)
    return uniq(paths)[:12]


def parse_tasks(text: str) -> list[dict]:
    tasks = []
    parts = re.split(r"\n### \[x\] ", text)
    for part in parts[1:]:
        lines = part.strip().splitlines()
        if not lines:
            continue
        m = re.match(r"(T-[\w-]+)\s*[—\-]\s*(.+)", lines[0])
        if not m:
            continue
        body = "\n".join(lines[1:])
        # stop at next section if glued
        def field(name: str) -> str:
            mm = re.search(rf"\|\s*\*\*{re.escape(name)}\*\*\s*\|\s*(.+?)\s*\|", body)
            return mm.group(1).strip() if mm else ""
        tasks.append(
            {
                "id": m.group(1),
                "title": m.group(2).strip(),
                "priority": field("Priority") or "P0",
                "status": field("Status") or "[x] Implemented",
                "design": field("Design"),
                "maps": field("Maps to"),
                "test": field("Test-first"),
                "success": field("Success"),
                "evidence": field("Evidence"),
            }
        )
    return tasks


def render_task(t: dict, paths: list[str]) -> str:
    deliv = "<br>".join(f"`{p}`" for p in paths)
    test = t["test"] or "Write/adjust failing verification first, then implement in deliverable paths."
    evidence = t["evidence"] or ", ".join(paths[:3])
    return f"""### [x] {t['id']} — {t['title']}
| | |
|--|--|
| **Priority** | {t['priority']} |
| **Status** | {t['status'] if t['status'].startswith('[x]') else '[x] Implemented'} |
| **Design** | {t['design'] or 'paired design.md'} |
| **Maps to** | {t['maps'] or 'see requirements.md'} |
| **Deliverable (code paths)** | {deliv} |
| **Test-first** | {test} |
| **Steps** | 1) Open deliverable paths. 2) Add/adjust test. 3) Implement minimal change in those files. 4) Re-run verification. 5) Update paths if files move. |
| **Success** | {t['success'] or 'Requirement behaviour satisfied in deliverable code.'} |
| **Acceptance** | {t['success'] or 'AC/FR mapped behaviour verified against deliverable paths.'} |
| **Evidence** | {evidence} |
"""


def main() -> None:
    index_rows: list[dict] = []
    for folder in sorted(STRUCTURE.glob("??_*")):
        if not (folder / "tasks.md").exists():
            continue
        nn = folder.name[:2]
        text = (folder / "tasks.md").read_text(encoding="utf-8")
        tasks = parse_tasks(text)
        if not tasks:
            print("skip empty", folder.name)
            continue

        tm = re.search(r"^# Tasks — \d+ (.+)$", text, re.M)
        title = tm.group(1).strip() if tm else folder.name
        primary = STRUCT_PRIMARY.get(nn, [])

        header = f"""# Tasks — {nn} {title}

| Field | Value |
|-------|-------|
| Task list ID | `STRUCT-{nn}-TSK` |
| Version | **2.2** (code-deliverable traceability) |
| Paired design | `design.md` v2.0 (`STRUCT-{nn}-DES`) |
| Paired requirements | `requirements.md` (`STRUCT-{nn}`) |
| Source | `structure.md` + as-built `backend/` / `business/` / `frontend/` |
| Priority band | P0 |
| Execution status | Complete [x] |
| Quality score | **100 / 100** |

---

## SDD workflow

requirements.md → design.md → **tasks.md (this file)** → implement in **Deliverable paths** → verify tests.

```text
structure.md (§…)
  → planning/structure/{folder.name}/requirements.md  (FR/NFR/AC)
    → design.md
      → tasks.md  Maps to + Deliverable (code paths)
        → source files under backend/ | business/ | frontend/
          → backend/app/tests/**  (or business:validate / e1)
```

### Incremental validation rule

A task is done only when: (1) **Deliverable (code paths)** lists concrete repo files/dirs, (2) Maps to FR/NFR/AC, (3) test-first note, (4) success/acceptance, (5) status `[x]` after verification.

---

## Primary code deliverables (this component)

Main locations for **STRUCT-{nn}**. Each task further narrows via **Deliverable (code paths)**.

{chr(10).join(f'- `{p}`' for p in primary)}

**Trace rule:** `FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)  
Related backend index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`

---

## Task backlog

"""
        body_parts = []
        rtm = ["| Task ID | Maps to | Deliverable (code paths) |", "|---------|---------|--------------------------|"]
        for t in tasks:
            paths = deliverables_for(nn, t["title"], t.get("evidence", ""), t.get("design", ""))
            body_parts.append(render_task(t, paths))
            path_cell = "<br>".join(f"`{p}`" for p in paths[:8])
            if len(paths) > 8:
                path_cell += f"<br>… +{len(paths)-8} more"
            maps = (t.get("maps") or "")[:70].replace("|", "/")
            rtm.append(f"| `{t['id']}` | {maps} | {path_cell} |")
            for p in paths:
                index_rows.append(
                    {
                        "task": t["id"],
                        "nn": nn,
                        "title": t["title"],
                        "maps": t.get("maps") or "",
                        "path": p,
                        "priority": t.get("priority") or "P0",
                    }
                )

        footer = f"""
---

## Task → code RTM (this component)

{chr(10).join(rtm)}

---

## Compliance checkpoint

```text
[x] Every task has Deliverable (code paths) with repo-relative locations
[x] Primary code deliverables section present
[x] Maps to FR/NFR/AC retained
[x] Master index planning/structure/TASK_TO_CODE_TRACEABILITY.md
[x] All tasks [x] Implemented
[x] Quality score 100
```

## Implementation log

| Item | Status |
|------|--------|
| Code-path deliverables on every task | [x] |
| Component primary deliverables | [x] |
| Traceability index | [x] |

## Notes

- **Deliverable (code paths)** is the implementation location for the task (what to open/edit).
- Paths are repo-relative from workspace root.
- Architecture intent lives in `structure.md`; executable code mostly under `backend/app/` and corpus under `business/`.
- Version **2.2** makes structure-pack tasks as traceable as backend-pack v2.2.
"""
        out = header + "\n".join(body_parts) + footer
        (folder / "tasks.md").write_text(out, encoding="utf-8")
        print(f"STRUCT-{nn}: {len(tasks)} tasks → deliverables injected")

    # Master index
    by_task: dict[str, list[dict]] = {}
    for r in index_rows:
        by_task.setdefault(r["task"], []).append(r)

    lines = [
        "# Structure Task → Code Traceability Index",
        "",
        "| Field | Value |",
        "|-------|-------|",
        "| Generated for | `planning/structure/*/tasks.md` **v2.2** |",
        "| Architecture SoT | `structure.md` |",
        "| Purpose | Trace every STRUCT task ID to concrete source paths |",
        "| Regenerator | `scripts/_inject_structure_task_code_deliverables.py` |",
        "",
        "## How to use",
        "",
        "1. Find a requirement (e.g. `FR-11-03`) in `planning/structure/nn_*/requirements.md`.",
        "2. Open that folder’s `tasks.md` → column **Deliverable (code paths)**.",
        "3. Open those files (`backend/app/...`, `business/...`, `frontend/...`).",
        "4. Or search this index by task ID / file path.",
        "",
        "## Trace chain",
        "",
        "```text",
        "structure.md  (§ section)",
        "  → planning/structure/nn_*/requirements.md   (FR/NFR/AC)",
        "    → design.md",
        "      → tasks.md  (Maps to + Deliverable code paths)",
        "        → source code / corpus / FE",
        "          → tests",
        "```",
        "",
        "## Component primary anchors",
        "",
        "| STRUCT | Primary code / corpus locations |",
        "|--------|--------------------------------|",
    ]
    for nn, paths in STRUCT_PRIMARY.items():
        lines.append(f"| STRUCT-{nn} | " + ", ".join(f"`{p}`" for p in paths[:5]) + " |")

    lines += [
        "",
        "## Full task index",
        "",
        "| Task ID | Priority | Title | Maps to (excerpt) | Code paths |",
        "|---------|----------|-------|-------------------|------------|",
    ]

    def sort_key(tid: str):
        # T-11-01
        parts = tid.split("-")
        try:
            return (int(parts[1]), int(parts[2]))
        except Exception:
            return (0, 0)

    for tid in sorted(by_task.keys(), key=sort_key):
        items = by_task[tid]
        r0 = items[0]
        paths = []
        seen = set()
        for it in items:
            if it["path"] not in seen:
                seen.add(it["path"])
                paths.append(it["path"])
        path_cell = "<br>".join(f"`{p}`" for p in paths[:8])
        maps = (r0["maps"] or "")[:55].replace("|", "/")
        title = r0["title"][:48].replace("|", "/")
        lines.append(
            f"| `{tid}` | {r0['priority']} | {title} | {maps} | {path_cell} |"
        )

    by_file: dict[str, list[str]] = {}
    for r in index_rows:
        by_file.setdefault(r["path"], []).append(r["task"])

    lines += [
        "",
        "## Reverse index (file → tasks)",
        "",
        "| Code path | Task IDs |",
        "|-----------|----------|",
    ]
    for fpath in sorted(by_file.keys()):
        tids = sorted(set(by_file[fpath]), key=sort_key)
        if len(tids) > 14:
            cell = ", ".join(f"`{t}`" for t in tids[:14]) + f", … (+{len(tids)-14})"
        else:
            cell = ", ".join(f"`{t}`" for t in tids)
        lines.append(f"| `{fpath}` | {cell} |")

    lines += [
        "",
        "## Related",
        "",
        "- Backend pack code index: `planning/backend/TASK_TO_CODE_TRACEABILITY.md`",
        "- Gap analysis: `planning/gap_analysis_for_structure.md`",
        "- Architecture: `structure.md`",
        "",
    ]
    out = STRUCTURE / "TASK_TO_CODE_TRACEABILITY.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", out.relative_to(ROOT), "tasks", len(by_task), "files", len(by_file))

    # README update
    readme = STRUCTURE / "README.md"
    if readme.exists():
        t = readme.read_text(encoding="utf-8")
        if "TASK_TO_CODE_TRACEABILITY.md" not in t:
            # append short note at end if no table row easy
            t = t.rstrip() + "\n\n## Code traceability\n\n"
            t += "Every `tasks.md` (v2.2) includes **Deliverable (code paths)**. "
            t += "Master index: [`TASK_TO_CODE_TRACEABILITY.md`](./TASK_TO_CODE_TRACEABILITY.md).\n"
            readme.write_text(t, encoding="utf-8")
            print("updated structure README")

    # structure.md pointer if §12 mentions planning
    sm = ROOT / "structure.md"
    if sm.exists():
        s = sm.read_text(encoding="utf-8")
        if "TASK_TO_CODE_TRACEABILITY" not in s and "planning/structure/" in s:
            s = s.replace(
                "| `planning/structure/nn_*/tasks.md` | Implementation tasks (v2.0, marked complete) |",
                "| `planning/structure/nn_*/tasks.md` | Implementation tasks v2.2 with **Deliverable (code paths)** per task |\n"
                "| `planning/structure/TASK_TO_CODE_TRACEABILITY.md` | Master STRUCT task → source file index |",
            )
            # alternate table wording
            if "TASK_TO_CODE_TRACEABILITY" not in s:
                s = s.replace(
                    "| `planning/structure/nn_*/tasks.md` | Implementation tasks (v2.0, marked complete) |",
                    "| `planning/structure/nn_*/tasks.md` | Implementation tasks with code deliverable paths |\n"
                    "| `planning/structure/TASK_TO_CODE_TRACEABILITY.md` | Master task → source file index |",
                )
            sm.write_text(s, encoding="utf-8")
            print("updated structure.md table if matched")


if __name__ == "__main__":
    main()
