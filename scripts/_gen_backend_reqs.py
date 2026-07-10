# Generate planning/backend/nn_*/requirements.md from backend.md decomposition.
from __future__ import annotations

from pathlib import Path

ROOT = Path("planning/backend")
ROOT.mkdir(parents=True, exist_ok=True)

SPECS: list[tuple[str, str, str, str, str, str, str]] = [
    (
        "01",
        "platform-charter-boundaries-and-principles",
        "Platform Charter, Boundaries, and Design Principles",
        "§1 Purpose, §2 Primary Objective, §4 System Boundary, §5 High-Level Architecture, §6 Core Design Principles",
        "structure.md design priorities; backend.md §24.1",
        "None (root)",
        "All BE-02–BE-24",
    ),
    (
        "02",
        "runtime-stack-and-project-scaffold",
        "Runtime Stack and Project Scaffold",
        "§3 Recommended Technology Stack, §9 Recommended Backend Folder Structure, §8.5 Maintainability",
        "structure.md §12.5 Backend entry",
        "BE-01",
        "BE-03+",
    ),
    (
        "03",
        "persistence-control-plane",
        "Persistence Control Plane",
        "§10 Data Model (infra), §18 env DATABASE_URL, §24.3 Postgres runtime_state",
        "structure.md §12.3 Control plane",
        "BE-02",
        "BE-04–BE-22",
    ),
    (
        "04",
        "api-contract-envelope-and-errors",
        "API Contract, Envelope, and Errors",
        "§6.1 API First, §11.1–11.3 Versioning / Response Format / Error Codes",
        "structure.md operator API surface",
        "BE-02, BE-03",
        "All route specs BE-05+",
    ),
    (
        "05",
        "authentication-and-identity",
        "Authentication and Identity",
        "§7.1 Authentication, §11.4 Authentication Endpoints, §16 security auth",
        "structure.md security layer",
        "BE-03, BE-04",
        "BE-06, BE-07, all protected APIs",
    ),
    (
        "06",
        "authorization-and-rbac",
        "Authorization and RBAC",
        "§7.2 Authorization, permission groups, future ABAC notes",
        "structure.md §6–7 permission scopes",
        "BE-05",
        "All resource APIs",
    ),
    (
        "07",
        "users-organizations-and-tenancy",
        "Users, Organizations, and Tenancy",
        "§7.3 User and Organization Management, §10.2–10.3, org settings APIs",
        "structure.md multi-tenant readiness",
        "BE-05, BE-06",
        "All tenant-scoped resources",
    ),
    (
        "08",
        "agent-registry",
        "Agent Registry",
        "§7.4 Agent Registry, §10.4, §11.5, §15 Agent Runtime Design",
        "structure.md §9 agent roster (API registry portion)",
        "BE-06, BE-07",
        "BE-09, BE-11",
    ),
    (
        "09",
        "tool-registry-adapters-and-broker",
        "Tool Registry, Adapters, and Broker",
        "§7.5 Tool Registry, tool_effects as-built, tool permission broker",
        "structure.md §7 tool broker; §12.3 adapters",
        "BE-06, BE-08",
        "BE-11, BE-12",
    ),
    (
        "10",
        "workflow-definition-and-versioning",
        "Workflow Definition and Versioning",
        "§7.6 Workflow Management, §10.5–10.6, §11.6",
        "structure.md §4.1 Workflow DNA",
        "BE-06–BE-09",
        "BE-11, BE-22",
    ),
    (
        "11",
        "workflow-run-execution-engine",
        "Workflow Run Execution Engine",
        "§7.7–7.8 Runs/Steps, §11.7, §12 Workflow Execution Design, idempotency",
        "structure.md §4.2 bounded execution; §2 Intake pre-check",
        "BE-10, BE-12, BE-13",
        "BE-14, BE-17, BE-19–BE-21",
    ),
    (
        "12",
        "governance-policies-and-risk",
        "Governance Policies and Risk",
        "§7.9 (policy engine), §11.11, §13 Governance Design",
        "structure.md §6 risk tiers and policies",
        "BE-06, BE-03",
        "BE-11, BE-13, BE-22",
    ),
    (
        "13",
        "human-approval-gates",
        "Human Approval Gates",
        "§6.4 HITL, §7.9 approvals, §11.8 Approval Endpoints",
        "structure.md §4 human gates; STRUCT-12",
        "BE-12, BE-11",
        "BE-14, BE-24 E1",
    ),
    (
        "14",
        "audit-logging",
        "Audit Logging",
        "§6.5 Audit Everything, §7.13, §10.14, §11.13",
        "structure.md audit log path",
        "BE-03, BE-05",
        "Compliance, FE audit views",
    ),
    (
        "15",
        "knowledge-base-and-retrieval",
        "Knowledge Base and Retrieval",
        "§7.10, §11.9, §14.1–14.2, tiered retrieval as-built",
        "structure.md §3.4 retrieval; STRUCT-09",
        "BE-06, BE-03",
        "BE-11 knowledge steps, BE-18",
    ),
    (
        "16",
        "memory-system",
        "Memory System",
        "§7.11, §11.10, §14.3 Memory Rules",
        "structure.md §3.3 hybrid memory",
        "BE-06, BE-03",
        "BE-08, BE-11",
    ),
    (
        "17",
        "evaluation-system",
        "Evaluation System",
        "§7.12, §11.12, evaluation design links",
        "structure.md §8 evaluation harness",
        "BE-11",
        "BE-20 promote gates, BE-21",
    ),
    (
        "18",
        "process-intelligence",
        "Process Intelligence",
        "§7.14, §11.14, PI disk artifacts",
        "structure.md §2.3 PI layer",
        "BE-11, BE-14",
        "Ops analytics, evolution signals",
    ),
    (
        "19",
        "streaming-health-and-observability",
        "Streaming, Health, and Observability",
        "§7.18 Streaming, §8.4 Observability, §17 Health/Metrics/Logs",
        "structure.md observability / operator proof",
        "BE-04, BE-11",
        "FE realtime, ops readiness",
    ),
    (
        "20",
        "evolution-sandbox-apis",
        "Evolution Sandbox APIs",
        "§7.15, §11.15, §24.3 evolution as-built",
        "structure.md §5 evolution sandbox",
        "BE-10, BE-17, BE-22",
        "BE-21, FE /app/evolution",
    ),
    (
        "21",
        "self-improvement-and-loops",
        "Self-Improvement and Loops",
        "§7.16, §11.16 Improvement / Loop Endpoints",
        "structure.md self-improvement / GEPA-style",
        "BE-11, BE-20, BE-17",
        "FE Improve pipeline, E1",
    ),
    (
        "22",
        "production-dna-safety",
        "Production DNA Safety",
        "§7.17 Production DNA Safety, structure_validators, business:validate",
        "structure.md DNA production safety §12.3",
        "BE-10, BE-12",
        "BE-20 promote, activate path",
    ),
    (
        "23",
        "security-hardening-and-nfr",
        "Security Hardening and Cross-Cutting NFRs",
        "§8 Non-Functional Requirements, §16 Security Design, rate limits, injection",
        "structure.md §7 security controls",
        "BE-05–BE-06, BE-09",
        "All endpoints",
    ),
    (
        "24",
        "testing-strategy-and-operator-path",
        "Testing Strategy and Operator Path",
        "§19 Testing Strategy, §21 MVP, §22 Definition of Done, §24 E1/non-goals",
        "structure.md §11.1 / §12.4–12.5, E1 path",
        "All prior BE specs",
        "Release gate / product bar",
    ),
]


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def load_details() -> dict[str, dict]:
    # Import via file path so script works regardless of PYTHONPATH.
    import importlib.util
    import sys

    data_path = Path(__file__).resolve().parent / "_gen_backend_reqs_data.py"
    spec = importlib.util.spec_from_file_location("_gen_backend_reqs_data", data_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {data_path}")
    # Ensure sibling modules (part2/part3) resolve from scripts/
    scripts_dir = str(Path(__file__).resolve().parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.DETAILS


def render(
    nn: str,
    slug: str,
    title: str,
    backend_map: str,
    structure_map: str,
    depends: str,
    provides: str,
    d: dict,
) -> str:
    spec_id = f"BE-{nn}"
    scope_in = "\n".join(d["scope_in"])
    scope_out = "\n".join(d["scope_out"])
    stk = table(
        ["ID", "Stakeholder", "Need"],
        [[a, b, c] for a, b, c in d["stk"]],
    )
    fr = table(["ID", "Statement (EARS)"], [[a, b] for a, b in d["fr"]])
    perf = table(["ID", "Statement"], [[a, b] for a, b in d["perf"]])
    sec = table(["ID", "Statement"], [[a, b] for a, b in d["sec"]])
    ac = table(["ID", "Criterion"], [[a, b] for a, b in d["ac"]])
    tv = table(["ID", "Protocol", "Type"], [[a, b, c] for a, b, c in d["tv"]])
    tr = table(
        ["backend.md / structure.md", "This spec"],
        [[a, b] for a, b in d["trace"]],
    )
    return f"""# {nn} — {title}

| Field | Value |
|-------|-------|
| Spec ID | `{spec_id}` |
| Source | `backend.md` — {backend_map} |
| Related architecture | {structure_map} |
| Priority order | {nn} |
| Status | Specification |
| Owner | Backend platform |

---

## 1. Scope

### 1.1 In scope
{scope_in}

### 1.2 Out of scope
{scope_out}

### 1.3 System under specification
Generic Swarm Ops **backend API server** (`backend/`), as specified in `backend.md` and constrained by `structure.md`.

---

## 2. Stakeholder Requirements

{stk}

---

## 3. Functional Requirements (EARS)

{fr}

---

## 4. Non-Functional Requirements

### 4.1 Performance
{perf}

### 4.2 Security
{sec}

---

## 5. Acceptance Criteria

{ac}

---

## 6. Integration Dependencies

| Depends on | Provides to |
|------------|-------------|
| {depends} | {provides} |

---

## 7. Test Validation Protocols

{tv}

---

## 8. Traceability

{tr}
"""


def write_readme() -> None:
    lines = [
        "# backend.md — Sub-Functional Specifications",
        "",
        "**Source:** `backend.md` (Backend API Server Requirements, Design, and Implementation Plan)  ",
        "**Architecture SoT:** `structure.md` (§12 implementation mapping)  ",
        "**Path pattern:** `planning/backend/nn_<sub-func-spec>/requirements.md`  ",
        "**Requirement style:** EARS (Easy Approach to Requirements Syntax)  ",
        "**Ordering:** `nn` is the sequential implementation priority (platform foundations → domain APIs → safety wrappers → proof)",
        "",
        "## Execution order",
        "",
        "| nn | Component | backend.md mapping |",
        "|----|-----------|--------------------|",
    ]
    for nn, slug, title, backend_map, *_ in SPECS:
        lines.append(f"| {nn} | {title} | {backend_map} |")
    lines += [
        "",
        "## Dependency sketch",
        "",
        "```text",
        "01 charter",
        " └── 02 stack/scaffold",
        "      └── 03 persistence control plane",
        "           └── 04 API envelope",
        "                ├── 05 authentication ──► 06 RBAC ──► 07 users/orgs",
        "                │                              │",
        "                ├── 08 agents ──► 09 tools/adapters/broker",
        "                ├── 10 workflow definition ──► 11 run engine",
        "                │         ▲                      │",
        "                │         │                      ├─► 12 governance ◄── tiers",
        "                │         │                      ├─► 13 human approvals",
        "                │         │                      ├─► 14 audit",
        "                │         │                      ├─► 15 knowledge/retrieval",
        "                │         │                      ├─► 16 memory",
        "                │         │                      ├─► 17 evaluation",
        "                │         │                      ├─► 18 process intelligence",
        "                │         │                      └─► 19 streaming/health/observability",
        "                ├── 22 production DNA safety ──► 10/11/20",
        "                ├── 20 evolution sandbox ◄── 17,22",
        "                ├── 21 self-improvement ◄── 11,20,17",
        "                ├── 23 security hardening & NFRs (cross-cutting)",
        "                └── 24 testing strategy & operator path (E1 / DoD)",
        "```",
        "",
        "## Document set (per component)",
        "",
        "| File | Role |",
        "|------|------|",
        "| `requirements.md` | EARS requirements + acceptance + test protocols (this decomposition) |",
        "| `design.md` | *(optional next)* SDD design: architecture, ICD, RTM |",
        "| `tasks.md` | *(optional next)* prioritized implementation backlog |",
        "",
        "## Document template (each `requirements.md`)",
        "",
        "1. Document control  ",
        "2. Scope  ",
        "3. Stakeholder requirements  ",
        "4. Functional requirements (EARS)  ",
        "5. Non-functional requirements (performance & security)  ",
        "6. Acceptance criteria  ",
        "7. Integration dependencies  ",
        "8. Test validation protocols  ",
        "9. Traceability to `backend.md` / `structure.md`",
        "",
        "## Recommended global build order",
        "",
        "```text",
        "01 charter → 02 scaffold → 03 persistence → 04 envelope",
        "→ 05 auth → 06 RBAC → 07 users/orgs",
        "→ 08 agents → 09 tools → 10 workflows → 12 governance → 13 approvals",
        "→ 11 run engine → 14 audit → 19 health/stream",
        "→ 15 knowledge → 16 memory → 17 evaluation → 18 PI",
        "→ 22 DNA safety → 20 evolution → 21 self-improvement",
        "→ 23 security/NFR hardening → 24 tests & E1 proof",
        "```",
        "",
        "## EARS patterns used",
        "",
        "| Pattern | Template |",
        "|---------|----------|",
        "| Ubiquitous | The `<system>` shall `<response>`. |",
        "| Event-driven | When `<trigger>`, the `<system>` shall `<response>`. |",
        "| State-driven | While `<state>`, the `<system>` shall `<response>`. |",
        "| Unwanted | If `<unwanted condition>`, then the `<system>` shall `<response>`. |",
        "| Optional feature | Where `<feature is included>`, the `<system>` shall `<response>`. |",
        "",
        "## Related product evidence",
        "",
        "See `status.md`, `backend/README.md`, `structure_scorecard_100.md`, `mark_100_verification.md`, and `planning/gap_analysis_for_structure.md` for as-built status against the parent architecture. This backend decomposition is the **requirements** layer for `backend.md`; it does not replace `structure.md`.",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    details = load_details()
    missing = {nn for nn, *_ in SPECS} - set(details)
    if missing:
        raise SystemExit(f"Missing DETAILS for: {sorted(missing)}")
    write_readme()
    for nn, slug, title, backend_map, structure_map, depends, provides in SPECS:
        d = ROOT / f"{nn}_{slug}"
        d.mkdir(parents=True, exist_ok=True)
        text = render(nn, slug, title, backend_map, structure_map, depends, provides, details[nn])
        (d / "requirements.md").write_text(text, encoding="utf-8")
        print(f"wrote {d / 'requirements.md'}")
    print(f"done: {len(SPECS)} specs + README")


if __name__ == "__main__":
    main()
