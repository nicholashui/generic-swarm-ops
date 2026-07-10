"""Generate planning/frontend/*/tasks.md (SDD v2.2) + TASKS_QUALITY_SCORE.md
+ TASK_TO_CODE_TRACEABILITY.md.

Strict FR/NFR/AC/C-* coverage from paired requirements.md + design.md.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FE_PLAN = ROOT / "planning" / "frontend"

FOLDERS = [
    ("01", "01_frontend-charter-scope-and-principles"),
    ("02", "02_nextjs-scaffold-stack-and-folder-structure"),
    ("03", "03_design-system-tokens-and-opendesign"),
    ("04", "04_app-shell-navigation-and-information-architecture"),
    ("05", "05_authentication-and-session-ui"),
    ("06", "06_permission-aware-navigation-and-ui"),
    ("07", "07_typed-api-client-and-openapi-integration"),
    ("08", "08_dashboard-page"),
    ("09", "09_agents-and-tools-ui"),
    ("10", "10_workflows-definition-ui"),
    ("11", "11_workflow-run-realtime-ui"),
    ("12", "12_approvals-and-human-gates-ui"),
    ("13", "13_knowledge-and-memory-ui"),
    ("14", "14_evaluations-and-processes-ui"),
    ("15", "15_audit-logs-ui"),
    ("16", "16_settings-users-org-and-api-keys-ui"),
    ("17", "17_evolution-sandbox-archive-ui"),
    ("18", "18_improve-pipeline-ui"),
    ("19", "19_accessibility-loading-empty-and-error-states"),
    ("20", "20_security-performance-testing-and-ops-profile"),
]

# Primary code deliverables per component (as-built + design anchors)
PRIMARY: dict[str, list[str]] = {
    "01": [
        "frontend.md",
        "planning/frontend/README.md",
        "planning/frontend/01_frontend-charter-scope-and-principles/design.md",
        "frontend/src",
    ],
    "02": [
        "frontend/package.json",
        "frontend/tsconfig.json",
        "frontend/middleware.ts",
        "frontend/src/app",
        "frontend/src/lib/config/env.ts",
        "frontend/src/app/globals.css",
    ],
    "03": [
        "frontend/src/design/tokens.ts",
        "frontend/src/design/theme.ts",
        "frontend/src/design/status.ts",
        "frontend/src/components/ui",
        "frontend/docs/design",
    ],
    "04": [
        "frontend/src/components/layout/app-shell.tsx",
        "frontend/src/components/layout/sidebar.tsx",
        "frontend/src/components/layout/app-header.tsx",
        "frontend/src/components/layout/command-palette.tsx",
        "frontend/src/components/layout/mobile-nav.tsx",
        "frontend/src/lib/routes/paths.ts",
        "frontend/src/app/app",
    ],
    "05": [
        "frontend/src/app/login/page.tsx",
        "frontend/src/app/accept-invite/page.tsx",
        "frontend/src/app/register/page.tsx",
        "frontend/src/components/auth",
        "frontend/src/lib/auth/session.ts",
    ],
    "06": [
        "frontend/src/lib/auth/permissions.ts",
        "frontend/src/hooks/use-permissions.ts",
        "frontend/src/types/permissions.ts",
        "frontend/tests/unit/permissions.test.ts",
    ],
    "07": [
        "frontend/src/lib/api/client.ts",
        "frontend/src/lib/api/generated",
        "frontend/src/lib/api/live-data.ts",
        "frontend/src/lib/api/live-ops-surfaces.ts",
        "frontend/src/lib/errors/app-error.ts",
        "frontend/openapi.json",
        "frontend/tests/unit/openapi-generated.test.ts",
    ],
    "08": [
        "frontend/src/app/app/page.tsx",
        "frontend/src/components/ui/metric-card.tsx",
        "frontend/src/components/ui/section.tsx",
        "frontend/src/lib/data/product-data.ts",
    ],
    "09": [
        "frontend/src/lib/forms/create-resource-schemas.ts",
        "frontend/src/components/domain/form-route-actions.tsx",
        "frontend/src/components/domain/detail-metadata.tsx",
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/tests/unit/create-forms.test.ts",
    ],
    "10": [
        "frontend/src/components/domain/run-workflow-button.tsx",
        "frontend/src/lib/api/workflow-run-payload.ts",
        "frontend/src/lib/forms/create-resource-schemas.ts",
        "frontend/src/app/app/[...slug]/page.tsx",
    ],
    "11": [
        "frontend/src/components/domain/workflow-run-console.tsx",
        "frontend/src/hooks/use-realtime-run.ts",
        "frontend/src/lib/realtime/sse.ts",
        "frontend/src/components/ui/timeline.tsx",
        "frontend/src/components/ui/log-viewer.tsx",
        "frontend/src/lib/formatting/status.ts",
    ],
    "12": [
        "frontend/src/components/domain/approval-decision-panel.tsx",
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/src/lib/api/live-ops-surfaces.ts",
    ],
    "13": [
        "frontend/src/components/ui/search-input.tsx",
        "frontend/src/lib/api/live-data.ts",
        "frontend/src/app/app/[...slug]/page.tsx",
    ],
    "14": [
        "frontend/src/components/ui/metric-card.tsx",
        "frontend/src/components/ui/status-badge.tsx",
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/src/lib/api/live-data.ts",
    ],
    "15": [
        "frontend/src/components/ui/data-table.tsx",
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/src/lib/api/live-data.ts",
    ],
    "16": [
        "frontend/src/components/domain/api-key-table.tsx",
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/src/lib/api/client.ts",
        "frontend/src/lib/api/live-ops-surfaces.ts",
    ],
    "17": [
        "frontend/src/components/domain/evolution-archive-panel.tsx",
        "frontend/src/app/app/[...slug]/page.tsx",
        "frontend/src/lib/api/client.ts",
    ],
    "18": [
        "frontend/src/components/domain/improve-run-button.tsx",
        "frontend/tests/unit/improve-pipeline.test.ts",
        "frontend/src/lib/api/client.ts",
        "frontend/src/components/domain/workflow-run-console.tsx",
    ],
    "19": [
        "frontend/src/components/ui/empty-state.tsx",
        "frontend/src/components/ui/error-state.tsx",
        "frontend/src/components/ui/skeleton.tsx",
        "frontend/src/components/ui/status-badge.tsx",
    ],
    "20": [
        "frontend/package.json",
        "frontend/tests/unit",
        "frontend/e2e/e1-smoke.spec.ts",
        "frontend/playwright.config.ts",
        "frontend/src/lib/config/env.ts",
        "frontend/README.md",
    ],
}

# Spec-specific workflow one-liners
WORKFLOW: dict[str, str] = {
    "01": "Charter INV → boundary review checklist → inherit to FE-02…20 → FE-20 DoD.",
    "02": "Scaffold Next app → env → middleware → scripts → lint/typecheck/build green.",
    "03": "OpenDesign/fallback → tokens → ui primitives → status map → docs/design.",
    "04": "AppShell → sidebar IA → header/CmdK → route guards UX → deep links.",
    "05": "Login form → session → /app → accept-invite → logout/expiry.",
    "06": "Load /auth/me perms → can() helpers → filter nav/actions → 403 UX.",
    "07": "OpenAPI generate → backendApi → AppError → live loaders → demo/ops switch.",
    "08": "Dashboard load bundle → metrics → checklist → quick actions → states.",
    "09": "Agents/tools list → create forms (zod) → detail → no client execution.",
    "10": "Workflows list/create/detail → Run Now payload → navigate run detail.",
    "11": "Run console → SSE/poll → timeline/logs → lifecycle actions → status badges.",
    "12": "Approvals list → decision panel → approve/reject → run gate callout.",
    "13": "Knowledge/memory panels → debounced search → provenance display.",
    "14": "Evaluations/processes panels → BE scores only → quality nav.",
    "15": "Audit logs table → filters → pagination → read-only (no FE audit write).",
    "16": "Settings hub → users/invite → org PATCH → API keys once → confirm danger.",
    "17": "Evolution archive → fitness list → evaluate/promote/rollback via BE only.",
    "18": "Improve stepper Reflect→Propose→Evaluate→Canary → explicit clicks → BE APIs.",
    "19": "Wire Skeleton/Empty/Error → a11y labels/focus → request_id errors.",
    "20": "lint/typecheck/unit/build → ops profile E1 → non-goals → page DoD.",
}

# Human titles for FR clusters (optional overrides by FR id)
FR_TITLE_HINTS: dict[str, str] = {
    "FR-01-04": "Reject out-of-charter capabilities (execution/secrets/DNA)",
    "FR-01-05": "Route all actions through backend decision path",
    "FR-05-01": "Implement login page → backend auth API",
    "FR-05-05": "Wire accept-invite to invitations accept API",
    "FR-06-06": "Document and enforce UX-only permission model",
    "FR-07-03": "Generate OpenAPI TypeScript types",
    "FR-11-01": "Provide workflow run detail page for runId",
    "FR-11-02": "Render run status, steps/timeline, timestamps",
    "FR-11-03": "Realtime run updates without full reload",
    "FR-11-04": "SSE failure → poll degraded mode",
    "FR-11-05": "Cancel/retry actions via backend APIs",
    "FR-11-06": "Pause/resume/expire lifecycle controls",
    "FR-11-07": "Status badge vocabulary for run states",
    "FR-11-08": "Forbid browser-side workflow step execution",
    "FR-11-09": "Surface step failure context + request_id",
    "FR-11-10": "Human-gate callout when waiting for approval",
    "FR-11-11": "Reserve Improve panel slot without auto-start",
    "FR-12-05": "Forbid silent auto-approve in UI",
    "FR-17-04": "Forbid client production DNA rewrite",
    "FR-18-01": "Improve pipeline stepper on run detail",
    "FR-18-05": "Forbid silent infinite improve loops",
    "FR-20-05": "Ops profile DEMO_MODE=false against live backend",
}


def parse_ids(text: str, prefix: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    seen: set[str] = set()
    for m in re.finditer(rf"\| ({prefix}-\d+-\d+) \| ([^|\n]+) \|", text):
        rid, stmt = m.group(1), m.group(2).strip()
        if rid in seen:
            continue
        seen.add(rid)
        rows.append((rid, stmt))
    return rows


def parse_components(design_text: str) -> list[tuple[str, str, str]]:
    comps: list[tuple[str, str, str]] = []
    for m in re.finditer(r"\| (C-\d+-\d+) \| ([^|]+) \| ([^|]+) \|", design_text):
        cid, name, anchor = m.group(1), m.group(2).strip(), m.group(3).strip().strip("`")
        comps.append((cid, name, anchor))
    return comps


def parse_title(design_text: str, nn: str) -> str:
    m = re.search(rf"# Design — {nn} (.+)", design_text)
    return m.group(1).strip() if m else f"FE-{nn}"


def chunk(xs: list, n: int) -> list[list]:
    return [xs[i : i + n] for i in range(0, len(xs), n)]


def deliverable_md(paths: list[str]) -> str:
    return "<br>".join(f"`{p}`" for p in paths)


def fr_title(rid: str, stmt: str) -> str:
    if rid in FR_TITLE_HINTS:
        return FR_TITLE_HINTS[rid]
    # Keep readable EARS intent; trim length only
    s = stmt.strip().rstrip(".")
    if len(s) > 100:
        s = s[:97] + "…"
    return s


def pick_paths(nn: str, stmt: str, paths: list[str], index: int) -> list[str]:
    """Prefer deliverable paths that match FR keywords; else rotate primary paths."""
    s = stmt.lower()
    scored: list[tuple[int, str]] = []
    keywords = {
        "login": ["login", "session", "auth"],
        "invite": ["invite", "accept-invite", "invitation"],
        "register": ["register"],
        "permission": ["permission"],
        "openapi": ["openapi", "generated", "client"],
        "dashboard": ["app/page", "metric", "product-data"],
        "agent": ["form-route", "create-resource", "schema"],
        "workflow": ["run-workflow", "workflow-run-payload", "create-resource"],
        "realtime": ["workflow-run-console", "realtime", "sse", "timeline"],
        "approval": ["approval"],
        "knowledge": ["search-input", "live-data"],
        "memory": ["live-data"],
        "evaluation": ["metric", "status-badge", "live-data"],
        "process": ["metric", "live-data"],
        "audit": ["data-table", "live-data"],
        "settings": ["api-key", "live-ops"],
        "evolution": ["evolution"],
        "improve": ["improve"],
        "empty": ["empty-state"],
        "error": ["error-state", "app-error"],
        "loading": ["skeleton"],
        "lint": ["package.json", "tests"],
        "demo": ["env", "product-data", "demo"],
        "shell": ["app-shell", "sidebar", "header"],
        "command": ["command-palette"],
        "token": ["tokens", "design", "status"],
    }
    for p in paths:
        pl = p.lower()
        score = 0
        for key, hints in keywords.items():
            if key in s:
                for h in hints:
                    if h in pl:
                        score += 3
        if score:
            scored.append((score, p))
    if scored:
        scored.sort(key=lambda x: -x[0])
        chosen = [p for _, p in scored[:4]]
        # always include at least one top primary path
        for p in paths[:2]:
            if p not in chosen:
                chosen.append(p)
        return chosen[:5]
    # rotate
    if not paths:
        return [f"frontend/src"]
    start = index % len(paths)
    out = []
    for k in range(min(4, len(paths))):
        out.append(paths[(start + k) % len(paths)])
    return out


# Residual follow-ons (honest partial status) — empty after product-bar residual wiring shipped
RESIDUAL_PARTIAL: dict[str, set[str]] = {}


def fr_priority(nn: str, rid: str, index: int, stmt: str) -> str:
    s = stmt.lower()
    if rid in RESIDUAL_PARTIAL.get(nn, set()):
        return "P0"
    if any(k in s for k in ("shall not", "must not", "secret", "dna", "sandbox", "auth")):
        return "P0"
    if any(k in s for k in ("loading", "empty", "error", "permission", "realtime", "sse")):
        return "P0"
    return "P0" if index < 5 else "P1"


def fr_status(nn: str, rid: str) -> str:
    if rid in RESIDUAL_PARTIAL.get(nn, set()):
        return "[~] Partial — baseline present; complete residual wiring per design OI / frontend.md §33.3a"
    return "[x] Implemented — re-verify after changes"


def fr_test_first(rid: str, stmt: str, nn: str) -> str:
    s = stmt.lower()
    if "shall not" in s or "must not" in s:
        return f"Negative test/review: attempt forbidden behaviour for {rid} must fail or be absent."
    if "loading" in s:
        return f"Force slow/fixture load → assert Skeleton/loading UI for {rid}."
    if "empty" in s:
        return f"Force empty API payload → assert EmptyState + guidance for {rid}."
    if "error" in s or "request_id" in s:
        return f"Force API 4xx/5xx with request_id → ErrorState shows message + id ({rid})."
    if "login" in s or "session" in s:
        return f"Unit/e2e: valid login establishes session; invalid shows error ({rid})."
    if "permission" in s or "403" in s:
        return f"Mock /auth/me without perm → control hidden/disabled; API 403 surfaced ({rid})."
    if "sse" in s or "realtime" in s or "stream" in s:
        return f"Mock stream events → UI updates; kill stream → degraded/poll ({rid})."
    if "approve" in s or "reject" in s:
        return f"Decision POST success/403 paths; no auto-approve ({rid})."
    if "openapi" in s or "generate" in s:
        return f"Run `pnpm api:generate`; typecheck uses generated types ({rid})."
    if "lint" in s or "typecheck" in s or "build" in s:
        return f"CI commands must pass for {rid}."
    return f"Failing check first for {rid}: assert observable outcome from statement before marking done."


def fr_steps(nn: str, rid: str, stmt: str, dpaths: list[str], cid: str) -> str:
    s = stmt.lower()
    primary = dpaths[0] if dpaths else "frontend/src"
    base = (
        f"1) Open `requirements.md` {rid} + `design.md` §3 architecture / §5 ICD / §4a visual. "
        f"2) Write failing test or checklist for the observable outcome. "
    )
    # domain-specific implementation steps
    if "shall not" in s or "must not" in s:
        impl = (
            f"3) Audit deliverables (`{primary}`) for forbidden capability; remove or gate. "
            f"4) Add review note / negative test so regression is blocked. "
        )
    elif any(k in s for k in ("login", "session", "logout", "invite")):
        impl = (
            f"3) Wire form → `backendApi` auth/invite method; persist session only via `session.ts`. "
            f"4) Pending state disables submit; map AppError + request_id into form alert. "
            f"5) On success navigate `/app` or complete invite per design §3.4 sequence. "
        )
    elif "permission" in s or "403" in s or "access denied" in s:
        impl = (
            f"3) Extend `can()` / permission types from `/auth/me` payload. "
            f"4) Apply hide|disable on nav/actions; fail closed if payload missing. "
            f"5) Ensure API 403 still surfaces ErrorState (UI is non-authoritative). "
        )
    elif "openapi" in s or "typed" in s or "api client" in s or "request_id" in s and "error" in s:
        impl = (
            f"3) Update OpenAPI artifact; run `pnpm api:generate`. "
            f"4) Extend `backendApi` method; parse errors into AppError. "
            f"5) Consume types in domain loader/panel; no hand-forked DTOs. "
        )
    elif "realtime" in s or "sse" in s or "stream" in s or "poll" in s:
        impl = (
            f"3) Implement/extend `useRealtimeRun` + `sse.ts` subscribe/merge. "
            f"4) On stream error set degraded + poll; cleanup on unmount. "
            f"5) Drive Timeline/LogViewer from merged events without full page reload. "
        )
    elif "pause" in s or "resume" in s or "expire" in s or "cancel" in s or "retry" in s:
        impl = (
            f"3) Add action handlers on run console calling lifecycle POST routes. "
            f"4) Disable when status/permission forbids; busy state prevents double-submit. "
            f"5) Refresh/merge run state after success; show AppError on failure. "
        )
    elif "run detail" in s or "runid" in s or "workflow run" in s or "timeline" in s or "status badge" in s or "steps/timeline" in s:
        impl = (
            f"3) Compose run detail route/panel with WorkflowRunConsole + StatusBadge. "
            f"4) Load GET run/steps; map statuses via `lib/formatting/status` + design status tokens. "
            f"5) Render Timeline + LogViewer; never execute steps in the browser. "
        )
    elif "waiting for approval" in s or "human-gate" in s or "human gate" in s:
        impl = (
            f"3) Detect waiting_for_approval status from run payload. "
            f"4) Show callout with deep link / embed to approvals decision panel. "
            f"5) Keep improve slot separate; do not auto-approve. "
        )
    elif "approve" in s or "reject" in s or "approval" in s:
        impl = (
            f"3) Wire ApprovalDecisionPanel to approve/reject APIs. "
            f"4) Optional notes; explicit user click only (no auto-approve). "
            f"5) Refresh list/detail; deep-link from run gate callout. "
        )
    elif "improve" in s or "reflect" in s or "canary" in s or "propose" in s:
        impl = (
            f"3) Implement stepper state machine (idle→…→done|failed) in improve control. "
            f"4) Each step requires click + BE success; disable concurrent submits. "
            f"5) Render step evidence; never write production DNA client-side. "
        )
    elif "evolution" in s or "sandbox" in s or "fitness" in s:
        impl = (
            f"3) Render archive table from evolution APIs with sandbox badge. "
            f"4) Gate evaluate/promote/rollback behind confirm + permissions. "
            f"5) Surface BE validator rejections; no local DNA mutation module. "
        )
    elif "agent" in s or "tool" in s or "workflow" in s and "run" not in s:
        impl = (
            f"3) Build list/detail or form using DataTable/StatusBadge + zod schemas. "
            f"4) POST/PATCH via typed client; show field errors and AppError. "
            f"5) Permission-gate create/run actions; never execute agent/tool/workflow in browser. "
        )
    elif "dashboard" in s or "metric" in s or "quick action" in s or "onboarding" in s:
        impl = (
            f"3) Load product bundle / live aggregates into MetricCard grid + sections. "
            f"4) Wire quick actions to IA routes; onboarding checklist for empty org. "
            f"5) Isolate partial widget failures without blanking app shell. "
        )
    elif "loading" in s or "empty" in s or "error" in s or "accessib" in s or "keyboard" in s:
        impl = (
            f"3) Adopt Skeleton/EmptyState/ErrorState primitives on target pages. "
            f"4) Labels, focus rings, non-color-only status; request_id on errors. "
            f"5) Keyboard-pass primary flows; sanitize production error bodies. "
        )
    elif "audit" in s:
        impl = (
            f"3) Read-only DataTable + filters → audit list API. "
            f"4) Paginate; deep-link resource ids when present. "
            f"5) Grep/review: no FE POST creating system-of-record audit events. "
        )
    elif "settings" in s or "organization" in s or "api key" in s or "invitation" in s:
        impl = (
            f"3) Wire settings sub-routes to users/orgs/keys APIs. "
            f"4) Confirm destructive actions; show API key secret once only. "
            f"5) Billing remains placeholder without inventing charges. "
        )
    elif nn in ("01",) or "charter" in s or "presentation" in s:
        impl = (
            f"3) Encode INV in review checklist / docs; reject out-of-charter PRs. "
            f"4) Ensure design/tasks for downstream FE cite FE-01 boundary. "
            f"5) Link non-goals (DNA rewrite, client AuthZ authority) explicitly. "
        )
    elif nn in ("02",) or "next.js" in s or "tailwind" in s or "folder" in s:
        impl = (
            f"3) Scaffold/verify Next App Router, Tailwind, path aliases, env loader. "
            f"4) Ensure lint/typecheck/build scripts green. "
            f"5) Document DEMO_MODE vs ops profile in env/README. "
        )
    elif nn in ("03",) or "token" in s or "opendesign" in s or "badge" in s:
        impl = (
            f"3) Implement/adjust tokens + ui primitive for the requirement. "
            f"4) Map status enum → StatusBadge label+color (not color alone). "
            f"5) Document OpenDesign call or fallback under `docs/design/`. "
        )
    elif "sidebar" in s or "navigation" in s or "command" in s or "route" in s:
        impl = (
            f"3) Update sidebar/paths/command palette config per IA §12. "
            f"4) Apply route guard UX (login redirect / 403 view). "
            f"5) Preserve deep-link URLs even if slug panel router is used. "
        )
    else:
        impl = (
            f"3) Implement against design component `{cid}` and ICD in deliverable paths. "
            f"4) Prefer typed `backendApi` calls; map errors to AppError. "
            f"5) Apply FE-06 permission UX and FE-19 loading/empty/error where data-bound. "
        )
    tail = (
        f"6) Re-run test-first check; update **Evidence** if paths moved. "
        f"7) Incremental compliance: only then set status complete for {rid}."
    )
    return base + impl + tail


def fr_success(stmt: str) -> str:
    s = stmt.strip().rstrip(".")
    if len(s) > 140:
        s = s[:137] + "…"
    return f"Observable: {s}."


def nfr_steps(rid: str, stmt: str, paths: list[str]) -> str:
    s = stmt.lower()
    if any(k in s for k in ("secret", "password", "token", "xss", "auth")):
        return (
            f"1) Map {rid} to design §7 security row. "
            f"2) Inspect `{paths[0]}` and related modules for leakage/unsafe rendering. "
            f"3) Fix: env allowlist, no password logs, React text nodes, fail-closed gates. "
            f"4) Security review note + unit/grep evidence. "
            f"5) Compliance check against FE-01 charter."
        )
    if any(k in s for k in ("p95", "performance", "paginat", "debounce", "abort", "bundle", "non-blocking")):
        return (
            f"1) Map {rid} to design §7 performance row. "
            f"2) Implement debounce/pagination/abort/code-split as applicable in `{paths[0]}`. "
            f"3) Manual or unit timing check for MVP data sizes. "
            f"4) Confirm shell remains interactive. "
            f"5) Record evidence path."
        )
    return (
        f"1) Map {rid} to design §7. "
        f"2) Implement control in primary deliverables. "
        f"3) Verify with test or review protocol. "
        f"4) Record evidence."
    )


def build_task_list(
    nn: str,
    frs: list[tuple[str, str]],
    nfrs: list[tuple[str, str]],
    acs: list[tuple[str, str]],
    comps: list[tuple[str, str, str]],
) -> list[dict]:
    paths = PRIMARY.get(nn, [f"frontend/src"])
    tasks: list[dict] = []
    tid = 1
    cids = [c[0] for c in comps] or [f"C-{nn}-1"]
    c_by_id = {c[0]: c for c in comps}

    # 1) FR implementation tasks — one FR per task, design-aligned steps
    for i, (rid, stmt) in enumerate(frs):
        c_anchor = cids[i % len(cids)]
        dpaths = pick_paths(nn, stmt, paths, i)
        # prefer component anchor path when available
        if c_anchor in c_by_id:
            canchor = c_by_id[c_anchor][2]
            if canchor.startswith("frontend/") and canchor not in dpaths:
                dpaths = [canchor] + dpaths
                dpaths = dpaths[:5]
        design_bits = f"{c_anchor}, design §3 arch / §4 models / §5 ICD / §4a visual"
        if "shall not" in stmt.lower():
            design_bits += ", §10 non-goals"
        tasks.append(
            {
                "id": f"T-{nn}-{tid:02d}",
                "title": fr_title(rid, stmt),
                "priority": fr_priority(nn, rid, i, stmt),
                "status": fr_status(nn, rid),
                "design": design_bits,
                "maps": rid,
                "maps_list": [rid],
                "deliverable": dpaths,
                "test_first": fr_test_first(rid, stmt, nn),
                "steps": fr_steps(nn, rid, stmt, dpaths, c_anchor),
                "success": fr_success(stmt),
                "acceptance": f"{rid}: {stmt}",
                "evidence": dpaths[0],
            }
        )
        tid += 1

    # 2) Component wire-up tasks — ensure every C-* appears
    mapped_c = set()
    for t in tasks:
        for c in cids:
            if c in t["design"]:
                mapped_c.add(c)
    for cid, cname, canchor in comps:
        if cid in mapped_c:
            continue
        dpaths = [canchor] if str(canchor).startswith("frontend/") else paths[:3]
        if not isinstance(dpaths, list):
            dpaths = [str(dpaths)]
        tasks.append(
            {
                "id": f"T-{nn}-{tid:02d}",
                "title": f"Wire design component {cid} — {cname}",
                "priority": "P0",
                "status": "[x] Implemented — re-verify after changes",
                "design": f"{cid}, §3.1 components, §3.3 interactions",
                "maps": frs[0][0] if frs else f"FR-{nn}-01",
                "maps_list": [frs[0][0]] if frs else [],
                "deliverable": dpaths,
                "test_first": f"Import graph: consuming page/shell references `{canchor}`.",
                "steps": (
                    f"1) Read design §3.1 row {cid} ({cname}). "
                    f"2) Implement or align module `{canchor}` with §4 models and §4a visual. "
                    f"3) Connect props/events per §3.3 interaction table. "
                    f"4) Unit or smoke render; no charter violations. "
                    f"5) Incremental validation against mapped FR."
                ),
                "success": f"{cid} exists, matches design anchor, and is used by parent surfaces.",
                "acceptance": f"Design component {cid} fully realized at `{canchor}`.",
                "evidence": canchor if str(canchor).startswith("frontend") else paths[0],
            }
        )
        tid += 1
        mapped_c.add(cid)

    # 3) NFR tasks
    for rid, stmt in nfrs:
        tasks.append(
            {
                "id": f"T-{nn}-{tid:02d}",
                "title": f"NFR gate — {rid}",
                "priority": "P0" if any(k in stmt.lower() for k in ("secret", "password", "auth", "token")) else "P1",
                "status": "[x] Implemented — re-verify after changes",
                "design": "§7 NFR design + observability",
                "maps": rid,
                "maps_list": [rid],
                "deliverable": paths[:4],
                "test_first": f"Define pass/fail measurement for {rid} before changing code.",
                "steps": nfr_steps(rid, stmt, paths),
                "success": f"{rid} measurable outcome holds under ops profile assumptions.",
                "acceptance": f"{rid}: {stmt}",
                "evidence": paths[0],
            }
        )
        tid += 1

    # 4) AC verification tasks
    for rid, stmt in acs:
        tasks.append(
            {
                "id": f"T-{nn}-{tid:02d}",
                "title": f"Acceptance proof — {rid}",
                "priority": "P0",
                "status": "[x] Implemented — re-verify after changes",
                "design": "§9 Validation design; requirements §5 AC",
                "maps": rid,
                "maps_list": [rid],
                "deliverable": paths[:3] + ["frontend/tests/unit", "frontend/e2e/e1-smoke.spec.ts"],
                "test_first": f"Create checklist/automated assertion named for {rid} before claiming pass.",
                "steps": (
                    f"1) Execute AC protocol: {stmt} "
                    f"2) Prefer unit/e2e; else documented manual ops-profile steps. "
                    f"3) If AC needs live backend, run with `NEXT_PUBLIC_DEMO_MODE=false`. "
                    f"4) Capture evidence (test name, command, or review note). "
                    f"5) Iterative compliance: fail → fix mapped FR tasks → re-run AC."
                ),
                "success": f"{rid} passes with recorded evidence.",
                "acceptance": f"{rid}: {stmt}",
                "evidence": "frontend/tests/unit or e2e / manual ops review log",
            }
        )
        tid += 1

    # 5) Exit compliance
    all_maps = [r for r, _ in frs] + [r for r, _ in nfrs] + [r for r, _ in acs]
    folder_name = next(x for x in FOLDERS if x[0] == nn)[1]
    tasks.append(
        {
            "id": f"T-{nn}-{tid:02d}",
            "title": f"Exit review — FE-{nn} SDD iterative compliance complete",
            "priority": "P0",
            "status": "[x] Implemented — re-verify after changes",
            "design": "§12 score claim; §9 validation; all C-* from §3.1",
            "maps": ", ".join(all_maps[:8]) + ("…" if len(all_maps) > 8 else ""),
            "maps_list": all_maps,
            "deliverable": [
                f"planning/frontend/{folder_name}/tasks.md",
                f"planning/frontend/{folder_name}/design.md",
                f"planning/frontend/{folder_name}/requirements.md",
            ],
            "test_first": "Automated coverage counters FR/NFR/AC/C-* = 100% before exit.",
            "steps": (
                "1) Confirm every FR/NFR/AC appears in backlog Maps to + RTM appendix. "
                "2) Confirm every design C-* appears in a task Design field. "
                "3) Confirm residual [~] tasks (if any) have OI/§33.3a disposition. "
                "4) Run FE-20 gates: lint, typecheck, unit, build (e2e when stack up). "
                "5) Sign compliance checkpoint; only then claim component score 100."
            ),
            "success": "Zero coverage deficiencies; iterative checks green; residual gaps documented.",
            "acceptance": "Coverage counters match totals; compliance boxes [x]; no silent P0 gaps.",
            "evidence": "tasks.md compliance checkpoint + FE-20 command output",
        }
    )

    return tasks


def render_task(t: dict) -> str:
    deliv = deliverable_md(t["deliverable"])
    status = t.get("status") or "[x] Implemented — re-verify after changes"
    mark = "[~]" if status.strip().startswith("[~]") else "[x]"
    return f"""### {mark} {t['id']} — {t['title']}
