from __future__ import annotations

import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = ROOT / "backend"


def dedent(value: str) -> str:
    return textwrap.dedent(value).lstrip("\n")


def write(relative_path: str, content: str) -> None:
    target = BACKEND_DIR / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(content), encoding="utf-8")


def build_files() -> dict[str, str]:
    files: dict[str, str] = {}

    files["pyproject.toml"] = """
    [project]
    name = "generic-swarm-ops-backend"
    version = "0.1.0"
    description = "Backend API server for the Generic Swarm Business Operating System."
    requires-python = ">=3.11"
    dependencies = [
      "fastapi>=0.115.0,<1.0.0",
      "uvicorn>=0.30.0,<1.0.0",
      "pydantic>=2.8.0,<3.0.0"
    ]

    [build-system]
    requires = ["setuptools>=68", "wheel"]
    build-backend = "setuptools.build_meta"
    """

    files["README.md"] = """
    # Backend

    FastAPI backend for the governed runtime described in `structure.md` and `backend.md`.

    ## What it provides

    - token-based authentication and role checks
    - workflow listing and execution
    - workflow run tracking and streaming
    - governance and approval gates
    - memory and knowledge retrieval
    - audit log capture
    - evaluation results
    - process intelligence summaries

    ## Quick start

    ```bash
    cd backend
    python -m pip install -e .
    uvicorn app.main:app --reload
    ```

    ## Demo tokens

    - `admin-token`
    - `analyst-token`
    - `approver-token`
    """

    files["app/__init__.py"] = """
    \"\"\"Backend application package.\"\"\"
    """

    files["app/runtime.py"] = """
    from __future__ import annotations

    import json
    import threading
    import uuid
    from copy import deepcopy
    from dataclasses import dataclass
    from datetime import UTC, datetime
    from pathlib import Path
    from typing import Any


    def utc_now() -> str:
        return datetime.now(UTC).isoformat()


    class RuntimeErrorBase(Exception):
        status_code = 400

        def __init__(self, message: str):
            super().__init__(message)
            self.message = message


    class NotFoundError(RuntimeErrorBase):
        status_code = 404


    class PermissionDeniedError(RuntimeErrorBase):
        status_code = 403


    class ApprovalRequiredError(RuntimeErrorBase):
        status_code = 409


    @dataclass(slots=True)
    class AuthenticatedUser:
        id: str
        organization_id: str
        email: str
        name: str
        role: str


    ROLE_PERMISSIONS = {
        "admin": {"workflows:read", "workflows:execute", "approvals:read", "approvals:decide", "governance:read", "memory:read", "memory:write", "knowledge:read", "evaluations:read", "audit:read", "processes:read", "settings:read", "users:read", "organizations:read", "agents:read", "tools:read"},
        "analyst": {"workflows:read", "workflows:execute", "approvals:read", "governance:read", "memory:read", "memory:write", "knowledge:read", "evaluations:read", "audit:read", "processes:read", "agents:read", "tools:read"},
        "approver": {"workflows:read", "approvals:read", "approvals:decide", "governance:read", "memory:read", "knowledge:read", "evaluations:read", "audit:read", "processes:read", "agents:read", "tools:read"},
        "viewer": {"workflows:read", "approvals:read", "governance:read", "memory:read", "knowledge:read", "evaluations:read", "audit:read", "processes:read", "agents:read", "tools:read"},
    }


    class RuntimeStore:
        def __init__(self, data_file: Path):
            self.data_file = data_file
            self.lock = threading.RLock()
            self.state = self._load()

        def _load(self) -> dict[str, Any]:
            if self.data_file.exists():
                return json.loads(self.data_file.read_text(encoding="utf-8"))
            default = {
                "organizations": [],
                "users": [],
                "agents": [],
                "tools": [],
                "workflows": [],
                "workflow_runs": [],
                "approvals": [],
                "audit_logs": [],
                "memory_items": [],
                "evaluation_runs": [],
                "knowledge_documents": [],
                "notifications": [],
                "process_metrics": [],
                "tokens": {},
            }
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.data_file.write_text(json.dumps(default, indent=2) + "\\n", encoding="utf-8")
            return default

        def save(self) -> None:
            with self.lock:
                self.data_file.write_text(json.dumps(self.state, indent=2) + "\\n", encoding="utf-8")

        def collection(self, name: str) -> list[dict[str, Any]]:
            return self.state[name]


    class BusinessSourceLoader:
        def __init__(self, repo_root: Path):
            self.repo_root = repo_root
            self.business_dir = repo_root / "business"

        def read_json(self, relative_path: str) -> dict[str, Any]:
            return json.loads((self.repo_root / relative_path).read_text(encoding="utf-8"))

        def load_workflows(self) -> list[dict[str, Any]]:
            workflow = self.read_json("business/examples/workflow-dna.example.json")
            return [workflow]

        def load_agents(self) -> list[dict[str, Any]]:
            return [
                {"id": "business_orchestrator", "name": "Business Orchestrator", "role": "control", "risk_tier": "tier_4_execute_with_gate"},
                {"id": "quality_compliance_agent", "name": "Quality Compliance Agent", "role": "execution", "risk_tier": "tier_2_draft"},
                {"id": "execution_agent", "name": "Execution Agent", "role": "execution", "risk_tier": "tier_3_execute_reversible"},
                {"id": "finance_ops_agent", "name": "Finance Ops Agent", "role": "execution", "risk_tier": "tier_4_execute_with_gate"},
                {"id": "communications_agent", "name": "Communications Agent", "role": "execution", "risk_tier": "tier_2_draft"},
                {"id": "governance_officer", "name": "Governance Officer", "role": "governance", "risk_tier": "tier_5_restricted"},
                {"id": "memory_steward", "name": "Memory Steward", "role": "memory", "risk_tier": "tier_2_draft"},
                {"id": "evolution_manager", "name": "Evolution Manager", "role": "evolution", "risk_tier": "tier_5_restricted"},
            ]

        def load_tools(self) -> list[dict[str, Any]]:
            register = self.read_json("business/security/tool-permissions/tool-permission-register.json")
            return [
                {
                    "id": entry["tool"],
                    "allowed_actions": entry["allowed_actions"],
                    "scope": entry["scope"],
                    "requires_human_gate_for": entry["requires_human_gate_for"],
                }
                for entry in register["tool_permissions"]
            ] + [
                {"id": "contract_parser", "allowed_actions": ["parse_contract"], "scope": "analysis_only", "requires_human_gate_for": []},
                {"id": "policy_retriever", "allowed_actions": ["retrieve_policy"], "scope": "knowledge_only", "requires_human_gate_for": []},
                {"id": "audit_log_writer", "allowed_actions": ["append_audit"], "scope": "audit_only", "requires_human_gate_for": []},
            ]

        def load_knowledge_documents(self) -> list[dict[str, Any]]:
            docs = []
            mapping = [
                ("docs/business-architecture.md", "business-architecture"),
                ("docs/process-intelligence.md", "process-intelligence"),
                ("docs/knowledge-memory.md", "knowledge-memory"),
                ("docs/workflow-dna.md", "workflow-dna"),
                ("docs/governance.md", "governance"),
                ("docs/evaluation.md", "evaluation"),
                ("docs/evolution-sandbox.md", "evolution-sandbox"),
            ]
            for relative_path, doc_id in mapping:
                path = self.repo_root / relative_path
                docs.append({
                    "id": doc_id,
                    "title": path.stem,
                    "path": relative_path.replace("\\\\", "/"),
                    "content": path.read_text(encoding="utf-8"),
                })
            return docs

        def load_seed_event(self) -> dict[str, Any]:
            return self.read_json("business/examples/event-log.example.json")

        def load_eval_card(self) -> dict[str, Any]:
            return self.read_json("business/examples/evaluation-card.example.json")

        def load_risk_tiers(self) -> dict[str, Any]:
            return self.read_json("business/governance/use-case-risk-tiering/risk-tiers.json")


    class RuntimeServices:
        def __init__(self):
            repo_root = Path(__file__).resolve().parents[2]
            self.repo_root = repo_root
            self.loader = BusinessSourceLoader(repo_root)
            self.store = RuntimeStore(repo_root / "backend" / "data" / "runtime.json")
            self._bootstrap()

        def _bootstrap(self) -> None:
            with self.store.lock:
                if self.store.collection("organizations"):
                    return

                organization_id = "org_default"
                users = [
                    {"id": "user_admin", "organization_id": organization_id, "email": "admin@example.com", "name": "Admin", "role": "admin"},
                    {"id": "user_analyst", "organization_id": organization_id, "email": "analyst@example.com", "name": "Analyst", "role": "analyst"},
                    {"id": "user_approver", "organization_id": organization_id, "email": "approver@example.com", "name": "Approver", "role": "approver"},
                ]

                self.store.state["organizations"] = [{"id": organization_id, "name": "Default Organization", "slug": "default", "status": "active", "created_at": utc_now(), "updated_at": utc_now()}]
                self.store.state["users"] = users
                self.store.state["tokens"] = {
                    "admin-token": users[0]["id"],
                    "analyst-token": users[1]["id"],
                    "approver-token": users[2]["id"],
                }
                self.store.state["agents"] = self.loader.load_agents()
                self.store.state["tools"] = self.loader.load_tools()
                self.store.state["workflows"] = self.loader.load_workflows()
                self.store.state["knowledge_documents"] = self.loader.load_knowledge_documents()
                self.store.state["process_metrics"] = [self._build_process_summary()]
                self.store.state["memory_items"] = [
                    {
                        "id": "mem_seed_contract_rules",
                        "scope": "semantic",
                        "title": "Contract Rules",
                        "content": "Enterprise contracts over configured thresholds require human review.",
                        "provenance": self.loader.load_seed_event()["provenance"],
                        "created_at": utc_now(),
                    }
                ]
                self.store.save()

        def _build_process_summary(self) -> dict[str, Any]:
            seed = self.loader.load_seed_event()
            return {
                "id": "proc_customer_onboarding",
                "process_id": seed["process_id"],
                "case_count": 1,
                "decision_points": 1,
                "average_latency_minutes": seed["outcome"]["latency_minutes"],
                "average_quality_score": seed["outcome"]["quality_score"],
                "last_updated_at": utc_now(),
            }

        def authenticate(self, token: str | None) -> AuthenticatedUser:
            if not token or token not in self.store.state["tokens"]:
                raise PermissionDeniedError("Invalid or missing bearer token")
            user_id = self.store.state["tokens"][token]
            user = next((item for item in self.store.collection("users") if item["id"] == user_id), None)
            if not user:
                raise PermissionDeniedError("Unknown user for token")
            return AuthenticatedUser(**user)

        def assert_permission(self, user: AuthenticatedUser, permission: str) -> None:
            if permission not in ROLE_PERMISSIONS.get(user.role, set()):
                raise PermissionDeniedError(f"Permission denied: {permission}")

        def issue_token(self, email: str) -> dict[str, Any]:
            user = next((item for item in self.store.collection("users") if item["email"] == email), None)
            if not user:
                raise PermissionDeniedError("Unknown user email")
            token = next((key for key, value in self.store.state["tokens"].items() if value == user["id"]), None)
            return {"access_token": token, "token_type": "bearer", "user": user}

        def list_collection(self, name: str) -> list[dict[str, Any]]:
            return deepcopy(self.store.collection(name))

        def get_workflow(self, workflow_id: str) -> dict[str, Any]:
            workflow = next((item for item in self.store.collection("workflows") if item["id"] == workflow_id), None)
            if not workflow:
                raise NotFoundError(f"Workflow not found: {workflow_id}")
            return deepcopy(workflow)

        def get_run(self, run_id: str) -> dict[str, Any]:
            run = next((item for item in self.store.collection("workflow_runs") if item["id"] == run_id), None)
            if not run:
                raise NotFoundError(f"Workflow run not found: {run_id}")
            return run

        def _append_audit(self, category: str, action: str, payload: dict[str, Any]) -> None:
            self.store.collection("audit_logs").append({
                "id": f"audit_{uuid.uuid4().hex[:12]}",
                "category": category,
                "action": action,
                "payload": payload,
                "timestamp": utc_now(),
            })

        def _write_memory(self, scope: str, title: str, content: str, provenance: dict[str, Any]) -> None:
            self.store.collection("memory_items").append({
                "id": f"mem_{uuid.uuid4().hex[:12]}",
                "scope": scope,
                "title": title,
                "content": content,
                "provenance": provenance,
                "created_at": utc_now(),
            })

        def governance_preview(self, workflow: dict[str, Any], requested_by: AuthenticatedUser) -> dict[str, Any]:
            risk_tier = workflow["risk_tier"]
            gated_steps = [step["id"] for step in workflow["steps"] if step["human_gate_required"]]
            return {
                "workflow_id": workflow["id"],
                "risk_tier": risk_tier,
                "requested_by": requested_by.id,
                "human_gate_steps": gated_steps,
                "approval_required": len(gated_steps) > 0,
                "policy_summary": workflow["guardrails"]["human_approval_required_if"],
            }

        def start_workflow_run(self, workflow_id: str, requested_by: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
            self.assert_permission(requested_by, "workflows:execute")
            workflow = self.get_workflow(workflow_id)
            run = {
                "id": f"run_{uuid.uuid4().hex[:12]}",
                "workflow_id": workflow_id,
                "workflow_name": workflow["name"],
                "status": "running",
                "risk_tier": workflow["risk_tier"],
                "requested_by": requested_by.id,
                "created_at": utc_now(),
                "updated_at": utc_now(),
                "current_step_index": 0,
                "input_payload": payload,
                "steps": [],
                "approval_request_id": None,
                "result": None,
            }
            self.store.collection("workflow_runs").append(run)
            self._append_audit("workflow_run", "created", {"run_id": run["id"], "workflow_id": workflow_id, "requested_by": requested_by.id})
            self._execute_run(run)
            self.store.save()
            return deepcopy(run)

        def _execute_run(self, run: dict[str, Any]) -> None:
            workflow = self.get_workflow(run["workflow_id"])
            while run["current_step_index"] < len(workflow["steps"]):
                step = workflow["steps"][run["current_step_index"]]
                if step["human_gate_required"] and not self._is_step_approved(run, step["id"]):
                    approval = self._create_approval(run, step)
                    run["status"] = "waiting_for_approval"
                    run["approval_request_id"] = approval["id"]
                    run["updated_at"] = utc_now()
                    self._append_audit("approval", "requested", {"run_id": run["id"], "step_id": step["id"], "approval_id": approval["id"]})
                    return

                step_result = {
                    "id": step["id"],
                    "state": step["state"],
                    "agent": step["agent"],
                    "tools": step["tools"],
                    "status": "completed",
                    "completed_at": utc_now(),
                }
                run["steps"].append(step_result)
                self._append_audit("workflow_step", "completed", {"run_id": run["id"], "step_id": step["id"], "agent": step["agent"]})
                self._write_memory("decision-memory", f"Run {run['id']} step {step['id']}", f"Completed step {step['id']} using {', '.join(step['tools'])}.", workflow["provenance"])
                run["current_step_index"] += 1
                run["updated_at"] = utc_now()

            run["status"] = "completed"
            run["approval_request_id"] = None
            run["result"] = {
                "outcome": "completed",
                "step_count": len(run["steps"]),
                "audit_log_complete": True,
            }
            self._create_evaluation(run)
            self._append_audit("workflow_run", "completed", {"run_id": run["id"], "workflow_id": run["workflow_id"]})

        def _create_approval(self, run: dict[str, Any], step: dict[str, Any]) -> dict[str, Any]:
            existing = next((item for item in self.store.collection("approvals") if item["run_id"] == run["id"] and item["step_id"] == step["id"] and item["status"] == "pending"), None)
            if existing:
                return existing
            approval = {
                "id": f"apr_{uuid.uuid4().hex[:12]}",
                "run_id": run["id"],
                "workflow_id": run["workflow_id"],
                "step_id": step["id"],
                "risk_tier": run["risk_tier"],
                "status": "pending",
                "requested_at": utc_now(),
                "requested_reason": f"Human gate required for step {step['id']}",
                "decided_at": None,
                "decided_by": None,
                "decision": None,
            }
            self.store.collection("approvals").append(approval)
            return approval

        def _is_step_approved(self, run: dict[str, Any], step_id: str) -> bool:
            return any(item["run_id"] == run["id"] and item["step_id"] == step_id and item["status"] == "approved" for item in self.store.collection("approvals"))

        def decide_approval(self, approval_id: str, decision: str, decided_by: AuthenticatedUser) -> dict[str, Any]:
            self.assert_permission(decided_by, "approvals:decide")
            approval = next((item for item in self.store.collection("approvals") if item["id"] == approval_id), None)
            if not approval:
                raise NotFoundError(f"Approval not found: {approval_id}")
            if approval["status"] != "pending":
                return deepcopy(approval)
            if decision not in {"approved", "rejected"}:
                raise PermissionDeniedError("Decision must be approved or rejected")
            approval["status"] = decision
            approval["decided_at"] = utc_now()
            approval["decided_by"] = decided_by.id
            approval["decision"] = decision
            run = self.get_run(approval["run_id"])
            if decision == "approved":
                run["status"] = "running"
                run["updated_at"] = utc_now()
                self._append_audit("approval", "approved", {"approval_id": approval["id"], "run_id": run["id"], "decided_by": decided_by.id})
                self._execute_run(run)
            else:
                run["status"] = "rejected"
                run["updated_at"] = utc_now()
                run["result"] = {"outcome": "rejected", "reason": f"Approval {approval_id} rejected"}
                self._append_audit("approval", "rejected", {"approval_id": approval["id"], "run_id": run["id"], "decided_by": decided_by.id})
            self.store.save()
            return deepcopy(approval)

        def create_memory_item(self, requested_by: AuthenticatedUser, scope: str, title: str, content: str) -> dict[str, Any]:
            self.assert_permission(requested_by, "memory:write")
            item = {
                "id": f"mem_{uuid.uuid4().hex[:12]}",
                "scope": scope,
                "title": title,
                "content": content,
                "provenance": {"source_refs": ["api"], "captured_by": requested_by.id, "recorded_at": utc_now()},
                "created_at": utc_now(),
            }
            self.store.collection("memory_items").append(item)
            self._append_audit("memory", "created", {"memory_id": item["id"], "scope": scope, "requested_by": requested_by.id})
            self.store.save()
            return deepcopy(item)

        def search_memory(self, query: str | None = None, scope: str | None = None) -> list[dict[str, Any]]:
            items = self.store.collection("memory_items")
            results = []
            for item in items:
                if scope and item["scope"] != scope:
                    continue
                if query and query.lower() not in f"{item['title']} {item['content']}".lower():
                    continue
                results.append(item)
            return deepcopy(results)

        def search_knowledge(self, query: str | None = None) -> list[dict[str, Any]]:
            documents = self.store.collection("knowledge_documents")
            if not query:
                return deepcopy(documents)
            return deepcopy([doc for doc in documents if query.lower() in f"{doc['title']} {doc['content']}".lower()])

        def list_evaluations(self) -> list[dict[str, Any]]:
            return deepcopy(self.store.collection("evaluation_runs"))

        def _create_evaluation(self, run: dict[str, Any]) -> None:
            seed = self.loader.load_eval_card()
            evaluation = {
                "id": f"eval_{uuid.uuid4().hex[:12]}",
                "run_id": run["id"],
                "workflow_id": run["workflow_id"],
                "target": run["workflow_id"],
                "eval_type": seed["eval_type"],
                "test_set": seed["test_set"],
                "metrics": deepcopy(seed["metrics"]),
                "result": "pass" if run["status"] == "completed" else "blocked",
                "promotion_decision": "canary_only" if run["status"] == "completed" else "blocked",
                "reviewer": "evaluation_harness",
                "created_at": utc_now(),
            }
            self.store.collection("evaluation_runs").append(evaluation)

        def process_summary(self) -> dict[str, Any]:
            runs = self.store.collection("workflow_runs")
            completed = [run for run in runs if run["status"] == "completed"]
            waiting = [run for run in runs if run["status"] == "waiting_for_approval"]
            return {
                "processes": deepcopy(self.store.collection("process_metrics")),
                "workflow_run_count": len(runs),
                "completed_run_count": len(completed),
                "waiting_for_approval_count": len(waiting),
                "audit_event_count": len(self.store.collection("audit_logs")),
                "memory_item_count": len(self.store.collection("memory_items")),
            }

        def settings(self) -> dict[str, Any]:
            return {
                "api_version": "v1",
                "runtime_mode": "local-json-store",
                "streaming": "sse",
                "governance": self.loader.load_risk_tiers(),
                "business_source_dir": "business/",
            }

        def stream_run_events(self, run_id: str) -> list[dict[str, Any]]:
            self.get_run(run_id)
            events = [item for item in self.store.collection("audit_logs") if item["payload"].get("run_id") == run_id]
            return deepcopy(events)


    runtime = RuntimeServices()
    """

    files["app/core/__init__.py"] = """\"\"\"Core helpers.\"\"\""""
    files["app/core/config.py"] = """
    from __future__ import annotations

    from dataclasses import dataclass
    import os


    @dataclass(slots=True)
    class Settings:
        app_name: str = os.getenv("GENERIC_SWARM_APP_NAME", "generic-swarm-ops-backend")
        api_prefix: str = os.getenv("GENERIC_SWARM_API_PREFIX", "/api/v1")
        environment: str = os.getenv("GENERIC_SWARM_ENV", "development")


    settings = Settings()
    """
    files["app/core/errors.py"] = """
    from app.runtime import ApprovalRequiredError, NotFoundError, PermissionDeniedError, RuntimeErrorBase

    __all__ = ["ApprovalRequiredError", "NotFoundError", "PermissionDeniedError", "RuntimeErrorBase"]
    """
    files["app/core/auth.py"] = """
    from __future__ import annotations

    from app.runtime import AuthenticatedUser, runtime


    def authenticate_bearer_token(token: str | None) -> AuthenticatedUser:
        return runtime.authenticate(token)
    """
    files["app/core/permissions.py"] = """
    from app.runtime import ROLE_PERMISSIONS


    def allowed_permissions(role: str) -> set[str]:
        return ROLE_PERMISSIONS.get(role, set())
    """
    files["app/core/logging.py"] = """
    import logging


    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    logger = logging.getLogger("generic-swarm-ops-backend")
    """
    files["app/core/security.py"] = """
    from app.core.auth import authenticate_bearer_token

    __all__ = ["authenticate_bearer_token"]
    """
    files["app/core/pagination.py"] = """
    def paginate(items: list, limit: int = 100, offset: int = 0) -> list:
        return items[offset: offset + limit]
    """
    files["app/core/idempotency.py"] = """
    from hashlib import sha256
    import json


    def request_fingerprint(payload: dict) -> str:
        return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    """
    files["app/core/rate_limit.py"] = """
    def rate_limit_hint() -> dict[str, int]:
        return {"requests_per_minute": 120}
    """

    files["app/api/__init__.py"] = """\"\"\"API package.\"\"\""""
    files["app/api/dependencies.py"] = """
    from __future__ import annotations

    from fastapi import Depends, Header

    from app.core.auth import authenticate_bearer_token
    from app.runtime import AuthenticatedUser, runtime


    def get_runtime():
        return runtime


    def get_current_user(authorization: str | None = Header(default=None)) -> AuthenticatedUser:
        if not authorization or not authorization.startswith("Bearer "):
            return authenticate_bearer_token(None)
        token = authorization.split(" ", 1)[1]
        return authenticate_bearer_token(token)
    """
    files["app/api/errors.py"] = """
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse

    from app.core.errors import RuntimeErrorBase


    def register_error_handlers(app: FastAPI) -> None:
        @app.exception_handler(RuntimeErrorBase)
        async def runtime_error_handler(_: Request, exc: RuntimeErrorBase):
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
    """
    files["app/api/v1/__init__.py"] = """\"\"\"Version 1 API.\"\"\""""
    files["app/api/v1/router.py"] = """
    from fastapi import APIRouter

    from app.api.v1.routes import approvals, agents, audit_logs, auth, evaluations, governance, health, knowledge, memory, organizations, processes, settings, tools, users, workflow_runs, workflows

    api_router = APIRouter()
    api_router.include_router(health.router, prefix="/health", tags=["health"])
    api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
    api_router.include_router(users.router, prefix="/users", tags=["users"])
    api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
    api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
    api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
    api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
    api_router.include_router(workflow_runs.router, prefix="/workflow-runs", tags=["workflow-runs"])
    api_router.include_router(approvals.router, prefix="/approvals", tags=["approvals"])
    api_router.include_router(governance.router, prefix="/governance", tags=["governance"])
    api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
    api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
    api_router.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
    api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])
    api_router.include_router(processes.router, prefix="/processes", tags=["processes"])
    api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
    """

    files["app/schemas/__init__.py"] = """\"\"\"Pydantic schemas.\"\"\""""
    files["app/schemas/common.py"] = """
    from __future__ import annotations

    from typing import Any

    from pydantic import BaseModel, Field


    class MessageResponse(BaseModel):
        message: str


    class LoginRequest(BaseModel):
        email: str


    class WorkflowStartRequest(BaseModel):
        input_payload: dict[str, Any] = Field(default_factory=dict)


    class ApprovalDecisionRequest(BaseModel):
        decision: str


    class MemoryCreateRequest(BaseModel):
        scope: str
        title: str
        content: str
    """

    reexport_modules = {
        "auth.py": "from app.schemas.common import LoginRequest\n",
        "users.py": "from app.schemas.common import MessageResponse\n",
        "organizations.py": "from app.schemas.common import MessageResponse\n",
        "agents.py": "from app.schemas.common import MessageResponse\n",
        "tools.py": "from app.schemas.common import MessageResponse\n",
        "workflows.py": "from app.schemas.common import WorkflowStartRequest\n",
        "workflow_runs.py": "from app.schemas.common import MessageResponse\n",
        "approvals.py": "from app.schemas.common import ApprovalDecisionRequest\n",
        "governance.py": "from app.schemas.common import MessageResponse\n",
        "knowledge.py": "from app.schemas.common import MessageResponse\n",
        "memory.py": "from app.schemas.common import MemoryCreateRequest\n",
        "evaluations.py": "from app.schemas.common import MessageResponse\n",
        "audit_logs.py": "from app.schemas.common import MessageResponse\n",
        "processes.py": "from app.schemas.common import MessageResponse\n",
    }
    for name, content in reexport_modules.items():
        files[f"app/schemas/{name}"] = content

    files["app/services/__init__.py"] = """\"\"\"Service package.\"\"\""""
    service_modules = {
        "auth_service.py": """
        from app.runtime import runtime


        def login(email: str) -> dict:
            return runtime.issue_token(email)
        """,
        "user_service.py": """
        from app.runtime import runtime


        def list_users() -> list[dict]:
            return runtime.list_collection("users")
        """,
        "organization_service.py": """
        from app.runtime import runtime


        def list_organizations() -> list[dict]:
            return runtime.list_collection("organizations")
        """,
        "agent_service.py": """
        from app.runtime import runtime


        def list_agents() -> list[dict]:
            return runtime.list_collection("agents")
        """,
        "tool_service.py": """
        from app.runtime import runtime


        def list_tools() -> list[dict]:
            return runtime.list_collection("tools")
        """,
        "workflow_service.py": """
        from app.runtime import runtime


        def list_workflows() -> list[dict]:
            return runtime.list_collection("workflows")


        def get_workflow(workflow_id: str) -> dict:
            return runtime.get_workflow(workflow_id)
        """,
        "workflow_run_service.py": """
        from app.runtime import AuthenticatedUser, runtime


        def list_runs() -> list[dict]:
            return runtime.list_collection("workflow_runs")


        def get_run(run_id: str) -> dict:
            return runtime.get_run(run_id)


        def start_run(workflow_id: str, requested_by: AuthenticatedUser, payload: dict) -> dict:
            return runtime.start_workflow_run(workflow_id, requested_by, payload)
        """,
        "governance_service.py": """
        from app.runtime import AuthenticatedUser, runtime


        def preview(workflow_id: str, requested_by: AuthenticatedUser) -> dict:
            workflow = runtime.get_workflow(workflow_id)
            return runtime.governance_preview(workflow, requested_by)
        """,
        "approval_service.py": """
        from app.runtime import AuthenticatedUser, runtime


        def list_approvals() -> list[dict]:
            return runtime.list_collection("approvals")


        def decide(approval_id: str, decision: str, decided_by: AuthenticatedUser) -> dict:
            return runtime.decide_approval(approval_id, decision, decided_by)
        """,
        "knowledge_service.py": """
        from app.runtime import runtime


        def search(query: str | None = None) -> list[dict]:
            return runtime.search_knowledge(query)
        """,
        "memory_service.py": """
        from app.runtime import AuthenticatedUser, runtime


        def search(query: str | None = None, scope: str | None = None) -> list[dict]:
            return runtime.search_memory(query=query, scope=scope)


        def create(requested_by: AuthenticatedUser, scope: str, title: str, content: str) -> dict:
            return runtime.create_memory_item(requested_by, scope, title, content)
        """,
        "evaluation_service.py": """
        from app.runtime import runtime


        def list_evaluations() -> list[dict]:
            return runtime.list_evaluations()
        """,
        "audit_service.py": """
        from app.runtime import runtime


        def list_audit_logs() -> list[dict]:
            return runtime.list_collection("audit_logs")


        def stream_run_events(run_id: str) -> list[dict]:
            return runtime.stream_run_events(run_id)
        """,
        "process_service.py": """
        from app.runtime import runtime


        def summary() -> dict:
            return runtime.process_summary()
        """,
        "notification_service.py": """
        from app.runtime import runtime


        def list_notifications() -> list[dict]:
            return runtime.list_collection("notifications")
        """,
    }
    files.update({f"app/services/{name}": content for name, content in service_modules.items()})

    files["app/main.py"] = """
    from __future__ import annotations

    from fastapi import FastAPI

    from app.api.errors import register_error_handlers
    from app.api.v1.router import api_router
    from app.core.config import settings

    app = FastAPI(title=settings.app_name, version="0.1.0", openapi_url=f"{settings.api_prefix}/openapi.json")
    register_error_handlers(app)
    app.include_router(api_router, prefix=settings.api_prefix)
    """

    route_files = {
        "health.py": """
        from fastapi import APIRouter

        router = APIRouter()


        @router.get("")
        def health() -> dict:
            return {"status": "ok", "service": "generic-swarm-ops-backend"}
        """,
        "auth.py": """
        from fastapi import APIRouter

        from app.schemas.auth import LoginRequest
        from app.services.auth_service import login

        router = APIRouter()


        @router.post("/login")
        def login_route(payload: LoginRequest) -> dict:
            return login(payload.email)
        """,
        "users.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.user_service import list_users

        router = APIRouter()


        @router.get("")
        def users_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "users:read")
            return list_users()
        """,
        "organizations.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.organization_service import list_organizations

        router = APIRouter()


        @router.get("")
        def organizations_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "organizations:read")
            return list_organizations()
        """,
        "agents.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.agent_service import list_agents

        router = APIRouter()


        @router.get("")
        def agents_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "agents:read")
            return list_agents()
        """,
        "tools.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.tool_service import list_tools

        router = APIRouter()


        @router.get("")
        def tools_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "tools:read")
            return list_tools()
        """,
        "workflows.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.schemas.workflows import WorkflowStartRequest
        from app.services.workflow_run_service import start_run
        from app.services.workflow_service import get_workflow, list_workflows

        router = APIRouter()


        @router.get("")
        def workflows_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "workflows:read")
            return list_workflows()


        @router.get("/{workflow_id}")
        def workflow_detail_route(workflow_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            runtime.assert_permission(current_user, "workflows:read")
            return get_workflow(workflow_id)


        @router.post("/{workflow_id}/run")
        def workflow_run_route(workflow_id: str, payload: WorkflowStartRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            return start_run(workflow_id, current_user, payload.input_payload)
        """,
        "workflow_runs.py": """
        from __future__ import annotations

        import json
        from fastapi import APIRouter, Depends
        from fastapi.responses import StreamingResponse

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.audit_service import stream_run_events
        from app.services.workflow_run_service import get_run, list_runs

        router = APIRouter()


        @router.get("")
        def workflow_runs_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "workflows:read")
            return list_runs()


        @router.get("/{run_id}")
        def workflow_run_detail_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            runtime.assert_permission(current_user, "workflows:read")
            return get_run(run_id)


        @router.get("/{run_id}/stream")
        def workflow_run_stream_route(run_id: str, current_user: AuthenticatedUser = Depends(get_current_user)) -> StreamingResponse:
            runtime.assert_permission(current_user, "workflows:read")
            events = stream_run_events(run_id)

            def iter_events():
                for event in events:
                    yield f"data: {json.dumps(event)}\\n\\n"

            return StreamingResponse(iter_events(), media_type="text/event-stream")
        """,
        "approvals.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.schemas.approvals import ApprovalDecisionRequest
        from app.services.approval_service import decide, list_approvals

        router = APIRouter()


        @router.get("")
        def approvals_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "approvals:read")
            return list_approvals()


        @router.post("/{approval_id}/decision")
        def approval_decision_route(approval_id: str, payload: ApprovalDecisionRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            return decide(approval_id, payload.decision, current_user)
        """,
        "governance.py": """
        from fastapi import APIRouter, Depends, Query

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.governance_service import preview

        router = APIRouter()


        @router.get("/preview")
        def governance_preview_route(workflow_id: str = Query(...), current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            runtime.assert_permission(current_user, "governance:read")
            return preview(workflow_id, current_user)
        """,
        "knowledge.py": """
        from fastapi import APIRouter, Depends, Query

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.knowledge_service import search

        router = APIRouter()


        @router.get("")
        def knowledge_route(query: str | None = Query(default=None), current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "knowledge:read")
            return search(query)
        """,
        "memory.py": """
        from fastapi import APIRouter, Depends, Query

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.schemas.memory import MemoryCreateRequest
        from app.services.memory_service import create, search

        router = APIRouter()


        @router.get("")
        def memory_route(query: str | None = Query(default=None), scope: str | None = Query(default=None), current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "memory:read")
            return search(query=query, scope=scope)


        @router.post("")
        def create_memory_route(payload: MemoryCreateRequest, current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            return create(current_user, payload.scope, payload.title, payload.content)
        """,
        "evaluations.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.evaluation_service import list_evaluations

        router = APIRouter()


        @router.get("")
        def evaluations_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "evaluations:read")
            return list_evaluations()
        """,
        "audit_logs.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.audit_service import list_audit_logs

        router = APIRouter()


        @router.get("")
        def audit_logs_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
            runtime.assert_permission(current_user, "audit:read")
            return list_audit_logs()
        """,
        "processes.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime
        from app.services.process_service import summary

        router = APIRouter()


        @router.get("/summary")
        def processes_summary_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            runtime.assert_permission(current_user, "processes:read")
            return summary()
        """,
        "settings.py": """
        from fastapi import APIRouter, Depends

        from app.api.dependencies import get_current_user
        from app.runtime import AuthenticatedUser, runtime

        router = APIRouter()


        @router.get("")
        def settings_route(current_user: AuthenticatedUser = Depends(get_current_user)) -> dict:
            runtime.assert_permission(current_user, "settings:read")
            return runtime.settings()
        """,
    }
    for name, content in route_files.items():
        files[f"app/api/v1/routes/{name}"] = content

    files["app/api/v1/routes/__init__.py"] = """
    \"\"\"Route modules.\"\"\"
    """

    domain_stub = """
    \"\"\"Generated domain module.\"\"\"
    """
    domain_files = [
        "app/domain/__init__.py",
        "app/domain/agents/models.py",
        "app/domain/agents/policies.py",
        "app/domain/agents/runtime.py",
        "app/domain/workflows/models.py",
        "app/domain/workflows/engine.py",
        "app/domain/workflows/states.py",
        "app/domain/workflows/policies.py",
        "app/domain/governance/models.py",
        "app/domain/governance/policy_engine.py",
        "app/domain/governance/risk.py",
        "app/domain/approvals/models.py",
        "app/domain/approvals/service.py",
        "app/domain/knowledge/models.py",
        "app/domain/knowledge/chunking.py",
        "app/domain/knowledge/retrieval.py",
        "app/domain/memory/models.py",
        "app/domain/memory/scopes.py",
        "app/domain/memory/retrieval.py",
        "app/domain/evaluations/models.py",
        "app/domain/evaluations/evaluators.py",
        "app/domain/audit/models.py",
        "app/domain/audit/events.py",
        "app/domain/processes/analytics.py",
    ]
    for relative_path in domain_files:
        files[relative_path] = domain_stub

    infrastructure_files = {
        "app/infrastructure/__init__.py": domain_stub,
        "app/infrastructure/database/__init__.py": domain_stub,
        "app/infrastructure/database/session.py": """
        def get_session() -> None:
            return None
        """,
        "app/infrastructure/database/models.py": domain_stub,
        "app/infrastructure/repositories/user_repository.py": """
        from app.runtime import runtime


        def list_users():
            return runtime.list_collection("users")
        """,
        "app/infrastructure/repositories/agent_repository.py": """
        from app.runtime import runtime


        def list_agents():
            return runtime.list_collection("agents")
        """,
        "app/infrastructure/repositories/workflow_repository.py": """
        from app.runtime import runtime


        def list_workflows():
            return runtime.list_collection("workflows")
        """,
        "app/infrastructure/repositories/workflow_run_repository.py": """
        from app.runtime import runtime


        def list_runs():
            return runtime.list_collection("workflow_runs")
        """,
        "app/infrastructure/repositories/approval_repository.py": """
        from app.runtime import runtime


        def list_approvals():
            return runtime.list_collection("approvals")
        """,
        "app/infrastructure/repositories/knowledge_repository.py": """
        from app.runtime import runtime


        def list_knowledge():
            return runtime.list_collection("knowledge_documents")
        """,
        "app/infrastructure/repositories/memory_repository.py": """
        from app.runtime import runtime


        def list_memory():
            return runtime.list_collection("memory_items")
        """,
        "app/infrastructure/repositories/audit_repository.py": """
        from app.runtime import runtime


        def list_audit_logs():
            return runtime.list_collection("audit_logs")
        """,
        "app/infrastructure/vector_store/__init__.py": domain_stub,
        "app/infrastructure/vector_store/base.py": """
        class BaseVectorStore:
            pass
        """,
        "app/infrastructure/vector_store/pgvector_store.py": """
        from app.infrastructure.vector_store.base import BaseVectorStore


        class PgVectorStore(BaseVectorStore):
            pass
        """,
        "app/infrastructure/vector_store/qdrant_store.py": """
        from app.infrastructure.vector_store.base import BaseVectorStore


        class QdrantStore(BaseVectorStore):
            pass
        """,
        "app/infrastructure/object_storage/__init__.py": domain_stub,
        "app/infrastructure/object_storage/base.py": """
        class BaseObjectStorage:
            pass
        """,
        "app/infrastructure/object_storage/s3_storage.py": """
        from app.infrastructure.object_storage.base import BaseObjectStorage


        class S3Storage(BaseObjectStorage):
            pass
        """,
        "app/infrastructure/object_storage/local_storage.py": """
        from app.infrastructure.object_storage.base import BaseObjectStorage


        class LocalStorage(BaseObjectStorage):
            pass
        """,
        "app/infrastructure/queue/__init__.py": domain_stub,
        "app/infrastructure/queue/broker.py": """
        class QueueBroker:
            def publish(self, name: str, payload: dict) -> dict:
                return {"queue": name, "payload": payload}
        """,
        "app/infrastructure/queue/tasks.py": """
        def enqueue(name: str, payload: dict) -> dict:
            return {"task": name, "payload": payload}
        """,
        "app/infrastructure/llm/__init__.py": domain_stub,
        "app/infrastructure/llm/base.py": """
        class BaseLLMProvider:
            pass
        """,
        "app/infrastructure/llm/openai_provider.py": """
        from app.infrastructure.llm.base import BaseLLMProvider


        class OpenAIProvider(BaseLLMProvider):
            pass
        """,
        "app/infrastructure/llm/mock_provider.py": """
        from app.infrastructure.llm.base import BaseLLMProvider


        class MockProvider(BaseLLMProvider):
            pass
        """,
        "app/infrastructure/integrations/__init__.py": domain_stub,
        "app/infrastructure/integrations/email.py": """
        def send_email(payload: dict) -> dict:
            return {"status": "queued", "payload": payload}
        """,
        "app/infrastructure/integrations/crm.py": """
        def create_customer(payload: dict) -> dict:
            return {"status": "mocked", "payload": payload}
        """,
        "app/infrastructure/integrations/calendar.py": """
        def create_calendar_event(payload: dict) -> dict:
            return {"status": "mocked", "payload": payload}
        """,
    }
    files.update(infrastructure_files)

    files["app/workers/__init__.py"] = domain_stub
    files["app/workers/workflow_worker.py"] = """
    from app.runtime import runtime


    def run_pending() -> list[dict]:
        pending = []
        for run in runtime.list_collection("workflow_runs"):
            if run["status"] == "running":
                pending.append(run)
        return pending
    """
    files["app/workers/knowledge_worker.py"] = """
    from app.runtime import runtime


    def refresh_knowledge_index() -> int:
        return len(runtime.list_collection("knowledge_documents"))
    """
    files["app/workers/evaluation_worker.py"] = """
    from app.runtime import runtime


    def refresh_evaluations() -> int:
        return len(runtime.list_collection("evaluation_runs"))
    """
    files["app/workers/memory_worker.py"] = """
    from app.runtime import runtime


    def compact_memory() -> int:
        return len(runtime.list_collection("memory_items"))
    """

    files["app/tests/unit/test_runtime.py"] = """
    import sys
    import unittest
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

    from app.runtime import runtime


    class RuntimeSmokeTests(unittest.TestCase):
        def test_seeded_workflow_exists(self):
            workflows = runtime.list_collection("workflows")
            self.assertTrue(any(item["id"] == "wf_customer_onboarding_v12" for item in workflows))

        def test_process_summary_has_counts(self):
            summary = runtime.process_summary()
            self.assertIn("workflow_run_count", summary)
            self.assertIn("processes", summary)


    if __name__ == "__main__":
        unittest.main()
    """
    files["app/tests/integration/__init__.py"] = domain_stub
    files["app/tests/e2e/__init__.py"] = domain_stub
    files["app/tests/security/__init__.py"] = domain_stub
    files["app/tests/load/__init__.py"] = domain_stub

    files["scripts/seed.py"] = """
    from app.runtime import runtime


    if __name__ == "__main__":
        print({"organizations": len(runtime.list_collection("organizations")), "users": len(runtime.list_collection("users"))})
    """
    files["scripts/create_admin.py"] = """
    if __name__ == "__main__":
        print({"email": "admin@example.com", "token": "admin-token"})
    """
    files["scripts/migrate.py"] = """
    if __name__ == "__main__":
        print({"status": "noop", "message": "JSON-backed runtime store does not require migrations in the initial implementation."})
    """

    return files


def main() -> None:
    files = build_files()
    for relative_path, content in files.items():
        write(relative_path, content)
    print(f"Generated {len(files)} backend file(s)")


if __name__ == "__main__":
    main()