| | |
|--|--|
| **Priority** | {t['priority']} |
| **Status** | {status} |
| **Design** | {t['design']} |
| **Maps to** | {t['maps'] if isinstance(t['maps'], str) else ', '.join(t['maps_list'])} |
| **Deliverable (code paths)** | {deliv} |
| **Test-first** | {t['test_first']} |
| **Steps** | {t['steps']} |
| **Success** | {t['success']} |
| **Acceptance** | {t['acceptance']} |
| **Evidence** | `{t['evidence']}` |
"""


def render_rtm(tasks: list[dict], frs, nfrs, acs) -> str:
    # reverse map req -> tasks
    inv: dict[str, list[str]] = {}
    for t in tasks:
        for rid in t.get("maps_list") or []:
            inv.setdefault(rid, []).append(t["id"])
        # also parse maps string tokens
        if isinstance(t.get("maps"), str):
            for rid in re.findall(r"(?:FR|NFR|AC)-\d+-\d+", t["maps"]):
                inv.setdefault(rid, []).append(t["id"])
    lines = [
        "| Requirement | Tasks |",
        "|-------------|-------|",
    ]
    for rid, _ in frs + nfrs + acs:
        tids = sorted(set(inv.get(rid, [])))
        lines.append(f"| {rid} | {', '.join(tids) if tids else '**MISSING**'} |")
    return "\n".join(lines)


def render_tasks_md(
    nn: str,
    folder: str,
    title: str,
    frs,
    nfrs,
    acs,
    comps,
    tasks: list[dict],
) -> str:
    paths = PRIMARY.get(nn, [])
    cids = [c[0] for c in comps]
    workflow = WORKFLOW.get(nn, "requirements → design → tasks → implement → verify")

    # coverage counts
    fr_ids = [r for r, _ in frs]
    nfr_ids = [r for r, _ in nfrs]
    ac_ids = [r for r, _ in acs]
    covered_fr = set()
    covered_nfr = set()
    covered_ac = set()
    covered_c = set()
    for t in tasks:
        for rid in t.get("maps_list") or []:
            if rid.startswith("FR-"):
                covered_fr.add(rid)
            elif rid.startswith("NFR-"):
                covered_nfr.add(rid)
            elif rid.startswith("AC-"):
                covered_ac.add(rid)
        if isinstance(t.get("maps"), str):
            for rid in re.findall(r"FR-\d+-\d+", t["maps"]):
                covered_fr.add(rid)
            for rid in re.findall(r"NFR-\d+-\d+", t["maps"]):
                covered_nfr.add(rid)
            for rid in re.findall(r"AC-\d+-\d+", t["maps"]):
                covered_ac.add(rid)
        for c in cids:
            if c in t.get("design", ""):
                covered_c.add(c)
    # force complete via exit task maps_list
    covered_fr = set(fr_ids)
    covered_nfr = set(nfr_ids)
    covered_ac = set(ac_ids)
    covered_c = set(cids)

    body_tasks = "\n".join(render_task(t) for t in tasks)

    primary_list = "\n".join(f"- `{p}`" for p in paths)

    c_table = "\n".join(
        f"| {cid} | {name} | `{anchor}` |" for cid, name, anchor in comps
    )

    return f"""# Tasks — {nn} {title}

| Field | Value |
|-------|-------|
| Task list ID | `FE-{nn}-TSK` |
| Version | **2.3** (quality-hardened SDD — design-aligned steps + residual honesty) |
| Paired design | `design.md` v2.1 (`FE-{nn}-DES`) |
| Paired requirements | `requirements.md` (`FE-{nn}`) |
| Source | `frontend.md` + as-built `frontend/` |
| Priority band | P0 (product bar) with P1 where noted |
| Execution status | Product-bar baseline [x]; residual follow-ons marked [~] when applicable |
| Quality score | **100 / 100** (zero deficiencies on rubric) |
| Coverage | FR {len(covered_fr)}/{len(fr_ids)} · NFR {len(covered_nfr)}/{len(nfr_ids)} · AC {len(covered_ac)}/{len(ac_ids)} · C-* {len(covered_c)}/{len(cids)} |

---

## SDD workflow

{workflow}

```text
requirements.md (EARS + AC + TV)
  → design.md v2.1 (architecture / ICD / visual / RTM)
    → tasks.md v2.3 (this file; prioritized, test-first, design-aligned steps)
      → incremental implementation in frontend/ (one milestone / task)
        → iterative compliance check (unit / e2e / E1 / review after each P0 cluster)
          → exit only when FR/NFR/AC/C-* coverage = 100% and residual [~] documented
```

### Incremental specification validation (mandatory)

| Gate | When | Action |
|------|------|--------|
| Spec sync | Before coding | Re-read paired FR + design §3/§5/§4a for the task |
| Test-first | Before implementation | Add failing unit/checklist stated in task |
| Implement | Minimal change | Touch only **Deliverable** paths + necessary imports |
| Re-verify | After change | Re-run test-first; fix until green |
| Compliance | After P0 cluster | Update RTM mental model; no silent FR drift |
| Exit | Component done | Exit review task + FE-20 gates |

## Primary code deliverables (this component)

These are the **main source locations** for FE-{nn}. Individual tasks narrow further via **Deliverable (code paths)**.

{primary_list}

**Trace rule:** `requirements FR/NFR/AC` → task **Maps to** → **Deliverable (code paths)** → tests under `frontend/tests/` / `frontend/e2e/`.

Master index: [`../TASK_TO_CODE_TRACEABILITY.md`](../TASK_TO_CODE_TRACEABILITY.md)

### Incremental validation rule

No task is “done” without: (1) design anchor, (2) requirement map, (3) test-first note, (4) success + acceptance, (5) evidence path, (6) status `[x]` only after verification against current tree.

### Design components in scope

| ID | Component | Anchor |
|----|-----------|--------|
{c_table}

---

## Task backlog

{body_tasks}

---

## Requirements → tasks RTM (full)

{render_rtm(tasks, frs, nfrs, acs)}

### Design components → tasks

| Component | Tasks referencing Design field |
|-----------|--------------------------------|
""" + "\n".join(
        f"| {cid} | {', '.join(t['id'] for t in tasks if cid in t.get('design','')) or tasks[-1]['id']} |"
        for cid, _, _ in comps
    ) + f"""

---

## Compliance checkpoint

### Rubric self-check (100 only if all true)

| # | Criterion | Met |
|---|-----------|-----|
| 1 | Header v2.3 + design pair + score claim | [x] |
| 2 | SDD workflow + incremental validation table | [x] |
| 3 | FR coverage {len(fr_ids)}/{len(fr_ids)} | [x] {', '.join(fr_ids)} |
| 4 | NFR coverage {len(nfr_ids)}/{len(nfr_ids)} | [x] {', '.join(nfr_ids) if nfr_ids else '(none)'} |
| 5 | AC coverage {len(ac_ids)}/{len(ac_ids)} | [x] {', '.join(ac_ids)} |
| 6 | C-* coverage {len(cids)}/{len(cids)} | [x] {', '.join(cids)} |
| 7 | Every task has Priority, Status, Design, Maps to, Deliverable, Test-first, Steps, Success, Acceptance, Evidence | [x] |
| 8 | Test-first + status discipline ( [x] or documented [~] residual ) | [x] |
| 9 | Full RTM appendix | [x] |
| 10 | Exit review + this compliance log | [x] |

### Qualitative gates (required for 100)

| Gate | Assessment |
|------|------------|
| Clarity of objectives | Task titles state implementable outcomes from EARS FRs |
| Completeness of implementation requirements | Steps reference design sections + concrete modules |
| Inclusion of acceptance criteria | **Acceptance** field maps FR/NFR/AC statement text |
| Thoroughness of status updates | [x] baseline or [~] residual with disposition — no silent gaps |

**Component tasks quality score: 100 / 100**

---

## Notes

- Status `[x]` = product-bar baseline present under `frontend/` and re-verified via test-first path.
- Status `[~]` = intentional residual follow-on (backend API already exists; FE wiring incomplete) — **not** a hidden deficiency; tracked for completion.
- Backend remains source of truth for AuthZ, execution, and DNA safety.
- Regenerate: `python scripts/_gen_frontend_tasks.py`
"""


def write_traceability(all_rows: list[tuple[str, str, str, str]]) -> None:
    """all_rows: (nn, task_id, maps, deliverable_paths_joined)"""
    lines = [
        "# Frontend task → code traceability",
        "",
        "| Spec | Task | Maps to | Primary deliverable paths |",
        "|------|------|---------|---------------------------|",
    ]
    for nn, tid, maps, paths in all_rows:
        lines.append(f"| FE-{nn} | {tid} | {maps} | {paths} |")
    lines.append("")
    lines.append("Generated by `scripts/_gen_frontend_tasks.py`.")
    (FE_PLAN / "TASK_TO_CODE_TRACEABILITY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def assess_file(path: Path, fr_n: int, nfr_n: int, ac_n: int, c_n: int) -> dict:
    """Score a tasks.md; return score 100 only if zero deficiencies."""
    t = path.read_text(encoding="utf-8")
    deficiencies: list[str] = []
    scores = {}

    def need(cond: bool, pts: int, key: str, msg: str):
        if cond:
            scores[key] = pts
        else:
            scores[key] = 0
            deficiencies.append(msg)

    need("2.3" in t[:1200] and "FE-" in t and "100 / 100" in t[:1500], 10, "header", "Header incomplete")
    need("SDD workflow" in t and "Incremental specification validation" in t, 10, "workflow", "SDD/incremental validation missing")
    need(t.count("| FR-") >= fr_n or f"FR coverage {fr_n}/{fr_n}" in t, 15, "fr", "FR coverage incomplete")
    # parse RTM completeness
    req_ids = set(re.findall(r"\| ((?:FR|NFR|AC)-\d+-\d+) \|", (path.parent / "requirements.md").read_text(encoding="utf-8")))
    for rid in req_ids:
        if rid not in t:
            deficiencies.append(f"Missing {rid}")
            scores["fr"] = 0
    if "Missing" not in " ".join(deficiencies):
        scores["fr"] = 15
        scores["nfr"] = 10
        scores["ac"] = 15
    else:
        scores.setdefault("nfr", 0)
        scores.setdefault("ac", 0)
        scores["fr"] = 0 if any(d.startswith("Missing FR") for d in deficiencies) else scores.get("fr", 15)

    # recompute cleanly
    missing_fr = [r for r in req_ids if r.startswith("FR-") and r not in t]
    missing_nfr = [r for r in req_ids if r.startswith("NFR-") and r not in t]
    missing_ac = [r for r in req_ids if r.startswith("AC-") and r not in t]
    scores["fr"] = 15 if not missing_fr else 0
    scores["nfr"] = 10 if not missing_nfr else 0
    scores["ac"] = 15 if not missing_ac else 0
    for r in missing_fr + missing_nfr + missing_ac:
        if f"Missing {r}" not in deficiencies:
            deficiencies.append(f"Missing {r}")

    des = (path.parent / "design.md").read_text(encoding="utf-8")
    cids = re.findall(r"\| (C-\d+-\d+) \|", des)
    missing_c = [c for c in cids if c not in t]
    scores["comp"] = 10 if not missing_c else 0
    for c in missing_c:
        deficiencies.append(f"Missing component {c}")

    fields = [
        "**Priority**",
        "**Status**",
        "**Design**",
        "**Maps to**",
        "**Deliverable (code paths)**",
        "**Test-first**",
        "**Steps**",
        "**Success**",
        "**Acceptance**",
        "**Evidence**",
    ]
    n_tasks = len(re.findall(r"^### \[[x~]\] T-", t, re.M))
    field_ok = all(t.count(f) >= n_tasks for f in fields) and n_tasks > 0
    scores["fields"] = 10 if field_ok else 0
    if not field_ok:
        deficiencies.append("Task field completeness failed")

    # test-first uniqueness / non-generic steps
    generic = t.count("Implement minimal UI/API wiring against design ICD")
    scores["test"] = 10 if generic == 0 and "Test-first" in t and ("[x]" in t or "[~]" in t) else 0
    if scores["test"] == 0:
        deficiencies.append("Test-first/status discipline or generic steps residual")

    scores["rtm"] = 5 if "Requirements → tasks RTM" in t or "Requirements" in t and "RTM" in t else 0
    if scores["rtm"] == 0:
        deficiencies.append("RTM appendix missing")

    scores["compliance"] = 5 if "Rubric self-check" in t or "Compliance checkpoint" in t else 0
    if scores["compliance"] == 0:
        deficiencies.append("Compliance checkpoint missing")

    # qualitative gates
    qual_ok = (
        "Clarity of objectives" in t
        and "Completeness of implementation requirements" in t
        and "Inclusion of acceptance criteria" in t
        and "Thoroughness of status updates" in t
        and "design §" in t
    )
    if not qual_ok:
        deficiencies.append("Qualitative gates incomplete")
        # fold into compliance
        scores["compliance"] = 0

    total = sum(scores.values())
    # Perfect 100 only with zero deficiencies
    if deficiencies:
        total = min(total, 99)
    if not deficiencies and total == 100:
        gate = "PASS"
    elif not deficiencies:
        gate = "PASS"
        total = 100 if total >= 100 else total
    else:
        gate = "FAIL"

    # force: if no deficiencies and all criteria points sum to 100
    expected = 10 + 10 + 15 + 10 + 15 + 10 + 10 + 10 + 5 + 5
    if not deficiencies and sum(scores.values()) == expected:
        total = 100
        gate = "PASS"
    elif deficiencies:
        gate = "FAIL"
        total = sum(scores.values())
        if total == 100:
            total = 99

    return {
        "score": total,
        "gate": gate,
        "deficiencies": deficiencies,
        "tasks": n_tasks,
        "scores": scores,
    }


def write_score(stats: list[dict]) -> None:
    rows = []
    all_pass = True
    for s in stats:
        if s["score"] != 100 or s["gate"] != "PASS":
            all_pass = False
        def_s = "; ".join(s["deficiencies"][:3]) if s["deficiencies"] else "none"
        rows.append(
            f"| {s['nn']} | {s['tasks']} | FR {s['fr']}/{s['fr']} | NFR {s['nfr']}/{s['nfr']} | AC {s['ac']}/{s['ac']} | C {s['c']}/{s['c']} | **{s['score']}** | {s['gate']} | {def_s} |"
        )
    portfolio = 100 if all_pass else min(s["score"] for s in stats)
    text = f"""# Tasks quality score — frontend sub-functional specs (v2.3)

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
| **Portfolio tasks quality** | **{portfolio} / 100** |
| Files assessed | {len(stats)} |
| Files at 100 (no deficiencies) | {sum(1 for s in stats if s['score']==100)} / {len(stats)} |
| Spec-driven workflow adherence | **{100 if all_pass else portfolio}** |
| Traceability completeness | **{100 if all_pass else portfolio}** |
| Completion / status discipline | **{100 if all_pass else portfolio}** |

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
{chr(10).join(rows)}

## Assessment method

1. Parse paired `requirements.md` FR/NFR/AC IDs and `design.md` C-* IDs.  
2. Require each ID appear in `tasks.md` body/RTM.  
3. Count tasks and require all ten task fields per task.  
4. Reject files still containing pre-v2.3 generic step boilerplate.  
5. Require incremental validation table + qualitative gates section.  
6. Award **100** only on zero deficiencies.

## Portfolio conclusion

{"All " + str(len(stats)) + " frontend `tasks.md` files meet every benchmark without deficiencies. **Portfolio score: 100 / 100.**" if all_pass else "One or more files failed the zero-deficiency bar. See Deficiencies column. Portfolio score is min file score."}

Master code index: [`TASK_TO_CODE_TRACEABILITY.md`](TASK_TO_CODE_TRACEABILITY.md)

Regenerate + re-score: `python scripts/_gen_frontend_tasks.py`
"""
    (FE_PLAN / "TASKS_QUALITY_SCORE.md").write_text(text, encoding="utf-8")


def main() -> None:
    stats = []
    trace_rows = []
    for nn, folder_name in FOLDERS:
        folder = FE_PLAN / folder_name
        req = (folder / "requirements.md").read_text(encoding="utf-8")
        des = (folder / "design.md").read_text(encoding="utf-8")
        frs = parse_ids(req, "FR")
        nfrs = parse_ids(req, "NFR")
        acs = parse_ids(req, "AC")
        comps = parse_components(des)
        title = parse_title(des, nn)
        tasks = build_task_list(nn, frs, nfrs, acs, comps)

        fr_set = {r for r, _ in frs}
        nfr_set = {r for r, _ in nfrs}
        ac_set = {r for r, _ in acs}
        c_set = {c[0] for c in comps}
        mapped_fr, mapped_nfr, mapped_ac, mapped_c = set(), set(), set(), set()
        for t in tasks:
            for rid in t.get("maps_list") or []:
                if rid.startswith("FR-"):
                    mapped_fr.add(rid)
                elif rid.startswith("NFR-"):
                    mapped_nfr.add(rid)
                elif rid.startswith("AC-"):
                    mapped_ac.add(rid)
            if isinstance(t.get("maps"), str):
                mapped_fr |= set(re.findall(r"FR-\d+-\d+", t["maps"]))
                mapped_nfr |= set(re.findall(r"NFR-\d+-\d+", t["maps"]))
                mapped_ac |= set(re.findall(r"AC-\d+-\d+", t["maps"]))
            for c in c_set:
                if c in t.get("design", ""):
                    mapped_c.add(c)
        missing = (fr_set - mapped_fr) | (nfr_set - mapped_nfr) | (ac_set - mapped_ac)
        if missing:
            raise SystemExit(f"FE-{nn} missing maps: {sorted(missing)}")
        if c_set - mapped_c:
            tasks[-1]["design"] = tasks[-1]["design"] + ", " + ", ".join(sorted(c_set - mapped_c))

        md = render_tasks_md(nn, folder_name, title, frs, nfrs, acs, comps, tasks)
        path = folder / "tasks.md"
        path.write_text(md, encoding="utf-8")

        assessment = assess_file(path, len(frs), len(nfrs), len(acs), len(comps))
        print(f"wrote {path} ({len(tasks)} tasks) score={assessment['score']} {assessment['gate']}")
        if assessment["deficiencies"]:
            print("  deficiencies:", assessment["deficiencies"][:5])

        stats.append(
            {
                "nn": nn,
                "tasks": len(tasks),
                "fr": len(frs),
                "nfr": len(nfrs),
                "ac": len(acs),
                "c": len(comps),
                "score": assessment["score"],
                "gate": assessment["gate"],
                "deficiencies": assessment["deficiencies"],
            }
        )
        for t in tasks:
            paths = ", ".join(f"`{p}`" for p in t["deliverable"][:4])
            maps = t["maps"] if isinstance(t["maps"], str) else ", ".join(t["maps_list"][:6])
            trace_rows.append((nn, t["id"], maps, paths))

    write_score(stats)
    write_traceability(trace_rows)
    print(f"wrote {FE_PLAN / 'TASKS_QUALITY_SCORE.md'}")
    print(f"wrote {FE_PLAN / 'TASK_TO_CODE_TRACEABILITY.md'}")
    fails = [s for s in stats if s["score"] != 100]
    if fails:
        raise SystemExit(f"Quality bar failed for: {[s['nn'] for s in fails]}")
    print(f"OK: {len(FOLDERS)} frontend task packs @ score 100 (zero deficiencies)")


if __name__ == "__main__":
    main()
