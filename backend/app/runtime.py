from __future__ import annotations

import hashlib
import json
import threading
import uuid
from contextvars import ContextVar
from copy import deepcopy
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CURRENT_REQUEST_ID: ContextVar[str | None] = ContextVar("current_request_id", default=None)


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _sanitize_product_name_str(value: str) -> str:
    return (
        value.replace("genetic-swarm-ops", "generic-swarm-ops")
        .replace("GENETIC_SWARM", "GENERIC_SWARM")
        .replace("Genetic Swarm", "Generic Swarm")
    )


def sanitize_legacy_product_names(value: Any) -> Any:
    """Rewrite legacy typo product names (genetic → generic) in runtime state.

    Historical absolute paths and env prefixes used ``genetic-swarm-ops`` /
    ``GENETIC_SWARM_*``. Postgres snapshots can rehydrate those strings into
    ``runtime.json`` on save; scrub on load and save so product surfaces stay clean.
    """
    if isinstance(value, str):
        return _sanitize_product_name_str(value)
    if isinstance(value, list):
        return [sanitize_legacy_product_names(item) for item in value]
    if isinstance(value, dict):
        return {key: sanitize_legacy_product_names(item) for key, item in value.items()}
    return value


def sanitize_legacy_product_names_inplace(value: Any) -> None:
    """In-place scrub so RuntimeStore collection list identities stay stable."""
    if isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, str):
                value[index] = _sanitize_product_name_str(item)
            else:
                sanitize_legacy_product_names_inplace(item)
        return
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if isinstance(item, str):
                value[key] = _sanitize_product_name_str(item)
            else:
                sanitize_legacy_product_names_inplace(item)



def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def hash_password(value: str, *, salt: str | None = None) -> str:
    """PBKDF2-HMAC-SHA256 password hash (local-prod profile). Format: pbkdf2$iterations$salt$hex."""
    iterations = 120_000
    salt_bytes = (salt or uuid.uuid4().hex).encode("utf-8")
    digest = hashlib.pbkdf2_hmac("sha256", value.encode("utf-8"), salt_bytes, iterations)
    return f"pbkdf2${iterations}${salt_bytes.decode('utf-8')}${digest.hex()}"


def verify_password(value: str, stored: str) -> bool:
    if not stored:
        return False
    # Legacy SHA-256 (migration path for existing runtime.json seeds)
    if not stored.startswith("pbkdf2$"):
        return hashlib.sha256(value.encode("utf-8")).hexdigest() == stored
    try:
        _prefix, iterations_s, salt, digest_hex = stored.split("$", 3)
        iterations = int(iterations_s)
    except ValueError:
        return False
    candidate = hashlib.pbkdf2_hmac("sha256", value.encode("utf-8"), salt.encode("utf-8"), iterations).hex()
    return candidate == digest_hex


class RuntimeErrorBase(Exception):
    status_code = 400
    error_code = "bad_request"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(RuntimeErrorBase):
    status_code = 404
    error_code = "not_found"


class PermissionDeniedError(RuntimeErrorBase):
    status_code = 403
    error_code = "permission_denied"


class ApprovalRequiredError(RuntimeErrorBase):
    status_code = 409
    error_code = "approval_required"


class ValidationError(RuntimeErrorBase):
    status_code = 422
    error_code = "validation_error"


class RateLimitedError(RuntimeErrorBase):
    status_code = 429
    error_code = "rate_limited"

    def __init__(self, message: str, retry_after: int):
        super().__init__(message)
        self.retry_after = retry_after


@dataclass(slots=True)
class AuthenticatedUser:
    id: str
    organization_id: str
    email: str
    name: str
    role: str


ROLE_PERMISSIONS = {
    "owner": {"*"},
    "admin": {
        "users:read", "users:create", "users:update", "users:invite",
        "organizations:read", "organizations:update",
        "agents:read", "agents:create", "agents:update",
        "tools:read", "tools:create", "tools:update",
        "workflows:read", "workflows:create", "workflows:update", "workflows:execute",
        "workflow_runs:read", "workflow_runs:cancel", "workflow_runs:retry", "workflow_runs:dispatch",
        "approvals:read", "approvals:approve", "approvals:reject",
        "governance:read", "governance:update",
        "knowledge:read", "knowledge:write",
        "memory:read", "memory:write",
        "evaluations:read",
        "audit:read",
        "processes:read",
        "settings:read", "settings:update",
    },
    "manager": {
        "users:read",
        "agents:read",
        "tools:read",
        "workflows:read", "workflows:execute",
        "workflow_runs:read",
        "approvals:read", "approvals:approve", "approvals:reject",
        "governance:read",
        "knowledge:read", "knowledge:write",
        "memory:read", "memory:write",
        "evaluations:read",
        "audit:read",
        "processes:read",
        "settings:read",
    },
    "operator": {
        "agents:read",
        "tools:read",
        "workflows:read", "workflows:execute",
        "workflow_runs:read", "workflow_runs:cancel", "workflow_runs:retry",
        "approvals:read",
        "governance:read",
        "knowledge:read",
        "memory:read", "memory:write",
        "evaluations:read",
        "audit:read",
        "processes:read",
    },
    "reviewer": {
        "agents:read",
        "tools:read",
        "workflows:read",
        "workflow_runs:read",
        "approvals:read", "approvals:approve", "approvals:reject",
        "governance:read",
        "knowledge:read",
        "memory:read",
        "evaluations:read",
        "audit:read",
        "processes:read",
    },
    "viewer": {
        "agents:read",
        "tools:read",
        "workflows:read",
        "workflow_runs:read",
        "approvals:read",
        "governance:read",
        "knowledge:read",
        "memory:read",
        "evaluations:read",
        "audit:read",
        "processes:read",
        "settings:read",
    },
    "service_account": {
        "workflows:read", "workflows:execute",
        "workflow_runs:read",
        "knowledge:read",
        "memory:read", "memory:write",
        "governance:read",
        "evaluations:read",
        "processes:read",
    },
}


def _empty_runtime_state() -> dict[str, Any]:
    return {
        "organizations": [],
        "users": [],
        "agents": [],
        "tools": [],
        "workflows": [],
        "workflow_runs": [],
        "approvals": [],
        "audit_logs": [],
        "stream_events": [],
        "memory_items": [],
        "evaluation_runs": [],
        "knowledge_documents": [],
        "governance_policies": [],
        "notifications": [],
        "process_metrics": [],
        "event_logs": [],
        "evolution_variants": [],
        "tool_effects": [],
        "pi_artifacts": [],
        "improvement_lessons": [],
        "loop_runs": [],
        "knowledge_nodes": [],
        "knowledge_edges": [],
        "skill_proposals": [],
        "user_invitations": [],
        "access_tokens": {},
        "refresh_tokens": {},
        "api_keys": {},
    }


class RuntimeStore:
    """Persistent runtime document store.

    Prefer Postgres when ``DATABASE_URL`` is set in ``backend/.env`` (JSONB document).
    Falls back to ``backend/data/runtime.json`` when Postgres is disabled or forced off.
    """

    def __init__(self, data_file: Path):
        from app.core.config import settings as app_settings

        self.data_file = data_file
        self.lock = threading.RLock()
        self.settings = app_settings
        self.backend = "json-file"
        self.state = self._load()

    def _ensure_postgres_schema(self, conn) -> None:
        from sqlalchemy import text

        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS runtime_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    payload JSONB NOT NULL,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )

    def _load_from_postgres(self) -> dict[str, Any] | None:
        from sqlalchemy import text

        from app.infrastructure.database.session import get_engine

        engine = get_engine()
        if engine is None:
            return None
        try:
            with engine.begin() as conn:
                self._ensure_postgres_schema(conn)
                row = conn.execute(text("SELECT payload FROM runtime_state WHERE id = 1")).first()
                if row and row[0] is not None:
                    payload = row[0]
                    if isinstance(payload, str):
                        return json.loads(payload)
                    if isinstance(payload, dict):
                        return payload
                    return dict(payload)
                # Seed from existing JSON file if present (one-time migrate into Postgres)
                if self.data_file.exists():
                    payload = json.loads(self.data_file.read_text(encoding="utf-8"))
                else:
                    payload = _empty_runtime_state()
                conn.execute(
                    text(
                        """
                        INSERT INTO runtime_state (id, payload, updated_at)
                        VALUES (1, CAST(:payload AS jsonb), NOW())
                        ON CONFLICT (id) DO UPDATE
                        SET payload = EXCLUDED.payload, updated_at = NOW()
                        """
                    ),
                    {"payload": json.dumps(payload)},
                )
                return payload
        except Exception:
            # Fall back to JSON so local unit tests/dev still work if DB is down
            return None

    def _save_to_postgres(self) -> bool:
        from sqlalchemy import text

        from app.infrastructure.database.session import get_engine

        engine = get_engine()
        if engine is None:
            return False
        try:
            with engine.begin() as conn:
                self._ensure_postgres_schema(conn)
                conn.execute(
                    text(
                        """
                        INSERT INTO runtime_state (id, payload, updated_at)
                        VALUES (1, CAST(:payload AS jsonb), NOW())
                        ON CONFLICT (id) DO UPDATE
                        SET payload = EXCLUDED.payload, updated_at = NOW()
                        """
                    ),
                    {"payload": json.dumps(self.state)},
                )
            return True
        except Exception:
            return False

    def _load(self) -> dict[str, Any]:
        if self.settings.use_postgres:
            payload = self._load_from_postgres()
            if payload is not None:
                self.backend = "postgres"
                return sanitize_legacy_product_names(payload)
        # JSON fallback
        self.backend = "json-file"
        if self.data_file.exists():
            return sanitize_legacy_product_names(json.loads(self.data_file.read_text(encoding="utf-8")))
        default = _empty_runtime_state()
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data_file.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        return default

    def save(self) -> None:
        with self.lock:
            # In-place only — replacing self.state would break live collection() refs.
            sanitize_legacy_product_names_inplace(self.state)
            saved_pg = False
            if self.settings.use_postgres:
                saved_pg = self._save_to_postgres()
                if saved_pg:
                    self.backend = "postgres"
            # Always keep a JSON snapshot as offline backup / migrate source
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.data_file.write_text(json.dumps(self.state, indent=2) + "\n", encoding="utf-8")
            if not saved_pg and not self.settings.use_postgres:
                self.backend = "json-file"

    def collection(self, name: str) -> list[dict[str, Any]]:
        if name not in self.state:
            # Auto-create list collections for forward-compatible stores
            self.state[name] = []
        value = self.state[name]
        if not isinstance(value, list):
            raise TypeError(f"collection {name} is not a list")
        return value


class BusinessSourceLoader:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def read_json(self, relative_path: str) -> dict[str, Any]:
        return json.loads((self.repo_root / relative_path).read_text(encoding="utf-8"))

    def load_workflows(self, organization_id: str) -> list[dict[str, Any]]:
        workflow = self.read_json("business/examples/workflow-dna.example.json")
        workflow.update({
            "organization_id": organization_id,
            "description": workflow["objective"],
            "department": "operations",
            "status": "active",
            "input_schema": {
                "type": "object",
                "required": ["case_id"],
                "properties": {
                    "case_id": {"type": "string"},
                    "customer_name": {"type": "string"},
                },
            },
            "output_schema": {
                "type": "object",
                "required": ["outcome", "step_count"],
                "properties": {
                    "outcome": {"type": "string"},
                    "step_count": {"type": "number"},
                },
            },
            "evaluation_policy": {"required": True, "block_on_fail": True},
            "governance_policy": {"risk_tier": workflow["risk_tier"], "human_gate_steps": [step["id"] for step in workflow["steps"] if step["human_gate_required"]]},
            "active_version": workflow["version"],
            "versions": [{
                "version": workflow["version"],
                "status": "active",
                "created_at": utc_now(),
                "immutable": True,
                "steps": deepcopy(workflow["steps"]),
            }],
        })
        return [workflow]

    def load_agents(self, organization_id: str) -> list[dict[str, Any]]:
        seeds = [
            ("business_orchestrator", "Business Orchestrator", "control", "tier_4_execute_with_gate", ["crm", "billing_system", "email", "audit_log_writer"], ["workflow_memory", "organization_memory"]),
            ("quality_compliance_agent", "Quality Compliance Agent", "execution", "tier_2_draft", ["contract_parser", "policy_retriever"], ["organization_memory"]),
            ("execution_agent", "Execution Agent", "execution", "tier_3_execute_reversible", ["crm"], ["workflow_memory", "organization_memory"]),
            ("finance_ops_agent", "Finance Ops Agent", "execution", "tier_4_execute_with_gate", ["billing_system"], ["workflow_memory", "organization_memory", "department_memory"]),
            ("communications_agent", "Communications Agent", "execution", "tier_2_draft", ["email"], ["workflow_memory", "organization_memory"]),
        ]
        return [
            {
                "id": agent_id,
                "organization_id": organization_id,
                "name": name,
                "description": f"{name} runtime profile",
                "version": "1.0.0",
                "owner_user_id": "user_admin",
                "department": "operations",
                "allowed_tools": tools,
                "allowed_memory_scopes": scopes,
                "allowed_workflow_types": ["operations"],
                "risk_level": risk_tier,
                "runtime_configuration": {"mode": "local"},
                "status": "active",
                "role": role,
            }
            for agent_id, name, role, risk_tier, tools, scopes in seeds
        ]

    def load_tools(self, organization_id: str) -> list[dict[str, Any]]:
        register = self.read_json("business/security/tool-permissions/tool-permission-register.json")
        tools = []
        for entry in register["tool_permissions"]:
            tools.append({
                "id": entry["tool"],
                "organization_id": organization_id,
                "name": entry["tool"],
                "description": f"{entry['tool']} managed tool",
                "category": "internal_api",
                "input_schema": {"type": "object"},
                "output_schema": {"type": "object"},
                "risk_level": "tier_4_execute_with_gate" if entry["requires_human_gate_for"] else "tier_3_execute_reversible",
                "required_permissions": ["workflows:execute"],
                "approval_requirement": bool(entry["requires_human_gate_for"]),
                "timeout": 30,
                "retry_policy": {"max_retries": 1},
                "enabled": True,
                "allowed_actions": entry["allowed_actions"],
                "scope": entry["scope"],
            })
        # Ensure video pack stubs + core analysis tools exist even if register is partial
        existing_ids = {t["id"] for t in tools}
        for stub_id, actions, risk, gate in (
            ("audit_log_writer", ["write_audit"], "tier_1_recommend", False),
            ("contract_parser", ["parse_contract"], "tier_1_recommend", False),
            ("policy_retriever", ["retrieve_policy"], "tier_1_recommend", False),
            ("video_media_gen_stub", ["generate_media_stub"], "tier_3_execute_reversible", False),
            ("video_script_format", ["format_script"], "tier_3_execute_reversible", False),
            ("video_qc_stub", ["qc_pass"], "tier_3_execute_reversible", False),
            ("video_package_stub", ["package_deliverable"], "tier_4_execute_with_gate", True),
        ):
            if stub_id in existing_ids:
                continue
            tools.append({
                "id": stub_id,
                "organization_id": organization_id,
                "name": stub_id,
                "description": f"{stub_id} managed tool",
                "category": "video_stub" if stub_id.startswith("video_") else "internal_api",
                "input_schema": {"type": "object"},
                "output_schema": {"type": "object"},
                "risk_level": risk,
                "required_permissions": ["workflows:execute"],
                "approval_requirement": gate,
                "timeout": 30,
                "retry_policy": {"max_retries": 1},
                "enabled": True,
                "allowed_actions": actions,
                "scope": "video_pack_ci_stub" if stub_id.startswith("video_") else "platform",
            })
        return tools

    def load_knowledge_documents(self, organization_id: str) -> list[dict[str, Any]]:
        mapping = [
            ("docs/business-architecture.md", "business-architecture"),
            ("docs/process-intelligence.md", "process-intelligence"),
            ("docs/knowledge-memory.md", "knowledge-memory"),
            ("docs/workflow-dna.md", "workflow-dna"),
            ("docs/governance.md", "governance"),
            ("docs/evaluation.md", "evaluation"),
            ("docs/evolution-sandbox.md", "evolution-sandbox"),
        ]
        docs = []
        for relative_path, doc_id in mapping:
            path = self.repo_root / relative_path
            docs.append({
                "id": doc_id,
                "organization_id": organization_id,
                "title": path.stem,
                "path": relative_path.replace("\\", "/"),
                "content": path.read_text(encoding="utf-8"),
                "status": "indexed",
                "sensitivity": "internal",
                "allowed_roles": ["owner", "admin", "manager", "operator", "reviewer", "viewer", "service_account"],
                "created_at": utc_now(),
                "failure_reason": None,
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

    def _seed_users(self, organization_id: str) -> list[dict[str, Any]]:
        return [
            {"id": "user_owner", "organization_id": organization_id, "email": "owner@example.com", "name": "Owner", "role": "owner", "password_hash": hash_password("owner-password"), "status": "active", "department": "executive"},
            {"id": "user_admin", "organization_id": organization_id, "email": "admin@example.com", "name": "Admin", "role": "admin", "password_hash": hash_password("admin-password"), "status": "active", "department": "operations"},
            {"id": "user_operator", "organization_id": organization_id, "email": "operator@example.com", "name": "Operator", "role": "operator", "password_hash": hash_password("operator-password"), "status": "active", "department": "operations"},
            {"id": "user_reviewer", "organization_id": organization_id, "email": "reviewer@example.com", "name": "Reviewer", "role": "reviewer", "password_hash": hash_password("reviewer-password"), "status": "active", "department": "governance"},
        ]

    def _migrate_existing_state(self) -> None:
        organization_id = self.store.collection("organizations")[0]["id"]
        seeded_users = self._seed_users(organization_id)
        seeded_by_email = {user["email"]: user for user in seeded_users}
        seeded_by_id = {user["id"]: user for user in seeded_users}

        for name in [
            "workflow_runs",
            "approvals",
            "audit_logs",
            "stream_events",
            "memory_items",
            "evaluation_runs",
            "knowledge_documents",
            "governance_policies",
            "notifications",
            "process_metrics",
            "event_logs",
            "evolution_variants",
            "tool_effects",
            "pi_artifacts",
            "improvement_lessons",
            "loop_runs",
            "knowledge_nodes",
            "knowledge_edges",
            "skill_proposals",
            "user_invitations",
            "workflows",
            "agents",
            "tools",
        ]:
            self.store.state.setdefault(name, [])

        for name in ["access_tokens", "refresh_tokens", "api_keys"]:
            self.store.state.setdefault(name, {})

        self._normalize_workflows(organization_id)
        self._normalize_agents(organization_id)

        normalized_users: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for user in self.store.collection("users"):
            default_user = seeded_by_email.get(user.get("email")) or seeded_by_id.get(user.get("id", ""))
            normalized = dict(user)
            normalized.setdefault("organization_id", organization_id)
            normalized.setdefault("status", default_user["status"] if default_user else "active")
            normalized.setdefault("department", default_user["department"] if default_user else "general")
            if default_user and "password_hash" not in normalized:
                normalized["password_hash"] = default_user["password_hash"]
            normalized_users.append(normalized)
            seen_ids.add(normalized["id"])

        for seeded_user in seeded_users:
            if seeded_user["id"] not in seen_ids:
                normalized_users.append(dict(seeded_user))

        self.store.state["users"] = normalized_users

        user_ids = {user["id"] for user in normalized_users}
        access_tokens = {token: user_id for token, user_id in self.store.state["access_tokens"].items() if user_id in user_ids}
        refresh_tokens = {token: user_id for token, user_id in self.store.state["refresh_tokens"].items() if user_id in user_ids}
        default_access_tokens = {
            "owner-token": "user_owner",
            "admin-token": "user_admin",
            "operator-token": "user_operator",
            "reviewer-token": "user_reviewer",
        }
        default_refresh_tokens = {
            "owner-refresh-token": "user_owner",
            "admin-refresh-token": "user_admin",
            "operator-refresh-token": "user_operator",
            "reviewer-refresh-token": "user_reviewer",
        }
        for token, user_id in default_access_tokens.items():
            access_tokens.setdefault(token, user_id)
        for token, user_id in default_refresh_tokens.items():
            refresh_tokens.setdefault(token, user_id)
        self.store.state["access_tokens"] = access_tokens
        self.store.state["refresh_tokens"] = refresh_tokens
        self.store.state["api_keys"].setdefault("svc-default-key", {"user_id": "user_admin", "organization_id": organization_id})

    def _default_input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["case_id"],
            "properties": {
                "case_id": {"type": "string"},
                "customer_name": {"type": "string"},
                "triggered_from": {"type": "string"},
            },
        }

    def _default_output_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "required": ["outcome", "step_count"],
            "properties": {
                "outcome": {"type": "string"},
                "step_count": {"type": "number"},
            },
        }

    def _normalize_workflows(self, organization_id: str) -> None:
        """Ensure DNA-only or partial workflow records are runnable (status, schemas, org)."""
        seeded = {item["id"]: item for item in self.loader.load_workflows(organization_id)}
        normalized: list[dict[str, Any]] = []
        seen: set[str] = set()
        for raw in self.store.collection("workflows"):
            wf = dict(raw)
            seed = seeded.get(wf.get("id", ""))
            wf.setdefault("organization_id", organization_id)
            if not wf.get("organization_id"):
                wf["organization_id"] = organization_id
            # Prefer seed execution fields when missing/null
            if not wf.get("input_schema"):
                wf["input_schema"] = deepcopy((seed or {}).get("input_schema") or self._default_input_schema())
            if not wf.get("output_schema"):
                wf["output_schema"] = deepcopy((seed or {}).get("output_schema") or self._default_output_schema())
            if not wf.get("status"):
                if wf.get("production_ready") is True or (seed and seed.get("status") == "active"):
                    wf["status"] = "active"
                else:
                    wf["status"] = "draft"
            if not wf.get("active_version"):
                wf["active_version"] = wf.get("version") or (seed or {}).get("version") or "1.0.0"
            if not wf.get("version"):
                wf["version"] = wf["active_version"]
            if not wf.get("description") and wf.get("objective"):
                wf["description"] = wf["objective"]
            if not wf.get("versions"):
                steps = deepcopy(wf.get("steps") or (seed or {}).get("steps") or [])
                wf["versions"] = [{
                    "version": wf["active_version"],
                    "status": "active" if wf["status"] == "active" else "draft",
                    "created_at": utc_now(),
                    "immutable": True,
                    "steps": steps,
                }]
            if not wf.get("steps") and seed and seed.get("steps"):
                wf["steps"] = deepcopy(seed["steps"])
            if not wf.get("evaluation_policy"):
                wf["evaluation_policy"] = {"required": True, "block_on_fail": True}
            if not wf.get("governance_policy"):
                steps = wf.get("steps") or []
                wf["governance_policy"] = {
                    "risk_tier": wf.get("risk_tier", "tier_2_draft"),
                    "human_gate_steps": [step["id"] for step in steps if step.get("human_gate_required")],
                }
            if not wf.get("name"):
                wf["name"] = wf.get("id") or "unnamed_workflow"
            normalized.append(wf)
            seen.add(wf["id"])
        # Ensure flagship seed exists for live ops demos
        for seed_id, seed in seeded.items():
            if seed_id not in seen:
                normalized.append(deepcopy(seed))
        self.store.state["workflows"] = normalized

    def _normalize_agents(self, organization_id: str) -> None:
        seeded = {item["id"]: item for item in self.loader.load_agents(organization_id)}
        normalized: list[dict[str, Any]] = []
        seen: set[str] = set()
        for raw in self.store.collection("agents"):
            agent = dict(raw)
            seed = seeded.get(agent.get("id", ""))
            agent.setdefault("organization_id", organization_id)
            if not agent.get("organization_id"):
                agent["organization_id"] = organization_id
            agent.setdefault("status", "active")
            if not agent.get("allowed_tools") and seed:
                agent["allowed_tools"] = list(seed.get("allowed_tools") or [])
            if seed:
                # Union seed scopes so flagship agents pick up organization_memory upgrades
                current_scopes = list(agent.get("allowed_memory_scopes") or [])
                seed_scopes = list(seed.get("allowed_memory_scopes") or [])
                agent["allowed_memory_scopes"] = list(dict.fromkeys([*current_scopes, *seed_scopes]))
            elif not agent.get("allowed_memory_scopes"):
                agent["allowed_memory_scopes"] = ["workflow_memory", "organization_memory"]
            normalized.append(agent)
            seen.add(agent["id"])
        for seed_id, seed in seeded.items():
            if seed_id not in seen:
                normalized.append(deepcopy(seed))
        self.store.state["agents"] = normalized

    def _bootstrap(self) -> None:
        with self.store.lock:
            if self.store.collection("organizations"):
                self._migrate_existing_state()
                self.store.save()
                return

            organization_id = "org_default"
            users = self._seed_users(organization_id)

            self.store.state["organizations"] = [{"id": organization_id, "name": "Default Organization", "slug": "default", "status": "active", "created_at": utc_now(), "updated_at": utc_now()}]
            self.store.state["users"] = users
            self.store.state["access_tokens"] = {
                "owner-token": users[0]["id"],
                "admin-token": users[1]["id"],
                "operator-token": users[2]["id"],
                "reviewer-token": users[3]["id"],
            }
            self.store.state["refresh_tokens"] = {
                "owner-refresh-token": users[0]["id"],
                "admin-refresh-token": users[1]["id"],
                "operator-refresh-token": users[2]["id"],
                "reviewer-refresh-token": users[3]["id"],
            }
            self.store.state["api_keys"] = {"svc-default-key": {"user_id": users[1]["id"], "organization_id": organization_id}}
            self.store.state["agents"] = self.loader.load_agents(organization_id)
            self.store.state["tools"] = self.loader.load_tools(organization_id)
            self.store.state["workflows"] = self.loader.load_workflows(organization_id)
            self.store.state["knowledge_documents"] = self.loader.load_knowledge_documents(organization_id)
            self.store.state["process_metrics"] = [self._build_process_summary()]
            self.store.state["memory_items"] = [
                {
                    "id": "mem_seed_contract_rules",
                    "organization_id": organization_id,
                    "owner": "user_admin",
                    "department": "operations",
                    "scope": "organization_memory",
                    "title": "Contract Rules",
                    "content": "Enterprise contracts over configured thresholds require human review.",
                    "metadata": {"source": "seed"},
                    "embedding_reference": None,
                    "sensitivity_level": "internal",
                    "allowed_roles": ["owner", "admin", "manager", "operator", "reviewer"],
                    "expires_at": None,
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
            "approval_wait_minutes": 0,
            "failed_runs": 0,
            "last_updated_at": utc_now(),
        }

    def set_request_id(self, request_id: str | None) -> None:
        CURRENT_REQUEST_ID.set(request_id)

    def _current_request_id(self) -> str | None:
        return CURRENT_REQUEST_ID.get()

    def _scoped_items(self, name: str, organization_id: str) -> list[dict[str, Any]]:
        items = self.store.collection(name)
        return [item for item in items if item.get("organization_id") in {None, organization_id}]

    def _find_user(self, user_id: str) -> dict[str, Any]:
        user = next((item for item in self.store.collection("users") if item["id"] == user_id), None)
        if not user:
            raise NotFoundError(f"User not found: {user_id}")
        return user

    def _api_key_record(self, token: str, metadata: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": token,
            "token": token,
            "name": metadata.get("name", token),
            "organization_id": metadata.get("organization_id"),
            "user_id": metadata.get("user_id"),
            "status": metadata.get("status", "active"),
            "created_at": metadata.get("created_at"),
        }

    def authenticate(self, token: str | None) -> AuthenticatedUser:
        if not token:
            raise PermissionDeniedError("Invalid or missing bearer token")
        if token in self.store.state["access_tokens"]:
            user_id = self.store.state["access_tokens"][token]
        elif token in self.store.state["api_keys"]:
            user_id = self.store.state["api_keys"][token]["user_id"]
        else:
            raise PermissionDeniedError("Invalid or missing bearer token")
        user = self._find_user(user_id)
        if str(user.get("status", "active")).lower() in {"disabled", "invited"}:
            raise PermissionDeniedError(f"User account is {user.get('status')}")
        return AuthenticatedUser(id=user["id"], organization_id=user["organization_id"], email=user["email"], name=user["name"], role=user["role"])

    def assert_permission(self, user: AuthenticatedUser, permission: str) -> None:
        permissions = ROLE_PERMISSIONS.get(user.role, set())
        if "*" in permissions or permission in permissions:
            return
        raise PermissionDeniedError(f"Permission denied: {permission}")

    def list_collection(self, name: str) -> list[dict[str, Any]]:
        """Compatibility helper used by workers/repositories/seed scripts."""
        return deepcopy(self.store.collection(name))

    def _tier_level(self, risk_tier: str | None) -> int:
        if not risk_tier:
            return 2
        if isinstance(risk_tier, int):
            return risk_tier
        text = str(risk_tier)
        for level in range(0, 6):
            if text.startswith(f"tier_{level}") or text == str(level):
                return level
        legacy = {"observe": 0, "recommend": 1, "draft": 2, "low": 2, "medium": 3, "high": 4, "critical": 5, "restricted": 5}
        return legacy.get(text.lower(), 2)

    def _tool_requires_approval(self, tool: dict[str, Any]) -> bool:
        requirement = str(tool.get("approval_requirement") or tool.get("approval") or "").lower()
        if requirement in {"always", "required", "human", "gate", "true", "1"}:
            return True
        if tool.get("requires_approval") is True:
            return True
        if tool.get("approval_requirement") is True:
            return True
        return False

    def _agent_allowed_scopes(self, agent: dict[str, Any] | None) -> set[str]:
        if not agent:
            return set()
        scopes = agent.get("allowed_memory_scopes")
        if not scopes:
            # Back-compat: older agent records without scopes get org+workflow defaults
            return {"organization_memory", "workflow_memory"}
        return {str(s) for s in scopes}

    def assert_memory_scope_allowed(
        self,
        *,
        agent: dict[str, Any] | None,
        scope: str,
        action: str = "write",
        organization_id: str | None = None,
        actor_user_id: str | None = None,
    ) -> None:
        """Deny memory read/write when agent lacks the scope (structure.md hybrid memory control)."""
        allowed = self._agent_allowed_scopes(agent)
        # Admin/owner API writes without agent context use role-wide org memory by default
        if agent is None:
            return
        if scope not in allowed:
            if organization_id:
                self._append_audit(
                    organization_id,
                    actor_user_id,
                    "memory",
                    f"memory.{action}_denied",
                    "memory",
                    scope,
                    {"scope": scope, "agent_id": agent.get("id"), "allowed": sorted(allowed)},
                    "failed",
                )
                try:
                    self.store.save()
                except Exception:
                    pass
            raise PermissionDeniedError(
                f"Memory {action} denied for scope '{scope}' (agent {agent.get('id')} allowed={sorted(allowed)})"
            )

    def issue_token(self, email: str, password: str) -> dict[str, Any]:
        user = next((item for item in self.store.collection("users") if item["email"] == email), None)
        if not user or not verify_password(password, user.get("password_hash", "")):
            raise PermissionDeniedError("Invalid credentials")
        if str(user.get("status", "active")).lower() == "disabled":
            raise PermissionDeniedError("User account is disabled")
        if str(user.get("status", "active")).lower() == "invited":
            raise PermissionDeniedError("User invitation not accepted yet")
        # Upgrade legacy SHA-256 hashes on successful login
        if not str(user.get("password_hash", "")).startswith("pbkdf2$"):
            user["password_hash"] = hash_password(password)
            self.store.save()
        access_token = next((key for key, value in self.store.state["access_tokens"].items() if value == user["id"]), None)
        refresh_token = next((key for key, value in self.store.state["refresh_tokens"].items() if value == user["id"]), None)
        if not access_token:
            access_token = f"tok_{uuid.uuid4().hex[:18]}"
            self.store.state["access_tokens"][access_token] = user["id"]
        if not refresh_token:
            refresh_token = f"ref_{uuid.uuid4().hex[:18]}"
            self.store.state["refresh_tokens"][refresh_token] = user["id"]
        self._append_audit(user["organization_id"], user["id"], "auth", "user.login", "user", user["id"], {"email": email}, "success")
        self.store.save()
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user": self._sanitize_user(user)}

    def refresh_access_token(self, refresh_token: str) -> dict[str, Any]:
        user_id = self.store.state["refresh_tokens"].get(refresh_token)
        if not user_id:
            raise PermissionDeniedError("Invalid refresh token")
        user = self._find_user(user_id)
        access_token = next((key for key, value in self.store.state["access_tokens"].items() if value == user["id"]), None)
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def logout(self, token: str | None) -> dict[str, Any]:
        if token and token in self.store.state["access_tokens"]:
            user_id = self.store.state["access_tokens"].pop(token)
            user = self._find_user(user_id)
            self._append_audit(user["organization_id"], user["id"], "auth", "user.logout", "user", user["id"], {}, "success")
            self.store.save()
        return {"message": "logged_out"}

    def list_api_keys(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "settings:read")
        keys = []
        for token, metadata in self.store.state["api_keys"].items():
            if metadata.get("organization_id") != current_user.organization_id:
                continue
            keys.append(self._api_key_record(token, metadata))
        return deepcopy(keys)

    def create_api_key(self, current_user: AuthenticatedUser, name: str) -> dict[str, Any]:
        self.assert_permission(current_user, "settings:update")
        token = f"api_{uuid.uuid4().hex[:20]}"
        self.store.state["api_keys"][token] = {
            "user_id": current_user.id,
            "organization_id": current_user.organization_id,
            "name": name,
            "status": "active",
            "created_at": utc_now(),
        }
        self._append_audit(current_user.organization_id, current_user.id, "service_account", "api_key.created", "api_key", token, {"name": name}, "success")
        self.store.save()
        return deepcopy(self._api_key_record(token, self.store.state["api_keys"][token]))

    def revoke_api_key(self, current_user: AuthenticatedUser, key_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "settings:update")
        metadata = self.store.state["api_keys"].get(key_id)
        if not metadata or metadata.get("organization_id") != current_user.organization_id:
            raise NotFoundError(f"API key not found: {key_id}")
        metadata["status"] = "revoked"
        self.store.state["api_keys"].pop(key_id, None)
        self._append_audit(current_user.organization_id, current_user.id, "service_account", "api_key.revoked", "api_key", key_id, {}, "success")
        self.store.save()
        return {"id": key_id, "status": "revoked"}

    def reset_password(
        self,
        email: str,
        new_password: str,
        *,
        acting_user: AuthenticatedUser | None = None,
        reset_token: str | None = None,
    ) -> dict[str, Any]:
        """Reset password only for authenticated self-service or privileged admin.

        Unauthenticated open reset is intentionally rejected (structure.md / OWASP LLM02-adjacent).
        """
        user = next((item for item in self.store.collection("users") if item["email"] == email), None)
        if not user:
            # Avoid account enumeration for unauthenticated callers.
            if acting_user is None and not reset_token:
                raise PermissionDeniedError("Password reset requires authentication or a valid reset token")
            raise NotFoundError(f"User not found for email: {email}")

        if acting_user is not None:
            same_user = acting_user.id == user["id"]
            same_org = acting_user.organization_id == user["organization_id"]
            privileged = acting_user.role in {"owner", "admin"} or "*" in ROLE_PERMISSIONS.get(acting_user.role, set())
            if not same_user and not (privileged and same_org):
                raise PermissionDeniedError("Not allowed to reset this password")
        elif reset_token:
            expected = self.store.state.get("password_reset_tokens", {}).get(email)
            if not expected or expected != reset_token:
                raise PermissionDeniedError("Invalid or expired password reset token")
            self.store.state.setdefault("password_reset_tokens", {}).pop(email, None)
        else:
            raise PermissionDeniedError("Password reset requires authentication or a valid reset token")

        if len(new_password or "") < 8:
            raise ValidationError("Password must be at least 8 characters")
        user["password_hash"] = hash_password(new_password)
        self._append_audit(user["organization_id"], user["id"], "auth", "user.password_reset", "user", user["id"], {"email": email}, "success")
        self.store.save()
        return {"message": "password_reset", "email": email}

    def _sanitize_user(self, user: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in user.items() if key != "password_hash"}

    def list_users(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "users:read")
        return deepcopy([self._sanitize_user(item) for item in self._scoped_items("users", current_user.organization_id)])

    def get_user(self, current_user: AuthenticatedUser, user_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "users:read")
        user = next((item for item in self._scoped_items("users", current_user.organization_id) if item["id"] == user_id), None)
        if not user:
            raise NotFoundError(f"User not found: {user_id}")
        return deepcopy(self._sanitize_user(user))

    def create_user(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "users:create")
        if any(item["email"] == payload["email"] for item in self.store.collection("users")):
            raise ValidationError("Email already exists")
        role = payload.get("role", "viewer")
        if role not in ROLE_PERMISSIONS:
            raise ValidationError(f"Unknown role: {role}")
        status = payload.get("status", "active")
        if status not in {"active", "invited", "disabled"}:
            raise ValidationError("status must be active, invited, or disabled")
        created = {
            "id": f"user_{uuid.uuid4().hex[:10]}",
            "organization_id": current_user.organization_id,
            "email": payload["email"],
            "name": payload["name"],
            "role": role,
            "password_hash": hash_password(payload.get("password", "change-me")),
            "status": status,
            "department": payload.get("department", "general"),
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        self.store.collection("users").append(created)
        access_token = f"tok_{uuid.uuid4().hex[:18]}"
        refresh_token = f"ref_{uuid.uuid4().hex[:18]}"
        if status == "active":
            self.store.state["access_tokens"][access_token] = created["id"]
            self.store.state["refresh_tokens"][refresh_token] = created["id"]
        self._append_audit(current_user.organization_id, current_user.id, "user", "user.created", "user", created["id"], {"email": created["email"], "role": role, "status": status}, "success")
        self.store.save()
        out = self._sanitize_user(created)
        if status == "active":
            out = out | {"seed_access_token": access_token, "seed_refresh_token": refresh_token}
        return deepcopy(out)

    def update_user(self, current_user: AuthenticatedUser, user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "users:update")
        user = next((item for item in self._scoped_items("users", current_user.organization_id) if item["id"] == user_id), None)
        if not user:
            raise NotFoundError(f"User not found: {user_id}")
        if "name" in payload and payload["name"] is not None:
            user["name"] = payload["name"]
        if "department" in payload and payload["department"] is not None:
            user["department"] = payload["department"]
        if "role" in payload and payload["role"] is not None:
            if payload["role"] not in ROLE_PERMISSIONS:
                raise ValidationError(f"Unknown role: {payload['role']}")
            # Prevent non-owner from assigning owner
            if payload["role"] == "owner" and current_user.role not in {"owner"} and "*" not in ROLE_PERMISSIONS.get(current_user.role, set()):
                raise PermissionDeniedError("Only owner can assign owner role")
            user["role"] = payload["role"]
        if "status" in payload and payload["status"] is not None:
            if payload["status"] not in {"active", "invited", "disabled"}:
                raise ValidationError("status must be active, invited, or disabled")
            if user["id"] == current_user.id and payload["status"] == "disabled":
                raise ValidationError("Cannot disable your own account")
            user["status"] = payload["status"]
            if payload["status"] == "disabled":
                # Revoke live tokens for this user
                self.store.state["access_tokens"] = {
                    tok: uid for tok, uid in self.store.state.get("access_tokens", {}).items() if uid != user_id
                }
                self.store.state["refresh_tokens"] = {
                    tok: uid for tok, uid in self.store.state.get("refresh_tokens", {}).items() if uid != user_id
                }
        user["updated_at"] = utc_now()
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "user",
            "user.updated",
            "user",
            user_id,
            {k: payload.get(k) for k in ("name", "department", "role", "status") if k in payload},
            "success",
        )
        self.store.save()
        return deepcopy(self._sanitize_user(user))

    def create_invitation(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a pending invitation (BE-07). Accept via accept_invitation."""
        self.assert_permission(current_user, "users:invite")
        email = (payload.get("email") or "").strip().lower()
        if not email:
            raise ValidationError("email is required")
        if any(item["email"].lower() == email for item in self.store.collection("users")):
            raise ValidationError("Email already exists as a user")
        if any(
            item.get("email", "").lower() == email
            and item.get("status") == "pending"
            and item.get("organization_id") == current_user.organization_id
            for item in self.store.collection("user_invitations")
        ):
            raise ValidationError("Pending invitation already exists for this email")
        role = payload.get("role", "viewer")
        if role not in ROLE_PERMISSIONS:
            raise ValidationError(f"Unknown role: {role}")
        if role == "owner" and current_user.role not in {"owner"} and "*" not in ROLE_PERMISSIONS.get(current_user.role, set()):
            raise PermissionDeniedError("Only owner can invite as owner")
        token = f"inv_{uuid.uuid4().hex}"
        invitation = {
            "id": f"invitation_{uuid.uuid4().hex[:10]}",
            "organization_id": current_user.organization_id,
            "email": email,
            "name": payload.get("name") or email.split("@")[0],
            "role": role,
            "department": payload.get("department", "general"),
            "token": token,
            "status": "pending",
            "invited_by": current_user.id,
            "created_at": utc_now(),
            "accepted_at": None,
        }
        self.store.collection("user_invitations").append(invitation)
        # Placeholder invited user (cannot login until accept)
        if not any(u["email"].lower() == email for u in self.store.collection("users")):
            self.store.collection("users").append(
                {
                    "id": f"user_{uuid.uuid4().hex[:10]}",
                    "organization_id": current_user.organization_id,
                    "email": email,
                    "name": invitation["name"],
                    "role": role,
                    "password_hash": hash_password(uuid.uuid4().hex),
                    "status": "invited",
                    "department": invitation["department"],
                    "created_at": utc_now(),
                    "updated_at": utc_now(),
                }
            )
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "user",
            "user.invited",
            "invitation",
            invitation["id"],
            {"email": email, "role": role},
            "success",
        )
        self.store.save()
        # Return token once (ops/dev); production would email it
        return deepcopy({k: v for k, v in invitation.items()})

    def list_invitations(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "users:read")
        items = [
            item
            for item in self.store.collection("user_invitations")
            if item.get("organization_id") == current_user.organization_id
        ]
        return deepcopy(items)

    def accept_invitation(self, token: str, password: str, name: str | None = None) -> dict[str, Any]:
        """Public accept path: set password and activate invited user."""
        invitation = next(
            (item for item in self.store.collection("user_invitations") if item.get("token") == token and item.get("status") == "pending"),
            None,
        )
        if not invitation:
            raise NotFoundError("Invitation not found or already used")
        if len(password or "") < 8:
            raise ValidationError("Password must be at least 8 characters")
        user = next((item for item in self.store.collection("users") if item["email"].lower() == invitation["email"].lower()), None)
        if not user:
            raise NotFoundError("Invited user record missing")
        user["password_hash"] = hash_password(password)
        user["status"] = "active"
        if name:
            user["name"] = name
        user["updated_at"] = utc_now()
        invitation["status"] = "accepted"
        invitation["accepted_at"] = utc_now()
        access_token = f"tok_{uuid.uuid4().hex[:18]}"
        refresh_token = f"ref_{uuid.uuid4().hex[:18]}"
        self.store.state["access_tokens"][access_token] = user["id"]
        self.store.state["refresh_tokens"][refresh_token] = user["id"]
        self._append_audit(
            invitation["organization_id"],
            user["id"],
            "user",
            "user.invitation_accepted",
            "user",
            user["id"],
            {"email": user["email"]},
            "success",
        )
        self.store.save()
        return {
            "message": "invitation_accepted",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": self._sanitize_user(user),
        }

    def list_organizations(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "organizations:read")
        return deepcopy(self._scoped_items("organizations", current_user.organization_id))

    def get_organization(self, current_user: AuthenticatedUser, organization_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "organizations:read")
        org = next((item for item in self._scoped_items("organizations", current_user.organization_id) if item["id"] == organization_id), None)
        if not org:
            # allow read of own org only
            if organization_id != current_user.organization_id:
                raise NotFoundError(f"Organization not found: {organization_id}")
            org = next((item for item in self.store.collection("organizations") if item["id"] == organization_id), None)
        if not org:
            raise NotFoundError(f"Organization not found: {organization_id}")
        return deepcopy(org)

    def update_organization(self, current_user: AuthenticatedUser, organization_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "organizations:update")
        if organization_id != current_user.organization_id and current_user.role not in {"owner"} and "*" not in ROLE_PERMISSIONS.get(current_user.role, set()):
            raise PermissionDeniedError("Can only update your own organization")
        org = next((item for item in self.store.collection("organizations") if item["id"] == organization_id), None)
        if not org:
            raise NotFoundError(f"Organization not found: {organization_id}")
        if org["id"] != current_user.organization_id and current_user.role != "owner" and "*" not in ROLE_PERMISSIONS.get(current_user.role, set()):
            raise PermissionDeniedError("Not allowed to update this organization")
        if "name" in payload and payload["name"] is not None:
            org["name"] = payload["name"]
        if "slug" in payload and payload["slug"] is not None:
            org["slug"] = payload["slug"]
        if "status" in payload and payload["status"] is not None:
            if payload["status"] not in {"active", "disabled"}:
                raise ValidationError("status must be active or disabled")
            org["status"] = payload["status"]
        org["updated_at"] = utc_now()
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "organization",
            "organization.updated",
            "organization",
            organization_id,
            {k: payload.get(k) for k in ("name", "slug", "status") if k in payload},
            "success",
        )
        self.store.save()
        return deepcopy(org)

    def list_agents(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "agents:read")
        return deepcopy(self._scoped_items("agents", current_user.organization_id))

    def get_agent(self, current_user: AuthenticatedUser, agent_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "agents:read")
        agent = next((item for item in self._scoped_items("agents", current_user.organization_id) if item["id"] == agent_id), None)
        if not agent:
            raise NotFoundError(f"Agent not found: {agent_id}")
        return deepcopy(agent)

    def create_agent(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "agents:create")
        created = {
            "id": payload["id"],
            "organization_id": current_user.organization_id,
            "name": payload["name"],
            "description": payload.get("description"),
            "version": payload.get("version", "1.0.0"),
            "owner_user_id": current_user.id,
            "department": payload.get("department", "general"),
            "allowed_tools": payload.get("allowed_tools", []),
            "allowed_memory_scopes": payload.get("allowed_memory_scopes", []),
            "allowed_workflow_types": payload.get("allowed_workflow_types", ["general"]),
            "risk_level": payload.get("risk_level", "tier_2_draft"),
            "runtime_configuration": payload.get("runtime_configuration", {"mode": "local"}),
            "status": payload.get("status", "draft"),
            "role": payload.get("role", "execution"),
            "domain_id": payload.get("domain_id"),
            "requires_alc": payload.get("requires_alc"),
            "alc_version": payload.get("alc_version"),
            "hooks": payload.get("hooks") or {},
        }
        self.store.collection("agents").append(created)
        self._append_audit(current_user.organization_id, current_user.id, "agent", "agent.created", "agent", created["id"], {}, "success")
        self.store.save()
        return deepcopy(created)

    def update_agent_status(self, current_user: AuthenticatedUser, agent_id: str, status: str) -> dict[str, Any]:
        self.assert_permission(current_user, "agents:update")
        agent = next((item for item in self._scoped_items("agents", current_user.organization_id) if item["id"] == agent_id), None)
        if not agent:
            raise NotFoundError(f"Agent not found: {agent_id}")
        if status == "active":
            from app.infrastructure.governance.alc_validator import AlcRequiredError, assert_alc_ready

            try:
                assert_alc_ready(agent)
            except AlcRequiredError as exc:
                self._append_audit(
                    current_user.organization_id,
                    current_user.id,
                    "agent",
                    "agent.activate_denied_alc",
                    "agent",
                    agent_id,
                    {"code": exc.code},
                    "failed",
                )
                self.store.save()
                raise ValidationError(str(exc.message)) from exc
        agent["status"] = status
        self._append_audit(current_user.organization_id, current_user.id, "agent", "agent.updated", "agent", agent_id, {"status": status}, "success")
        self.store.save()
        return deepcopy(agent)

    def archive_agent(self, current_user: AuthenticatedUser, agent_id: str) -> dict[str, Any]:
        return self.update_agent_status(current_user, agent_id, "archived")

    def agent_activity(self, current_user: AuthenticatedUser, agent_id: str) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "agents:read")
        self.get_agent(current_user, agent_id)
        activity = []
        for run in self._scoped_items("workflow_runs", current_user.organization_id):
            for step in run.get("steps", []):
                if step.get("agent_id") == agent_id:
                    activity.append({
                        "workflow_run_id": run["id"],
                        "workflow_id": run["workflow_id"],
                        "step_id": step["id"],
                        "status": step["status"],
                        "completed_at": step.get("completed_at"),
                    })
        return deepcopy(activity)

    def agent_tools(self, current_user: AuthenticatedUser, agent_id: str) -> list[dict[str, Any]]:
        agent = self.get_agent(current_user, agent_id)
        allowed = set(agent.get("allowed_tools", []))
        return deepcopy([tool for tool in self._scoped_items("tools", current_user.organization_id) if tool["id"] in allowed])

    def list_tools(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "tools:read")
        return deepcopy(self._scoped_items("tools", current_user.organization_id))

    def get_tool(self, current_user: AuthenticatedUser, tool_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "tools:read")
        tool = next((item for item in self._scoped_items("tools", current_user.organization_id) if item["id"] == tool_id), None)
        if not tool:
            raise NotFoundError(f"Tool not found: {tool_id}")
        return deepcopy(tool)

    def create_tool(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "tools:create")
        created = {
            "id": payload["id"],
            "organization_id": current_user.organization_id,
            "name": payload["name"],
            "description": payload.get("description"),
            "category": payload.get("category", "internal_api"),
            "input_schema": payload.get("input_schema", {"type": "object"}),
            "output_schema": payload.get("output_schema", {"type": "object"}),
            "risk_level": payload.get("risk_level", "tier_2_draft"),
            "required_permissions": payload.get("required_permissions", ["workflows:execute"]),
            "approval_requirement": payload.get("approval_requirement", False),
            "timeout": payload.get("timeout", 30),
            "retry_policy": payload.get("retry_policy", {"max_retries": 1}),
            "enabled": payload.get("enabled", True),
            "allowed_actions": payload.get("allowed_actions", []),
            "scope": payload.get("scope", "custom"),
        }
        self.store.collection("tools").append(created)
        self._append_audit(current_user.organization_id, current_user.id, "tool", "tool.created", "tool", created["id"], {}, "success")
        self.store.save()
        return deepcopy(created)

    def update_tool_status(self, current_user: AuthenticatedUser, tool_id: str, enabled: bool) -> dict[str, Any]:
        self.assert_permission(current_user, "tools:update")
        tool = next((item for item in self._scoped_items("tools", current_user.organization_id) if item["id"] == tool_id), None)
        if not tool:
            raise NotFoundError(f"Tool not found: {tool_id}")
        tool["enabled"] = enabled
        self._append_audit(current_user.organization_id, current_user.id, "tool", "tool.updated", "tool", tool_id, {"enabled": enabled}, "success")
        self.store.save()
        return deepcopy(tool)

    def archive_tool(self, current_user: AuthenticatedUser, tool_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "tools:update")
        tool = next((item for item in self._scoped_items("tools", current_user.organization_id) if item["id"] == tool_id), None)
        if not tool:
            raise NotFoundError(f"Tool not found: {tool_id}")
        tool["enabled"] = False
        tool["archived"] = True
        self._append_audit(current_user.organization_id, current_user.id, "tool", "tool.archived", "tool", tool_id, {}, "success")
        self.store.save()
        return deepcopy(tool)

    def list_workflows(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "workflows:read")
        return deepcopy(self._scoped_items("workflows", current_user.organization_id))

    def get_workflow(self, current_user: AuthenticatedUser, workflow_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:read")
        workflow = next((item for item in self._scoped_items("workflows", current_user.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        return deepcopy(workflow)

    def list_workflow_versions(self, current_user: AuthenticatedUser, workflow_id: str) -> list[dict[str, Any]]:
        workflow = self.get_workflow(current_user, workflow_id)
        return deepcopy(workflow.get("versions", []))

    def _assert_production_dna_safe(
        self, dna_like: dict[str, Any], *, context: str = "workflow", force: bool = False
    ) -> None:
        """STRUCT-10: reject production DNA that violates gate/rollback rules.

        Enforced when production_ready=True or force=True (e.g. activate_workflow_version).
        Draft workflows may be incomplete until activation.
        """
        from app.infrastructure.governance.structure_validators import validate_production_workflow_dna

        if not force and not bool(dna_like.get("production_ready")):
            return
        failures = validate_production_workflow_dna(dna_like)
        if failures:
            raise ValidationError(f"{context} failed production DNA validation: " + "; ".join(failures))

    def create_workflow(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:create")
        steps = payload["steps"]
        created = {
            "id": payload["id"],
            "organization_id": current_user.organization_id,
            "name": payload["name"],
            "description": payload.get("description", payload["name"]),
            "version": payload.get("version", "1.0.0"),
            "owner": current_user.id,
            "department": payload.get("department", "general"),
            "risk_tier": payload.get("risk_tier", "tier_2_draft"),
            "input_schema": payload.get("input_schema", {"type": "object", "properties": {}, "required": []}),
            "output_schema": payload.get("output_schema", {"type": "object", "properties": {}, "required": []}),
            "steps": steps,
            "governance_policy": payload.get("governance_policy", {"risk_tier": payload.get("risk_tier", "tier_2_draft"), "human_gate_steps": [step["id"] for step in steps if step.get("human_gate_required")]}),
            "evaluation_policy": payload.get("evaluation_policy", {"required": True, "block_on_fail": True}),
            "status": payload.get("status", "draft"),
            "active_version": None,
            "versions": [{
                "version": payload.get("version", "1.0.0"),
                "status": payload.get("status", "draft"),
                "created_at": utc_now(),
                "immutable": False,
                "steps": deepcopy(steps),
            }],
            "memory_reads": payload.get("memory_reads", []),
            "memory_writes": payload.get("memory_writes", []),
            "guardrails": payload.get("guardrails", {"human_approval_required_if": [], "forbidden_actions": []}),
            "verification": payload.get("verification", {"required_checks": []}),
            "rollback": payload.get("rollback", {"reversible": True, "rollback_steps": []}),
            "fitness_metrics": payload.get("fitness_metrics", []),
            "audit_log_write_required": payload.get("audit_log_write_required", True),
            "provenance": payload.get("provenance", {"source_refs": ["api"], "captured_by": current_user.id, "recorded_at": utc_now()}),
            "production_ready": payload.get("production_ready", False),
        }
        self._assert_production_dna_safe(created, context="create_workflow")
        self.store.collection("workflows").append(created)
        self._append_audit(current_user.organization_id, current_user.id, "workflow", "workflow.created", "workflow", created["id"], {}, "success")
        self.store.save()
        return deepcopy(created)

    def update_workflow(self, current_user: AuthenticatedUser, workflow_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:update")
        workflow = next((item for item in self._scoped_items("workflows", current_user.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        for field in [
            "name",
            "description",
            "department",
            "risk_tier",
            "status",
            "memory_reads",
            "memory_writes",
            "guardrails",
            "verification",
            "rollback",
            "fitness_metrics",
            "production_ready",
        ]:
            if field in payload and payload[field] is not None:
                workflow[field] = payload[field]
        if "steps" in payload and payload["steps"]:
            workflow["steps"] = deepcopy(payload["steps"])
            if workflow.get("versions"):
                workflow["versions"][-1]["steps"] = deepcopy(payload["steps"])
        if "input_schema" in payload and payload["input_schema"] is not None:
            workflow["input_schema"] = payload["input_schema"]
        if "output_schema" in payload and payload["output_schema"] is not None:
            workflow["output_schema"] = payload["output_schema"]
        self._assert_production_dna_safe(workflow, context="update_workflow")
        self._append_audit(current_user.organization_id, current_user.id, "workflow", "workflow.updated", "workflow", workflow_id, {}, "success")
        self.store.save()
        return deepcopy(workflow)

    def add_workflow_version(self, current_user: AuthenticatedUser, workflow_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:update")
        workflow = next((item for item in self._scoped_items("workflows", current_user.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        if any(item["version"] == payload["version"] for item in workflow["versions"]):
            raise ValidationError("Workflow version already exists")
        version = {
            "version": payload["version"],
            "status": "draft",
            "created_at": utc_now(),
            "immutable": False,
            "steps": deepcopy(payload.get("steps", workflow["steps"])),
        }
        workflow["versions"].append(version)
        workflow["version"] = payload["version"]
        workflow["steps"] = deepcopy(version["steps"])
        self._append_audit(current_user.organization_id, current_user.id, "workflow", "workflow.version_created", "workflow", workflow_id, {"version": payload["version"]}, "success")
        self.store.save()
        return deepcopy(workflow)

    def activate_workflow_version(self, current_user: AuthenticatedUser, workflow_id: str, version: str) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:update")
        workflow = next((item for item in self._scoped_items("workflows", current_user.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        target = next((item for item in workflow["versions"] if item["version"] == version), None)
        if not target:
            raise NotFoundError(f"Workflow version not found: {version}")
        # Validate DNA as production before activation (STRUCT-10)
        candidate = deepcopy(workflow)
        candidate["steps"] = deepcopy(target["steps"])
        candidate["status"] = "active"
        candidate["production_ready"] = True
        self._assert_production_dna_safe(candidate, context="activate_workflow_version", force=True)
        for item in workflow["versions"]:
            item["status"] = "draft" if item["version"] != version else "active"
        target["immutable"] = True
        workflow["active_version"] = version
        workflow["version"] = version
        workflow["steps"] = deepcopy(target["steps"])
        workflow["status"] = "active"
        workflow["production_ready"] = True
        self._append_audit(current_user.organization_id, current_user.id, "workflow", "workflow.activated", "workflow", workflow_id, {"version": version}, "success")
        self.store.save()
        return deepcopy(workflow)

    def disable_workflow(self, current_user: AuthenticatedUser, workflow_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:update")
        workflow = next((item for item in self._scoped_items("workflows", current_user.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        workflow["status"] = "disabled"
        self._append_audit(current_user.organization_id, current_user.id, "workflow", "workflow.disabled", "workflow", workflow_id, {}, "success")
        self.store.save()
        return deepcopy(workflow)

    def archive_workflow(self, current_user: AuthenticatedUser, workflow_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:update")
        workflow = next((item for item in self._scoped_items("workflows", current_user.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        workflow["status"] = "archived"
        self._append_audit(current_user.organization_id, current_user.id, "workflow", "workflow.archived", "workflow", workflow_id, {}, "success")
        self.store.save()
        return deepcopy(workflow)

    def _validate_schema(self, schema: dict[str, Any] | None, payload: dict[str, Any], label: str) -> None:
        if not schema or not isinstance(schema, dict):
            return
        if schema.get("type") != "object":
            return
        body = payload or {}
        for required in schema.get("required", []) or []:
            if required not in body or body[required] in (None, ""):
                raise ValidationError(f"{label} missing required field: {required}")

    def governance_preview(self, workflow: dict[str, Any], requested_by: AuthenticatedUser) -> dict[str, Any]:
        gated_steps = [step["id"] for step in workflow["steps"] if step.get("human_gate_required")]
        return {
            "workflow_id": workflow["id"],
            "risk_tier": workflow["risk_tier"],
            "requested_by": requested_by.id,
            "human_gate_steps": gated_steps,
            "approval_required": len(gated_steps) > 0,
            "policy_summary": workflow.get("guardrails", {}).get("human_approval_required_if", []),
        }

    def list_runs(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "workflow_runs:read")
        return deepcopy(self._scoped_items("workflow_runs", current_user.organization_id))

    def get_run(self, current_user: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "workflow_runs:read")
        run = next((item for item in self._scoped_items("workflow_runs", current_user.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        return deepcopy(run)

    def start_workflow_run(self, workflow_id: str, requested_by: AuthenticatedUser, payload: dict[str, Any], idempotency_key: str | None = None) -> dict[str, Any]:
        self.assert_permission(requested_by, "workflows:execute")
        # Self-heal DNA-only records that predate normalization
        self._normalize_workflows(requested_by.organization_id)
        workflow = next((item for item in self._scoped_items("workflows", requested_by.organization_id) if item["id"] == workflow_id), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        status = workflow.get("status")
        if status != "active":
            raise ValidationError(f"Only active workflows can be run (status={status!r})")
        tier = self._tier_level(workflow.get("risk_tier"))
        if tier >= 5:
            raise PermissionDeniedError(
                "Tier 5 restricted workflows cannot start until an assurance case is recorded and approved"
            )
        if tier <= 0:
            raise ValidationError("Tier 0 observe workflows cannot execute actions; use recommend/draft tiers")
        input_schema = workflow.get("input_schema") or self._default_input_schema()
        if not isinstance(input_schema, dict):
            raise ValidationError("workflow input_schema must be an object schema")
        self._validate_schema(input_schema, payload or {}, "workflow input")
        steps = workflow.get("steps") or []
        if not steps:
            raise ValidationError("Workflow has no steps to execute")
        if idempotency_key:
            existing = next(
                (
                    item for item in self._scoped_items("workflow_runs", requested_by.organization_id)
                    if item["workflow_id"] == workflow_id
                    and item["requested_by"] == requested_by.id
                    and item.get("idempotency_key") == idempotency_key
                ),
                None,
            )
            if existing:
                return deepcopy(existing)
        version = workflow.get("active_version") or workflow.get("version") or "1.0.0"
        run = {
            "id": f"run_{uuid.uuid4().hex[:12]}",
            "organization_id": requested_by.organization_id,
            "workflow_id": workflow_id,
            "workflow_name": workflow.get("name") or workflow_id,
            "workflow_version": version,
            "status": "queued",
            "risk_tier": workflow.get("risk_tier") or "tier_2_draft",
            "requested_by": requested_by.id,
            "input_payload": payload,
            "output": None,
            "error": None,
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "queued_at": utc_now(),
            "started_at": None,
            "completed_at": None,
            "current_step": None,
            "approval_request_id": None,
            "approval_state": None,
            "evaluation_results": [],
            "token_usage": 0,
            "cost_usage": 0,
            "retry_count": 0,
            "idempotency_key": idempotency_key,
            "steps": [
                {
                    "id": step.get("id") or f"step_{idx}",
                    "workflow_run_id": None,
                    "step_name": step.get("id") or f"step_{idx}",
                    "step_type": step.get("action_type") or "analysis",
                    "agent_id": step.get("agent"),
                    "tool_id": (step.get("tools") or [None])[0],
                    "input": payload,
                    "output": None,
                    "error": None,
                    "status": "pending",
                    "started_at": None,
                    "completed_at": None,
                    "duration": None,
                    "retry_count": 0,
                }
                for idx, step in enumerate(steps)
            ],
            "result": None,
        }
        for step in run["steps"]:
            step["workflow_run_id"] = run["id"]
        self.store.collection("workflow_runs").append(run)
        self._append_audit(requested_by.organization_id, requested_by.id, "workflow_run", "workflow_run.started", "workflow_run", run["id"], {"workflow_id": workflow_id, "status": "queued"}, "success")
        self._emit_event("run.started", run["id"], None, "Workflow run queued")
        self.store.save()
        return deepcopy(run)

    def get_run_steps(self, current_user: AuthenticatedUser, run_id: str) -> list[dict[str, Any]]:
        run = self.get_run(current_user, run_id)
        return deepcopy(run.get("steps", []))

    def dispatch_queued_runs(self, requested_by: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(requested_by, "workflow_runs:dispatch")
        queued = [item for item in self._scoped_items("workflow_runs", requested_by.organization_id) if item["status"] in {"queued", "retry_queued"}]
        results = []
        for run in queued:
            run["status"] = "running"
            run["started_at"] = run["started_at"] or utc_now()
            run["updated_at"] = utc_now()
            self._emit_event("run.status_changed", run["id"], None, "Run picked up by worker")
            self._execute_run(run, requested_by.id)
            results.append(deepcopy(run))
        self.store.save()
        return results

    def cancel_run(self, requested_by: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        self.assert_permission(requested_by, "workflow_runs:cancel")
        run = next((item for item in self._scoped_items("workflow_runs", requested_by.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        if run["status"] in {"completed", "cancelled", "expired"}:
            raise ValidationError(f"Cannot cancel run in status {run['status']!r}")
        run["status"] = "cancelled"
        run["updated_at"] = utc_now()
        run["completed_at"] = utc_now()
        run["error"] = None
        self._append_audit(requested_by.organization_id, requested_by.id, "workflow_run", "workflow_run.cancelled", "workflow_run", run_id, {}, "success")
        self._emit_event("run.status_changed", run_id, None, "Run cancelled")
        self.store.save()
        return deepcopy(run)

    def pause_run(self, requested_by: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        """Pause a running/queued run (BE-11 lifecycle)."""
        self.assert_permission(requested_by, "workflow_runs:cancel")
        run = next((item for item in self._scoped_items("workflow_runs", requested_by.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        if run["status"] not in {"queued", "running", "retry_queued"}:
            raise ValidationError(f"Cannot pause run in status {run['status']!r}")
        run["status"] = "paused"
        run["updated_at"] = utc_now()
        self._append_audit(requested_by.organization_id, requested_by.id, "workflow_run", "workflow_run.paused", "workflow_run", run_id, {}, "success")
        self._emit_event("run.status_changed", run_id, None, "Run paused")
        self.store.save()
        return deepcopy(run)

    def resume_run(self, requested_by: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        """Resume a paused run back to queued for dispatch."""
        self.assert_permission(requested_by, "workflow_runs:retry")
        run = next((item for item in self._scoped_items("workflow_runs", requested_by.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        if run["status"] != "paused":
            raise ValidationError("Only paused runs can be resumed")
        run["status"] = "queued"
        run["updated_at"] = utc_now()
        self._append_audit(requested_by.organization_id, requested_by.id, "workflow_run", "workflow_run.resumed", "workflow_run", run_id, {}, "success")
        self._emit_event("run.status_changed", run_id, None, "Run resumed to queued")
        self.store.save()
        return deepcopy(run)

    def expire_run(self, requested_by: AuthenticatedUser, run_id: str, reason: str | None = None) -> dict[str, Any]:
        """Mark a non-terminal run as expired (BE-11 lifecycle)."""
        self.assert_permission(requested_by, "workflow_runs:cancel")
        run = next((item for item in self._scoped_items("workflow_runs", requested_by.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        if run["status"] in {"completed", "cancelled", "expired"}:
            raise ValidationError(f"Cannot expire run in status {run['status']!r}")
        run["status"] = "expired"
        run["updated_at"] = utc_now()
        run["completed_at"] = utc_now()
        run["error"] = reason or "expired"
        self._append_audit(
            requested_by.organization_id,
            requested_by.id,
            "workflow_run",
            "workflow_run.expired",
            "workflow_run",
            run_id,
            {"reason": reason or "expired"},
            "success",
        )
        self._emit_event("run.status_changed", run_id, None, "Run expired")
        self.store.save()
        return deepcopy(run)

    def retry_run(self, requested_by: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        self.assert_permission(requested_by, "workflow_runs:retry")
        run = next((item for item in self._scoped_items("workflow_runs", requested_by.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        if run["status"] not in {"failed", "cancelled", "rejected", "expired", "paused"}:
            raise ValidationError("Only failed, cancelled, rejected, expired, or paused runs can be retried")
        run["status"] = "retry_queued"
        run["retry_count"] += 1
        run["updated_at"] = utc_now()
        run["current_step"] = None
        run["approval_request_id"] = None
        run["approval_state"] = None
        run["error"] = None
        run["output"] = None
        run["result"] = None
        for step in run["steps"]:
            step["status"] = "pending"
            step["output"] = None
            step["error"] = None
            step["started_at"] = None
            step["completed_at"] = None
            step["duration"] = None
        self._append_audit(requested_by.organization_id, requested_by.id, "workflow_run", "workflow_run.retry_queued", "workflow_run", run_id, {"retry_count": run["retry_count"]}, "success")
        self._emit_event("run.status_changed", run_id, None, "Run queued for retry")
        self.store.save()
        return deepcopy(run)

    def _append_audit(self, organization_id: str, actor_user_id: str | None, actor_type: str, action: str, resource_type: str, resource_id: str, metadata: dict[str, Any], status: str) -> None:
        entry = {
            "id": f"audit_{uuid.uuid4().hex[:12]}",
            "organization_id": organization_id,
            "actor_user_id": actor_user_id,
            "actor_type": actor_type,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "request_id": self._current_request_id(),
            "metadata": metadata,
            "status": status,
            "created_at": utc_now(),
        }
        self.store.collection("audit_logs").append(entry)

    def _emit_event(self, event: str, run_id: str, step_id: str | None, message: str) -> None:
        self.store.collection("stream_events").append({
            "id": f"evt_{uuid.uuid4().hex[:12]}",
            "event": event,
            "workflow_run_id": run_id,
            "step_id": step_id,
            "message": message,
            "timestamp": utc_now(),
        })

    def _tool_lookup(self, organization_id: str) -> dict[str, dict[str, Any]]:
        return {item["id"]: item for item in self._scoped_items("tools", organization_id)}

    def _agent_lookup(self, organization_id: str) -> dict[str, dict[str, Any]]:
        return {item["id"]: item for item in self._scoped_items("agents", organization_id)}

    def _write_memory(
        self,
        organization_id: str,
        owner: str,
        scope: str,
        title: str,
        content: str,
        provenance: dict[str, Any],
        sensitivity_level: str = "internal",
        *,
        agent: dict[str, Any] | None = None,
    ) -> None:
        if agent is not None:
            self.assert_memory_scope_allowed(
                agent=agent,
                scope=scope,
                action="write",
                organization_id=organization_id,
                actor_user_id=owner,
            )
        self.store.collection("memory_items").append({
            "id": f"mem_{uuid.uuid4().hex[:12]}",
            "organization_id": organization_id,
            "owner": owner,
            "department": "operations",
            "scope": scope,
            "title": title,
            "content": content,
            "metadata": {"created_by_runtime": True},
            "embedding_reference": None,
            "sensitivity_level": sensitivity_level,
            "allowed_roles": ["owner", "admin", "manager", "operator", "reviewer"],
            "expires_at": None,
            "provenance": provenance,
            "created_at": utc_now(),
        })

    def _execute_run(self, run: dict[str, Any], actor_user_id: str) -> None:
        try:
            self._execute_run_body(run, actor_user_id)
        finally:
            # Auto-reflect on terminal states (self-evolving inter-episode loop)
            try:
                if run.get("status") in {"completed", "failed", "waiting_for_approval"}:
                    self._auto_reflect_if_enabled(run, actor_user_id)
            except Exception:  # noqa: BLE001
                pass

    def _execute_run_body(self, run: dict[str, Any], actor_user_id: str) -> None:
        workflow = next((item for item in self._scoped_items("workflows", run["organization_id"]) if item["id"] == run["workflow_id"]), None)
        if not workflow:
            raise NotFoundError(f"Workflow not found: {run['workflow_id']}")
        tool_lookup = self._tool_lookup(run["organization_id"])
        agent_lookup = self._agent_lookup(run["organization_id"])
        for step_record, step_definition in zip(run["steps"], workflow["steps"]):
            if step_record["status"] == "completed":
                continue
            run["current_step"] = step_definition["id"]
            step_record["status"] = "running"
            step_record["started_at"] = utc_now()
            self._emit_event("step.started", run["id"], step_definition["id"], f"Starting step {step_definition['id']}")
            agent = agent_lookup.get(step_definition["agent"])
            step_record["agent_id"] = (agent or {}).get("id") or step_definition.get("agent")
            agent_status = (agent or {}).get("status", "active")
            if not agent or agent_status not in {"active", "enabled"}:
                step_record["status"] = "failed"
                step_record["error"] = f"Agent unavailable: {step_definition['agent']}"
                run["status"] = "failed"
                run["error"] = step_record["error"]
                self._emit_event("step.failed", run["id"], step_definition["id"], step_record["error"])
                self._append_audit(run["organization_id"], actor_user_id, "workflow_step", "workflow_step.failed", "workflow_run", run["id"], {"step_id": step_definition["id"], "reason": step_record["error"]}, "failed")
                return
            # Ensure scope/tool metadata exists for older store records
            agent.setdefault("allowed_memory_scopes", ["workflow_memory", "organization_memory"])
            if not agent.get("allowed_tools"):
                seeded = next((a for a in self.loader.load_agents(run["organization_id"]) if a["id"] == agent.get("id")), None)
                if seeded and seeded.get("allowed_tools"):
                    agent["allowed_tools"] = list(seeded["allowed_tools"])
                else:
                    agent["allowed_tools"] = list(step_definition.get("tools") or [])

            tool_gate_required = False
            for tool_id in step_definition["tools"]:
                tool = tool_lookup.get(tool_id)
                if not tool or tool.get("enabled", True) is False:
                    step_record["status"] = "failed"
                    step_record["error"] = f"Tool unavailable: {tool_id}"
                    run["status"] = "failed"
                    run["error"] = step_record["error"]
                    self._emit_event("step.failed", run["id"], step_definition["id"], step_record["error"])
                    self._append_audit(run["organization_id"], actor_user_id, "workflow_step", "workflow_step.failed", "workflow_run", run["id"], {"step_id": step_definition["id"], "reason": step_record["error"]}, "failed")
                    return
                if tool_id not in agent["allowed_tools"]:
                    step_record["status"] = "failed"
                    step_record["error"] = f"Agent {agent['id']} is not allowed to use tool {tool_id}"
                    run["status"] = "failed"
                    run["error"] = step_record["error"]
                    self._emit_event("step.failed", run["id"], step_definition["id"], step_record["error"])
                    self._append_audit(run["organization_id"], actor_user_id, "workflow_step", "workflow_step.failed", "workflow_run", run["id"], {"step_id": step_definition["id"], "reason": step_record["error"]}, "failed")
                    return
                if self._tool_requires_approval(tool):
                    tool_gate_required = True

            tier = self._tier_level(run.get("risk_tier") or workflow.get("risk_tier"))
            # structure.md §6.1: tier 4 gates critical steps; tier 2 drafts need approval before externalize
            critical_action = (
                step_definition.get("irreversible")
                or step_definition.get("action_type") in {"irreversible_execution", "external_write"}
            )
            tier_requires_gate = (tier >= 4 and critical_action) or (
                tier == 2
                and step_definition.get("action_type")
                in {"notification", "irreversible_execution", "external_write", "send"}
            )
            sensitive_action = (
                step_definition.get("human_gate_required")
                or step_definition.get("irreversible")
                or step_definition.get("action_type") == "irreversible_execution"
                or tool_gate_required
                or tier_requires_gate
            )
            if sensitive_action and not self._is_step_approved(run["id"], step_definition["id"]):
                approval = self._create_approval(run, step_definition, actor_user_id)
                step_record["status"] = "waiting_for_approval"
                run["status"] = "waiting_for_approval"
                run["approval_request_id"] = approval["id"]
                run["approval_state"] = "pending"
                run["updated_at"] = utc_now()
                self.store.save()
                self._emit_event("approval.requested", run["id"], step_definition["id"], f"Approval requested for {step_definition['id']}")
                return

            # Memory reads declared on workflow (structure.md hybrid memory)
            scope_aliases = {
                "event_log": "workflow_memory",
                "decision_memory": "organization_memory",
                "lessons_learned": "organization_memory",
                "contract_rules": "organization_memory",
                "customer_exceptions": "organization_memory",
                "past_failures": "organization_memory",
            }
            memory_context: list[dict[str, Any]] = []
            for raw_scope in workflow.get("memory_reads") or []:
                read_scope = scope_aliases.get(raw_scope, raw_scope)
                try:
                    self.assert_memory_scope_allowed(
                        agent=agent,
                        scope=read_scope,
                        action="read",
                        organization_id=run["organization_id"],
                        actor_user_id=actor_user_id,
                    )
                except PermissionDeniedError as exc:
                    step_record["status"] = "failed"
                    step_record["error"] = str(exc.message if hasattr(exc, "message") else exc)
                    run["status"] = "failed"
                    run["error"] = step_record["error"]
                    self._emit_event("step.failed", run["id"], step_definition["id"], step_record["error"])
                    self.store.save()
                    return
                hits = [
                    item
                    for item in self._scoped_items("memory_items", run["organization_id"])
                    if item.get("scope") == read_scope
                ][:5]
                memory_context.extend(hits)

            # ALC pre-step: inject top-k agent lessons (Wave 1)
            try:
                from app.infrastructure.self_improvement.lessons import LessonLibrary

                org_lessons = [
                    i
                    for i in self.store.collection("improvement_lessons")
                    if i.get("organization_id") == run["organization_id"]
                ]
                lib = LessonLibrary(org_lessons)
                injected = lib.retrieve(
                    agent_id=agent.get("id"),
                    workflow_id=run.get("workflow_id"),
                    k=5,
                    increment_uses=True,
                )
                step_record["injected_lessons"] = [l.to_dict() for l in injected]
                # Persist use counters back into store
                by_id = {i.get("id"): i for i in self.store.collection("improvement_lessons")}
                for lesson in injected:
                    if lesson.id in by_id:
                        by_id[lesson.id]["uses"] = lesson.uses
            except Exception:  # noqa: BLE001
                step_record.setdefault("injected_lessons", [])

            # Execute tools via registered adapters (real side-effect records)
            from app.infrastructure.tools.adapters import ToolAdapterError, execute_tool

            tool_results: list[dict[str, Any]] = []
            base_payload = {
                **(run.get("input_payload") or {}),
                "run_id": run["id"],
                "step_id": step_definition["id"],
                "workflow_id": run["workflow_id"],
                "agent_id": agent.get("id"),
                "message": f"step:{step_definition['id']}",
            }
            for tool_id in step_definition.get("tools") or []:
                try:
                    effect = execute_tool(tool_id, base_payload)
                except ToolAdapterError as exc:
                    step_record["status"] = "failed"
                    step_record["error"] = exc.message
                    run["status"] = "failed"
                    run["error"] = step_record["error"]
                    self._emit_event("step.failed", run["id"], step_definition["id"], step_record["error"])
                    self._append_audit(
                        run["organization_id"],
                        actor_user_id,
                        "workflow_step",
                        "workflow_step.tool_failed",
                        "workflow_run",
                        run["id"],
                        {"step_id": step_definition["id"], "tool_id": tool_id, "reason": exc.message},
                        "failed",
                    )
                    self.store.save()
                    return
                effect["organization_id"] = run["organization_id"]
                effect["run_id"] = run["id"]
                effect["step_id"] = step_definition["id"]
                self.store.collection("tool_effects").append(effect)
                tool_results.append(effect)
                self._append_audit(
                    run["organization_id"],
                    actor_user_id,
                    "tool",
                    "tool.executed",
                    "tool_effect",
                    effect["id"],
                    {"tool_id": tool_id, "run_id": run["id"], "step_id": step_definition["id"]},
                    "success",
                )

            step_record["output"] = {
                "agent": step_definition["agent"],
                "tools_used": step_definition.get("tools") or [],
                "tool_effects": [item["id"] for item in tool_results],
                "memory_reads": len(memory_context),
                "message": f"Completed step {step_definition['id']}",
                "results": [item.get("result") for item in tool_results],
            }
            step_record["completed_at"] = utc_now()
            start = parse_dt(step_record["started_at"])
            end = parse_dt(step_record["completed_at"])
            step_record["duration"] = (end - start).total_seconds() if start and end else 0
            step_record["status"] = "completed"
            run["updated_at"] = utc_now()
            self._append_audit(run["organization_id"], actor_user_id, "workflow_step", "workflow_step.completed", "workflow_run", run["id"], {"step_id": step_definition["id"], "agent": step_definition["agent"], "tool_effects": [item["id"] for item in tool_results]}, "success")
            memory_scopes = workflow.get("memory_writes") or ["workflow_memory"]
            write_scope = memory_scopes[0] if memory_scopes else "workflow_memory"
            write_scope = scope_aliases.get(write_scope, write_scope)
            try:
                self._write_memory(
                    run["organization_id"],
                    actor_user_id,
                    write_scope,
                    f"Run {run['id']} step {step_definition['id']}",
                    f"Completed step {step_definition['id']} using {', '.join(step_definition.get('tools') or [])}. effects={[e['id'] for e in tool_results]}",
                    workflow.get("provenance") or {"source_refs": [run["workflow_id"]], "captured_by": actor_user_id, "recorded_at": utc_now()},
                    agent=agent,
                )
            except PermissionDeniedError as exc:
                step_record["status"] = "failed"
                step_record["error"] = str(exc.message if hasattr(exc, "message") else exc)
                run["status"] = "failed"
                run["error"] = step_record["error"]
                self._emit_event("step.failed", run["id"], step_definition["id"], step_record["error"])
                self.store.save()
                return
            self._emit_event("step.completed", run["id"], step_definition["id"], f"Completed step {step_definition['id']}")
            self.store.save()

        run["status"] = "completed"
        run["current_step"] = None
        run["approval_request_id"] = None
        run["approval_state"] = None
        run["completed_at"] = utc_now()
        run["output"] = {"outcome": "completed", "step_count": len(run["steps"])}
        self._validate_schema(workflow["output_schema"], run["output"], "workflow output")
        evaluation = self._create_evaluation(run)
        run["evaluation_results"].append(evaluation["id"])
        run["result"] = run["output"]
        eval_policy = workflow.get("evaluation_policy") or {}
        if eval_policy.get("block_on_fail") and evaluation.get("status") in {"failed", "fail", "blocked"}:
            run["status"] = "failed"
            run["error"] = "Evaluation failed and evaluation_policy.block_on_fail is enabled"
            self._append_audit(
                run["organization_id"],
                actor_user_id,
                "workflow_run",
                "workflow_run.evaluation_blocked",
                "workflow_run",
                run["id"],
                {"evaluation_id": evaluation["id"]},
                "failed",
            )
            self._emit_event("evaluation.failed", run["id"], None, "Evaluation blocked promotion/completion")
            return
        self._append_audit(run["organization_id"], actor_user_id, "workflow_run", "workflow_run.completed", "workflow_run", run["id"], {"evaluation_id": evaluation["id"]}, "success")
        self._emit_event("evaluation.completed", run["id"], None, "Evaluation completed")
        self._emit_event("run.completed", run["id"], None, "Workflow run completed")

    def _create_approval(self, run: dict[str, Any], step: dict[str, Any], actor_user_id: str) -> dict[str, Any]:
        existing = next((item for item in self.store.collection("approvals") if item["run_id"] == run["id"] and item["step_id"] == step["id"] and item["status"] == "pending"), None)
        if existing:
            return existing
        approval = {
            "id": f"apr_{uuid.uuid4().hex[:12]}",
            "organization_id": run["organization_id"],
            "run_id": run["id"],
            "workflow_id": run["workflow_id"],
            "step_id": step["id"],
            "requested_action": step["action_type"],
            "risk_level": run["risk_tier"],
            "requested_by": actor_user_id,
            "assigned_reviewer": None,
            "status": "pending",
            "decision": None,
            "decision_reason": None,
            "created_at": utc_now(),
            "decided_at": None,
        }
        self.store.collection("approvals").append(approval)
        self._append_audit(run["organization_id"], actor_user_id, "approval", "approval.requested", "approval", approval["id"], {"run_id": run["id"], "step_id": step["id"]}, "success")
        return approval

    def _is_step_approved(self, run_id: str, step_id: str) -> bool:
        return any(item["run_id"] == run_id and item["step_id"] == step_id and item["status"] == "approved" for item in self.store.collection("approvals"))

    def list_approvals(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "approvals:read")
        return deepcopy(self._scoped_items("approvals", current_user.organization_id))

    def get_approval(self, current_user: AuthenticatedUser, approval_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "approvals:read")
        approval = next((item for item in self._scoped_items("approvals", current_user.organization_id) if item["id"] == approval_id), None)
        if not approval:
            raise NotFoundError(f"Approval not found: {approval_id}")
        return deepcopy(approval)

    def decide_approval(self, approval_id: str, decision: str, reason: str | None, decided_by: AuthenticatedUser) -> dict[str, Any]:
        required_permission = "approvals:approve" if decision == "approved" else "approvals:reject"
        self.assert_permission(decided_by, required_permission)
        approval = next((item for item in self._scoped_items("approvals", decided_by.organization_id) if item["id"] == approval_id), None)
        if not approval:
            raise NotFoundError(f"Approval not found: {approval_id}")
        if approval["status"] != "pending":
            return deepcopy(approval)
        if decision not in {"approved", "rejected"}:
            raise ValidationError("Decision must be approved or rejected")
        approval["status"] = decision
        approval["decision"] = decision
        approval["decision_reason"] = reason
        approval["assigned_reviewer"] = decided_by.id
        approval["decided_at"] = utc_now()
        run = next((item for item in self._scoped_items("workflow_runs", decided_by.organization_id) if item["id"] == approval["run_id"]), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {approval['run_id']}")
        if decision == "approved":
            run["status"] = "running"
            run["approval_state"] = "approved"
            self._append_audit(decided_by.organization_id, decided_by.id, "approval", "approval.approved", "approval", approval_id, {"run_id": run["id"]}, "success")
            self._emit_event("approval.approved", run["id"], approval["step_id"], "Approval granted")
            self._execute_run(run, decided_by.id)
        else:
            run["status"] = "rejected"
            run["approval_state"] = "rejected"
            run["completed_at"] = utc_now()
            run["error"] = reason or "Approval rejected"
            self._append_audit(decided_by.organization_id, decided_by.id, "approval", "approval.rejected", "approval", approval_id, {"run_id": run["id"]}, "success")
            self._emit_event("approval.rejected", run["id"], approval["step_id"], "Approval rejected")
            # STRUCT-16: store rejection as learning signal (lessons), not production DNA mutation
            self._record_rejection_lesson(run, approval, decided_by, reason)
        self.store.save()
        return deepcopy(approval)

    def _record_rejection_lesson(
        self,
        run: dict[str, Any],
        approval: dict[str, Any],
        decided_by: AuthenticatedUser,
        reason: str | None,
    ) -> None:
        lessons = self.store.data.setdefault("improvement_lessons", [])
        lesson = {
            "id": f"lesson_reject_{approval.get('id', 'unknown')}",
            "type": "decision",
            "organization_id": decided_by.organization_id,
            "workflow_id": run.get("workflow_id"),
            "run_id": run.get("id"),
            "source": "approval.rejected",
            "step_id": approval.get("step_id"),
            "summary": reason or "Human rejected gated step",
            "utility": 0.6,
            "provenance": {
                "source_refs": [f"approval:{approval.get('id')}", f"run:{run.get('id')}"],
                "captured_by": decided_by.id,
                "recorded_at": utc_now(),
            },
            "scopes": ["organization_memory", "improvement_lessons"],
            "created_at": utc_now(),
        }
        lessons.append(lesson)
        try:
            self._append_audit(
                decided_by.organization_id,
                decided_by.id,
                "improvement",
                "lesson.rejection_recorded",
                "lesson",
                lesson["id"],
                {"run_id": run.get("id"), "approval_id": approval.get("id")},
                "success",
            )
        except Exception:
            pass

    def reassign_approval(self, approval_id: str, reviewer_user_id: str, decided_by: AuthenticatedUser) -> dict[str, Any]:
        self.assert_permission(decided_by, "approvals:approve")
        approval = next((item for item in self._scoped_items("approvals", decided_by.organization_id) if item["id"] == approval_id), None)
        if not approval:
            raise NotFoundError(f"Approval not found: {approval_id}")
        reviewer = next((item for item in self._scoped_items("users", decided_by.organization_id) if item["id"] == reviewer_user_id), None)
        if not reviewer:
            raise NotFoundError(f"Reviewer not found: {reviewer_user_id}")
        approval["assigned_reviewer"] = reviewer_user_id
        self._append_audit(decided_by.organization_id, decided_by.id, "approval", "approval.reassigned", "approval", approval_id, {"reviewer_user_id": reviewer_user_id}, "success")
        self.store.save()
        return deepcopy(approval)

    def create_memory_item(self, requested_by: AuthenticatedUser, payload: dict[str, Any], *, acting_agent_id: str | None = None) -> dict[str, Any]:
        self.assert_permission(requested_by, "memory:write")
        agent = None
        if acting_agent_id:
            agent = next((a for a in self._scoped_items("agents", requested_by.organization_id) if a["id"] == acting_agent_id), None)
            if not agent:
                raise NotFoundError(f"Agent not found: {acting_agent_id}")
            self.assert_memory_scope_allowed(
                agent=agent,
                scope=payload["scope"],
                action="write",
                organization_id=requested_by.organization_id,
                actor_user_id=requested_by.id,
            )
        provenance = payload.get("provenance") or {
            "source_refs": ["api"],
            "captured_by": requested_by.id,
            "recorded_at": utc_now(),
        }
        if "source_refs" not in provenance:
            provenance["source_refs"] = ["api"]
        item = {
            "id": f"mem_{uuid.uuid4().hex[:12]}",
            "organization_id": requested_by.organization_id,
            "owner": requested_by.id,
            "department": payload.get("department", "general"),
            "scope": payload["scope"],
            "title": payload["title"],
            "content": payload["content"],
            "metadata": payload.get("metadata", {}),
            "embedding_reference": payload.get("embedding_reference"),
            "sensitivity_level": payload.get("sensitivity_level", "internal"),
            "allowed_roles": payload.get("allowed_roles", [requested_by.role]),
            "expires_at": payload.get("expires_at"),
            "provenance": provenance,
            "created_at": utc_now(),
        }
        self.store.collection("memory_items").append(item)
        self._append_audit(requested_by.organization_id, requested_by.id, "memory", "memory.created", "memory", item["id"], {"scope": item["scope"]}, "success")
        self.store.save()
        return deepcopy(item)

    def get_memory_item(self, requested_by: AuthenticatedUser, memory_id: str) -> dict[str, Any]:
        items = self.search_memory(requested_by)
        item = next((entry for entry in items if entry["id"] == memory_id), None)
        if not item:
            raise NotFoundError(f"Memory item not found: {memory_id}")
        return deepcopy(item)

    def update_memory_item(self, requested_by: AuthenticatedUser, memory_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(requested_by, "memory:write")
        item = next((entry for entry in self._scoped_items("memory_items", requested_by.organization_id) if entry["id"] == memory_id), None)
        if not item:
            raise NotFoundError(f"Memory item not found: {memory_id}")
        if item["owner"] != requested_by.id and requested_by.role not in {"owner", "admin"}:
            raise PermissionDeniedError("Memory item can only be updated by its owner or an admin")
        for field in ["title", "content", "scope", "department", "embedding_reference", "sensitivity_level", "expires_at"]:
            if field in payload and payload[field] is not None:
                item[field] = payload[field]
        if "metadata" in payload and payload["metadata"] is not None:
            item["metadata"] = payload["metadata"]
        if "allowed_roles" in payload and payload["allowed_roles"]:
            item["allowed_roles"] = payload["allowed_roles"]
        self._append_audit(requested_by.organization_id, requested_by.id, "memory", "memory.updated", "memory", memory_id, {}, "success")
        self.store.save()
        return deepcopy(item)

    def delete_memory_item(self, requested_by: AuthenticatedUser, memory_id: str) -> dict[str, Any]:
        self.assert_permission(requested_by, "memory:write")
        items = self.store.collection("memory_items")
        index = next((idx for idx, entry in enumerate(items) if entry["id"] == memory_id and entry["organization_id"] == requested_by.organization_id), None)
        if index is None:
            raise NotFoundError(f"Memory item not found: {memory_id}")
        item = items[index]
        if item["owner"] != requested_by.id and requested_by.role not in {"owner", "admin"}:
            raise PermissionDeniedError("Memory item can only be deleted by its owner or an admin")
        items.pop(index)
        self._append_audit(requested_by.organization_id, requested_by.id, "memory", "memory.deleted", "memory", memory_id, {}, "success")
        self.store.save()
        return {"id": memory_id, "status": "deleted"}

    def search_memory(
        self,
        requested_by: AuthenticatedUser,
        query: str | None = None,
        scope: str | None = None,
        *,
        acting_agent_id: str | None = None,
    ) -> list[dict[str, Any]]:
        self.assert_permission(requested_by, "memory:read")
        agent = None
        if acting_agent_id:
            agent = next((a for a in self._scoped_items("agents", requested_by.organization_id) if a["id"] == acting_agent_id), None)
            if not agent:
                raise NotFoundError(f"Agent not found: {acting_agent_id}")
            # If a specific scope is requested, enforce agent allow-list before returning hits
            if scope:
                self.assert_memory_scope_allowed(
                    agent=agent,
                    scope=scope,
                    action="read",
                    organization_id=requested_by.organization_id,
                    actor_user_id=requested_by.id,
                )
        allowed_scopes = self._agent_allowed_scopes(agent) if agent else None
        results = []
        for item in self._scoped_items("memory_items", requested_by.organization_id):
            expires_at = parse_dt(item.get("expires_at"))
            if expires_at and expires_at <= datetime.now(UTC):
                continue
            if requested_by.role not in item.get("allowed_roles", [requested_by.role]) and requested_by.role != "owner":
                continue
            if scope and item["scope"] != scope:
                continue
            if allowed_scopes is not None and item.get("scope") not in allowed_scopes:
                continue
            if query and query.lower() not in f"{item.get('title', '')} {item.get('content', '')}".lower():
                continue
            if item.get("sensitivity_level") in {"restricted", "confidential"}:
                self._append_audit(requested_by.organization_id, requested_by.id, "memory", "memory.accessed", "memory", item["id"], {"sensitivity_level": item["sensitivity_level"]}, "success")
            results.append(item)
        self.store.save()
        return deepcopy(results)

    def upload_knowledge_document(self, requested_by: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(requested_by, "knowledge:write")
        source = payload.get("source") or payload.get("path") or f"uploads/{payload['id']}.md"
        document = {
            "id": payload["id"],
            "organization_id": requested_by.organization_id,
            "title": payload["title"],
            "path": payload.get("path", f"uploads/{payload['id']}.md"),
            "source": source,
            "content": payload["content"],
            "status": payload.get("status", "indexed"),
            "sensitivity": payload.get("sensitivity", "internal"),
            "allowed_roles": payload.get("allowed_roles", ["owner", "admin", "manager", "operator", "reviewer", "viewer"]),
            "failure_reason": payload.get("failure_reason"),
            "provenance": payload.get("provenance") or {
                "source_refs": [source],
                "captured_by": requested_by.id,
                "recorded_at": utc_now(),
            },
            "created_at": utc_now(),
        }
        self.store.collection("knowledge_documents").append(document)
        self._append_audit(requested_by.organization_id, requested_by.id, "knowledge", "knowledge.uploaded", "knowledge", document["id"], {"status": document["status"]}, "success")
        self.store.save()
        return deepcopy(document)

    def get_knowledge_document(self, requested_by: AuthenticatedUser, document_id: str) -> dict[str, Any]:
        self.assert_permission(requested_by, "knowledge:read")
        document = next((doc for doc in self._scoped_items("knowledge_documents", requested_by.organization_id) if doc["id"] == document_id), None)
        if not document:
            raise NotFoundError(f"Knowledge document not found: {document_id}")
        if requested_by.role not in document.get("allowed_roles", [requested_by.role]) and requested_by.role != "owner":
            raise PermissionDeniedError("Knowledge document access denied")
        return deepcopy(document)

    def index_knowledge_document(self, requested_by: AuthenticatedUser, document_id: str) -> dict[str, Any]:
        self.assert_permission(requested_by, "knowledge:write")
        document = next((doc for doc in self._scoped_items("knowledge_documents", requested_by.organization_id) if doc["id"] == document_id), None)
        if not document:
            raise NotFoundError(f"Knowledge document not found: {document_id}")
        document["status"] = "indexed" if document.get("content") else "failed"
        document["failure_reason"] = None if document["status"] == "indexed" else "Missing content"
        if document["status"] == "indexed":
            from app.core.config import settings as app_settings
            from app.infrastructure.knowledge.embeddings import embed_text, try_upsert_pgvector
            from app.infrastructure.knowledge.retrieval import extract_entity_links
            from app.infrastructure.knowledge_orchestration.extract import extract_document_graph

            document["entity_links"] = extract_entity_links(
                f"{document.get('title', '')} {document.get('content', '')}",
                source=document.get("source") or document.get("path"),
            )
            # Agents-K1 lite: populate knowledge graph on index
            graph = extract_document_graph(document)
            self._merge_knowledge_graph(requested_by.organization_id, graph)
            document["graph_node_count"] = len(graph.get("nodes") or [])
            document["graph_edge_count"] = len(graph.get("edges") or [])
            if app_settings.embeddings_enabled:
                emb = embed_text(f"{document.get('title', '')} {document.get('content', '')}")
                document["embedding"] = emb
                document["embedding_dims"] = len(emb)
                document["pgvector"] = try_upsert_pgvector(document_id, emb, app_settings)
        self._append_audit(
            requested_by.organization_id,
            requested_by.id,
            "knowledge",
            "knowledge.indexed",
            "knowledge",
            document_id,
            {
                "status": document["status"],
                "entity_link_count": len(document.get("entity_links") or []),
                "graph_node_count": document.get("graph_node_count", 0),
            },
            "success",
        )
        self.store.save()
        return deepcopy(document)

    def archive_knowledge_document(self, requested_by: AuthenticatedUser, document_id: str) -> dict[str, Any]:
        self.assert_permission(requested_by, "knowledge:write")
        document = next((doc for doc in self._scoped_items("knowledge_documents", requested_by.organization_id) if doc["id"] == document_id), None)
        if not document:
            raise NotFoundError(f"Knowledge document not found: {document_id}")
        document["status"] = "archived"
        self._append_audit(requested_by.organization_id, requested_by.id, "knowledge", "knowledge.archived", "knowledge", document_id, {}, "success")
        self.store.save()
        return deepcopy(document)

    def search_knowledge(
        self,
        requested_by: AuthenticatedUser,
        query: str | None = None,
        *,
        multi_hop: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Tiered retrieval: Tier 0 keyword + optional Tier 1 entity-link multi-hop.

        Always attaches provenance/source_refs (structure.md §3.4).
        """
        self.assert_permission(requested_by, "knowledge:read")
        from app.infrastructure.knowledge.retrieval import (
            RETRIEVAL_TIER_NOTE,
            expand_multi_hop,
            extract_entity_links,
            score_keyword_hit,
            should_escalate_to_tier1,
        )

        accessible: list[dict[str, Any]] = []
        for doc in self._scoped_items("knowledge_documents", requested_by.organization_id):
            if requested_by.role not in doc.get("allowed_roles", [requested_by.role]) and requested_by.role != "owner":
                continue
            if doc.get("status", "indexed") not in {"indexed", "processing", "failed"}:
                continue
            accessible.append(doc)

        # Tier 0: keyword + optional embedding rank
        from app.core.config import settings as app_settings
        from app.infrastructure.knowledge.embeddings import cosine_similarity, embed_text

        tier0: list[dict[str, Any]] = []
        q_emb = embed_text(query) if query and app_settings.embeddings_enabled else None
        for doc in accessible:
            title = doc.get("title", "") or ""
            content = doc.get("content", "") or ""
            if query:
                score = score_keyword_hit(query, title, content)
                substring_hit = query.lower() in f"{title} {content}".lower()
                # Keep substring match for short queries / demo SOP titles
                if score <= 0 and not substring_hit:
                    # Pure embedding hits only when not in multi-hop seed mode
                    # (keeps Tier-1 expansion seeds precise)
                    if q_emb is None or multi_hop:
                        continue
                    emb = doc.get("embedding") or embed_text(f"{title} {content}")
                    emb_score = cosine_similarity(q_emb, emb)
                    if emb_score < 0.35:
                        continue
                    score = emb_score
                elif q_emb is not None and (score > 0 or substring_hit):
                    emb = doc.get("embedding") or embed_text(f"{title} {content}")
                    # Blend keyword + embedding for ranked keyword hits
                    kw = score if score > 0 else 0.5
                    score = round(0.6 * kw + 0.4 * cosine_similarity(q_emb, emb), 4)
            else:
                score = 0.0
            hit = deepcopy(doc)
            if not hit.get("entity_links"):
                hit["entity_links"] = extract_entity_links(
                    f"{title} {content}",
                    source=hit.get("source") or hit.get("path"),
                )
            hit["retrieval_score"] = score
            hit["retrieval_hop"] = 0
            tier0.append(hit)

        tier0.sort(key=lambda item: item.get("retrieval_score") or 0, reverse=True)
        escalate = should_escalate_to_tier1(query, force=bool(multi_hop))
        hits = list(tier0)
        retrieval_tier = 0
        if escalate and tier0:
            # Expand from all Tier-0 seeds when multi-hop (precision path); otherwise top-K
            seeds = tier0 if multi_hop else tier0[:8]
            extras = expand_multi_hop(seeds, accessible, max_extra=50 if multi_hop else 15)
            for extra in extras:
                if not any(h.get("id") == extra.get("id") for h in hits):
                    hits.append(extra)
            if extras:
                retrieval_tier = 1

        documents: list[dict[str, Any]] = []
        for hit in hits:
            provenance = hit.get("provenance") or {}
            source_refs = list(provenance.get("source_refs") or [])
            if hit.get("source") and hit["source"] not in source_refs:
                source_refs.append(hit["source"])
            if not source_refs:
                source_refs = [f"knowledge:{hit.get('id')}"]
            hop = int(hit.get("retrieval_hop") or 0)
            hit_tier = 1 if hop > 0 else 0
            hit["provenance"] = {
                **provenance,
                "source_refs": source_refs,
                "retrieval_tier": hit_tier,
                "retrieval_policy": RETRIEVAL_TIER_NOTE,
                "captured_by": provenance.get("captured_by") or "knowledge_search",
                "recorded_at": provenance.get("recorded_at") or utc_now(),
            }
            hit["source_refs"] = source_refs
            hit["retrieval_tier"] = hit_tier
            documents.append(hit)

        # Annotate response meta on first hit for clients (optional)
        if documents:
            documents[0] = {
                **documents[0],
                "search_meta": {
                    "query": query,
                    "tier_used": retrieval_tier,
                    "tier0_hits": len(tier0),
                    "total_hits": len(documents),
                    "policy": RETRIEVAL_TIER_NOTE,
                },
            }
        return documents

    def list_evaluations(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "evaluations:read")
        return deepcopy(self._scoped_items("evaluation_runs", current_user.organization_id))

    def get_evaluation(self, current_user: AuthenticatedUser, evaluation_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "evaluations:read")
        evaluation = next((item for item in self._scoped_items("evaluation_runs", current_user.organization_id) if item["id"] == evaluation_id), None)
        if not evaluation:
            raise NotFoundError(f"Evaluation not found: {evaluation_id}")
        return deepcopy(evaluation)

    def run_evaluation(self, current_user: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "evaluations:read")
        run = next((item for item in self._scoped_items("workflow_runs", current_user.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        evaluation = self._create_evaluation(run)
        run.setdefault("evaluation_results", []).append(evaluation["id"])
        self._append_audit(current_user.organization_id, current_user.id, "evaluation", "evaluation.created", "evaluation", evaluation["id"], {"run_id": run_id}, "success")
        self.store.save()
        return deepcopy(evaluation)

    def list_run_evaluations(self, current_user: AuthenticatedUser, run_id: str) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "evaluations:read")
        evaluations = [item for item in self._scoped_items("evaluation_runs", current_user.organization_id) if item.get("run_id") == run_id]
        return deepcopy(evaluations)

    def _create_evaluation(self, run: dict[str, Any]) -> dict[str, Any]:
        seed = self.loader.load_eval_card()
        outcome = run["output"] or {}
        result = "passed" if outcome.get("outcome") == "completed" else "failed"
        evaluation = {
            "id": f"eval_{uuid.uuid4().hex[:12]}",
            "organization_id": run["organization_id"],
            "run_id": run["id"],
            "workflow_id": run["workflow_id"],
            "step_id": None,
            "target": run["workflow_id"],
            "eval_type": seed["eval_type"],
            "test_set": seed["test_set"],
            "metrics": deepcopy(seed["metrics"]),
            "status": result,
            "result": result,
            "promotion_decision": "canary_only" if result == "passed" else "blocked",
            "reviewer": "evaluation_harness",
            "created_at": utc_now(),
        }
        self.store.collection("evaluation_runs").append(evaluation)
        return evaluation

    def list_audit_logs(self, current_user: AuthenticatedUser, action: str | None = None, resource_type: str | None = None) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "audit:read")
        logs = []
        for item in self._scoped_items("audit_logs", current_user.organization_id):
            if action and item["action"] != action:
                continue
            if resource_type and item["resource_type"] != resource_type:
                continue
            logs.append(item)
        return deepcopy(logs)

    def get_audit_log(self, current_user: AuthenticatedUser, audit_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "audit:read")
        log = next((item for item in self._scoped_items("audit_logs", current_user.organization_id) if item["id"] == audit_id), None)
        if not log:
            raise NotFoundError(f"Audit log not found: {audit_id}")
        return deepcopy(log)

    def process_summary(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        self.assert_permission(current_user, "processes:read")
        runs = self._scoped_items("workflow_runs", current_user.organization_id)
        completed = [run for run in runs if run["status"] == "completed"]
        failed = [run for run in runs if run["status"] == "failed"]
        waiting = [run for run in runs if run["status"] == "waiting_for_approval"]
        approval_durations = []
        for approval in self._scoped_items("approvals", current_user.organization_id):
            approval_started_at = approval.get("created_at") or approval.get("requested_at")
            approval_decided_at = approval.get("decided_at")
            if approval_started_at and approval_decided_at:
                approval_durations.append((parse_dt(approval_decided_at) - parse_dt(approval_started_at)).total_seconds() / 60)
        return {
            "processes": deepcopy(self.store.collection("process_metrics")),
            "workflow_run_count": len(runs),
            "completed_run_count": len(completed),
            "failed_run_count": len(failed),
            "waiting_for_approval_count": len(waiting),
            "average_workflow_duration_seconds": round(sum((parse_dt(run["completed_at"]) - parse_dt(run["started_at"])).total_seconds() for run in completed if run.get("started_at") and run.get("completed_at")) / max(len(completed), 1), 2) if completed else 0,
            "approval_wait_time_minutes": round(sum(approval_durations) / max(len(approval_durations), 1), 2) if approval_durations else 0,
            "most_failed_workflows": self._most_failed_workflows(runs),
            "audit_event_count": len(self._scoped_items("audit_logs", current_user.organization_id)),
            "memory_item_count": len(self._scoped_items("memory_items", current_user.organization_id)),
        }

    def process_metrics(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        return deepcopy(self.store.collection("process_metrics"))

    def workflow_performance(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        summary = self.process_summary(current_user)
        return deepcopy(summary["most_failed_workflows"] + [{
            "workflow_name": "all_workflows",
            "average_duration_seconds": summary["average_workflow_duration_seconds"],
            "completed_run_count": summary["completed_run_count"],
        }])

    def process_bottlenecks(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        waiting_runs = [run for run in self._scoped_items("workflow_runs", current_user.organization_id) if run["status"] == "waiting_for_approval"]
        return deepcopy([
            {
                "type": "approval_wait",
                "count": len(waiting_runs),
                "message": "Runs waiting on approval" if waiting_runs else "No approval bottlenecks detected",
            }
        ])

    def approval_delays(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        summary = self.process_summary(current_user)
        return {
            "approval_wait_time_minutes": summary["approval_wait_time_minutes"],
            "waiting_for_approval_count": summary["waiting_for_approval_count"],
        }

    def process_costs(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        self.assert_permission(current_user, "processes:read")
        runs = self._scoped_items("workflow_runs", current_user.organization_id)
        total_cost = round(sum(run.get("cost_usage", 0) for run in runs), 2)
        return {"total_cost_usage": total_cost, "workflow_run_count": len(runs)}

    def process_failures(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        return deepcopy(self._most_failed_workflows(self._scoped_items("workflow_runs", current_user.organization_id)))

    def list_governance_policies(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "governance:read")
        return deepcopy(self._scoped_items("governance_policies", current_user.organization_id))

    def create_governance_policy(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "governance:update")
        policy = {
            "id": payload.get("id", f"pol_{uuid.uuid4().hex[:10]}"),
            "organization_id": current_user.organization_id,
            "name": payload["name"],
            "conditions": payload.get("conditions", {}),
            "action": payload.get("action", "allow"),
            "reviewer_role": payload.get("reviewer_role"),
            "risk_level": payload.get("risk_level", "medium"),
            "status": payload.get("status", "active"),
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        self.store.collection("governance_policies").append(policy)
        self._append_audit(current_user.organization_id, current_user.id, "governance", "governance.policy_created", "governance_policy", policy["id"], {}, "success")
        self.store.save()
        return deepcopy(policy)

    def get_governance_policy(self, current_user: AuthenticatedUser, policy_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "governance:read")
        policy = next((item for item in self._scoped_items("governance_policies", current_user.organization_id) if item["id"] == policy_id), None)
        if not policy:
            raise NotFoundError(f"Governance policy not found: {policy_id}")
        return deepcopy(policy)

    def update_governance_policy(self, current_user: AuthenticatedUser, policy_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "governance:update")
        policy = next((item for item in self._scoped_items("governance_policies", current_user.organization_id) if item["id"] == policy_id), None)
        if not policy:
            raise NotFoundError(f"Governance policy not found: {policy_id}")
        for field in ["name", "conditions", "action", "reviewer_role", "risk_level", "status"]:
            if field in payload and payload[field] is not None:
                policy[field] = payload[field]
        policy["updated_at"] = utc_now()
        self._append_audit(current_user.organization_id, current_user.id, "governance", "governance.policy_updated", "governance_policy", policy_id, {}, "success")
        self.store.save()
        return deepcopy(policy)

    def archive_governance_policy(self, current_user: AuthenticatedUser, policy_id: str) -> dict[str, Any]:
        return self.update_governance_policy(current_user, policy_id, {"status": "archived"})

    def governance_check(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "governance:read")
        action = payload.get("action", "allow")
        matching = []
        for policy in self._scoped_items("governance_policies", current_user.organization_id):
            if policy.get("status") != "active":
                continue
            conditions = policy.get("conditions", {})
            if all(payload.get(key) == value for key, value in conditions.items()):
                matching.append(policy)
        if matching:
            first = matching[0]
            return {
                "decision": first["action"],
                "matched_policy_id": first["id"],
                "matched_policy_name": first["name"],
                "reviewer_role": first.get("reviewer_role"),
                "risk_level": first.get("risk_level"),
            }
        return {"decision": action, "matched_policy_id": None, "matched_policy_name": None, "reviewer_role": None, "risk_level": payload.get("risk_level")}

    def _most_failed_workflows(self, runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        for run in runs:
            if run["status"] == "failed":
                counts[run["workflow_name"]] = counts.get(run["workflow_name"], 0) + 1
        return [{"workflow_name": name, "failed_runs": count} for name, count in sorted(counts.items(), key=lambda item: item[1], reverse=True)]

    def settings(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        self.assert_permission(current_user, "settings:read")
        from app.infrastructure.database.session import database_status

        db = database_status()
        return {
            "api_version": "v1",
            "runtime_mode": "postgres" if self.store.backend == "postgres" else "local-json-store",
            "persistence": {
                "store_backend": self.store.backend,
                "database": db,
            },
            "streaming": "sse",
            "governance": self.loader.load_risk_tiers(),
            "business_source_dir": "business/",
            "auth_modes": ["bearer", "refresh_token", "api_key"],
        }

    def stream_run_events(self, current_user: AuthenticatedUser, run_id: str) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "workflow_runs:read")
        run = next((item for item in self._scoped_items("workflow_runs", current_user.organization_id) if item["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        events = [item for item in self.store.collection("stream_events") if item["workflow_run_id"] == run_id]
        return deepcopy(events)

    # --- Process intelligence: event logs ---

    def ingest_event_log(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "processes:read")
        # writers with knowledge:write or workflows:execute may also ingest; use processes:read as baseline + role check
        if current_user.role not in {"owner", "admin", "manager", "operator"} and "*" not in ROLE_PERMISSIONS.get(current_user.role, set()):
            raise PermissionDeniedError("Event log ingest requires operator role or higher")
        event = {
            "id": payload.get("id") or f"evt_{uuid.uuid4().hex[:12]}",
            "organization_id": current_user.organization_id,
            "timestamp": payload.get("timestamp") or utc_now(),
            "actor_type": payload.get("actor_type", "system"),
            "actor_id": payload.get("actor_id") or current_user.id,
            "process_id": payload.get("process_id") or "unknown_process",
            "case_id": payload.get("case_id") or f"case_{uuid.uuid4().hex[:8]}",
            "activity": payload.get("activity") or "unspecified",
            "input_refs": payload.get("input_refs") or [],
            "output_refs": payload.get("output_refs") or [],
            "tools_used": payload.get("tools_used") or [],
            "decision_point": bool(payload.get("decision_point", False)),
            "decision_reason_summary": payload.get("decision_reason_summary"),
            "confidence": payload.get("confidence"),
            "risk_tier": payload.get("risk_tier") or "tier_2_draft",
            "human_approved": bool(payload.get("human_approved", False)),
            "outcome": payload.get("outcome") or {"status": "completed"},
            "provenance": payload.get("provenance") or {
                "source_refs": ["event_log_api"],
                "captured_by": current_user.id,
                "recorded_at": utc_now(),
            },
        }
        self.store.collection("event_logs").append(event)
        artifacts = self._refresh_pi_artifacts(current_user.organization_id, process_id=event["process_id"])
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "process",
            "event_log.ingested",
            "event_log",
            event["id"],
            {
                "process_id": event["process_id"],
                "case_id": event["case_id"],
                "activity": event["activity"],
                "pi_artifacts_written": len(artifacts),
            },
            "success",
        )
        self.store.save()
        result = deepcopy(event)
        result["pi_artifacts"] = [
            {"id": a.get("id"), "artifact_type": a.get("artifact_type"), "relative_path": a.get("relative_path")}
            for a in artifacts
        ]
        return result

    def list_event_logs(self, current_user: AuthenticatedUser, process_id: str | None = None, case_id: str | None = None) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        items = []
        for event in self._scoped_items("event_logs", current_user.organization_id):
            if process_id and event.get("process_id") != process_id:
                continue
            if case_id and event.get("case_id") != case_id:
                continue
            items.append(event)
        return deepcopy(items)

    def process_summary(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        self.assert_permission(current_user, "processes:read")
        runs = self._scoped_items("workflow_runs", current_user.organization_id)
        completed = [run for run in runs if run["status"] == "completed"]
        failed = [run for run in runs if run["status"] == "failed"]
        waiting = [run for run in runs if run["status"] == "waiting_for_approval"]
        approval_durations = []
        for approval in self._scoped_items("approvals", current_user.organization_id):
            approval_started_at = approval.get("created_at") or approval.get("requested_at")
            approval_decided_at = approval.get("decided_at")
            if approval_started_at and approval_decided_at:
                approval_durations.append((parse_dt(approval_decided_at) - parse_dt(approval_started_at)).total_seconds() / 60)
        events = self._scoped_items("event_logs", current_user.organization_id)
        activity_counts: dict[str, int] = {}
        outcome_counts: dict[str, int] = {}
        case_ids: set[str] = set()
        for event in events:
            activity = event.get("activity") or "unknown"
            activity_counts[activity] = activity_counts.get(activity, 0) + 1
            status = (event.get("outcome") or {}).get("status") or "unknown"
            outcome_counts[status] = outcome_counts.get(status, 0) + 1
            if event.get("case_id"):
                case_ids.add(event["case_id"])
        return {
            "processes": deepcopy(self.store.collection("process_metrics")),
            "workflow_run_count": len(runs),
            "completed_run_count": len(completed),
            "failed_run_count": len(failed),
            "waiting_for_approval_count": len(waiting),
            "average_workflow_duration_seconds": round(sum((parse_dt(run["completed_at"]) - parse_dt(run["started_at"])).total_seconds() for run in completed if run.get("started_at") and run.get("completed_at")) / max(len(completed), 1), 2) if completed else 0,
            "approval_wait_time_minutes": round(sum(approval_durations) / max(len(approval_durations), 1), 2) if approval_durations else 0,
            "most_failed_workflows": self._most_failed_workflows(runs),
            "audit_event_count": len(self._scoped_items("audit_logs", current_user.organization_id)),
            "memory_item_count": len(self._scoped_items("memory_items", current_user.organization_id)),
            "event_log_count": len(events),
            "distinct_case_count": len(case_ids),
            "activity_counts": activity_counts,
            "outcome_counts": outcome_counts,
        }

    def _compute_bottlenecks(self, organization_id: str) -> list[dict[str, Any]]:
        waiting_runs = [run for run in self._scoped_items("workflow_runs", organization_id) if run["status"] == "waiting_for_approval"]
        bottlenecks: list[dict[str, Any]] = [
            {
                "type": "approval_wait",
                "count": len(waiting_runs),
                "message": "Runs waiting on approval" if waiting_runs else "No approval bottlenecks detected",
            }
        ]
        latency_by_activity: dict[str, list[float]] = {}
        for event in self._scoped_items("event_logs", organization_id):
            outcome = event.get("outcome") or {}
            latency = outcome.get("latency_minutes")
            if latency is None:
                continue
            activity = event.get("activity") or "unknown"
            latency_by_activity.setdefault(activity, []).append(float(latency))
        for activity, values in sorted(latency_by_activity.items(), key=lambda kv: sum(kv[1]) / len(kv[1]), reverse=True):
            avg = round(sum(values) / len(values), 2)
            if avg >= 30:
                bottlenecks.append(
                    {
                        "type": "activity_latency",
                        "activity": activity,
                        "count": len(values),
                        "average_latency_minutes": avg,
                        "message": f"Activity {activity} average latency {avg} minutes",
                    }
                )
        return bottlenecks

    def _compute_discovered(self, organization_id: str) -> list[dict[str, Any]]:
        by_process: dict[str, dict[str, Any]] = {}
        for event in self._scoped_items("event_logs", organization_id):
            pid = event.get("process_id") or "unknown"
            bucket = by_process.setdefault(pid, {"process_id": pid, "activities": [], "case_ids": set(), "event_count": 0})
            bucket["event_count"] += 1
            activity = event.get("activity")
            if activity and activity not in bucket["activities"]:
                bucket["activities"].append(activity)
            if event.get("case_id"):
                bucket["case_ids"].add(event["case_id"])
        results = []
        for pid, bucket in by_process.items():
            results.append(
                {
                    "process_id": pid,
                    "activities": bucket["activities"],
                    "case_count": len(bucket["case_ids"]),
                    "event_count": bucket["event_count"],
                    "discovered_from": "event_logs",
                }
            )
        return results

    def _compute_conformance(self, organization_id: str, process_id: str | None = None) -> dict[str, Any]:
        events = [
            e
            for e in self._scoped_items("event_logs", organization_id)
            if not process_id or e.get("process_id") == process_id
        ]
        expected = {
            "verify_contract",
            "create_customer_record",
            "activate_billing",
            "send_welcome_packet",
            "audit_and_close",
        }
        observed = {e.get("activity") for e in events if e.get("activity")}
        missing = sorted(expected - observed)
        extra = sorted(observed - expected)
        return {
            "process_id": process_id or "all",
            "expected_activities": sorted(expected),
            "observed_activities": sorted(observed),
            "missing_activities": missing,
            "extra_activities": extra,
            "conformance_score": round(1.0 - (len(missing) / max(len(expected), 1)), 2),
            "event_count": len(events),
        }

    def _pi_artifact_index(self, organization_id: str) -> dict[str, dict[str, Any]]:
        index: dict[str, dict[str, Any]] = {}
        for item in self._scoped_items("pi_artifacts", organization_id):
            key = f"{item.get('artifact_type')}:{item.get('process_id') or item.get('id')}"
            index[key] = item
            if item.get("relative_path"):
                index[str(item["relative_path"])] = item
        return index

    def _refresh_pi_artifacts(self, organization_id: str, *, process_id: str | None = None) -> list[dict[str, Any]]:
        """Recompute PI views and write disk + store artifacts (P3)."""
        from app.infrastructure.process_intelligence.artifacts import write_pi_artifacts

        discovered = self._compute_discovered(organization_id)
        bottlenecks = self._compute_bottlenecks(organization_id)
        process_ids = {d["process_id"] for d in discovered}
        if process_id:
            process_ids.add(process_id)
        conformance_by_process = {
            pid: self._compute_conformance(organization_id, process_id=pid) for pid in sorted(process_ids)
        }
        # Also keep an "all" conformance snapshot
        conformance_by_process["all"] = self._compute_conformance(organization_id, process_id=None)

        written = write_pi_artifacts(
            self.repo_root,
            organization_id=organization_id,
            discovered=discovered,
            conformance_by_process=conformance_by_process,
            bottlenecks=bottlenecks,
        )
        # Upsert into runtime store (Postgres-backed)
        existing = {
            (item.get("artifact_type"), item.get("process_id") or item.get("id")): item
            for item in self.store.collection("pi_artifacts")
            if item.get("organization_id") == organization_id
        }
        for artifact in written:
            key = (artifact.get("artifact_type"), artifact.get("process_id") or artifact.get("id"))
            prior = existing.get(key)
            if prior:
                prior.update(artifact)
            else:
                self.store.collection("pi_artifacts").append(artifact)
        return written

    def process_bottlenecks(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        bottlenecks = self._compute_bottlenecks(current_user.organization_id)
        index = self._pi_artifact_index(current_user.organization_id)
        artifact = index.get("bottleneck_report:all") or next(
            (v for k, v in index.items() if k.startswith("bottleneck_report:")),
            None,
        )
        if artifact:
            for item in bottlenecks:
                item.setdefault("artifact_path", artifact.get("relative_path") or artifact.get("artifact_path"))
        return deepcopy(bottlenecks)

    def discovered_processes(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        results = self._compute_discovered(current_user.organization_id)
        index = self._pi_artifact_index(current_user.organization_id)
        for item in results:
            art = index.get(f"discovered_process:{item['process_id']}")
            if art:
                item["artifact_path"] = art.get("relative_path") or art.get("artifact_path")
                item["artifact_id"] = art.get("id")
        return deepcopy(results)

    def conformance_report(self, current_user: AuthenticatedUser, process_id: str | None = None) -> dict[str, Any]:
        self.assert_permission(current_user, "processes:read")
        report = self._compute_conformance(current_user.organization_id, process_id=process_id)
        index = self._pi_artifact_index(current_user.organization_id)
        key_pid = process_id or "all"
        art = index.get(f"conformance_report:{key_pid}")
        if art:
            report["artifact_path"] = art.get("relative_path") or art.get("artifact_path")
            report["artifact_id"] = art.get("id")
        return deepcopy(report)

    def list_pi_artifacts(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "processes:read")
        return deepcopy(self._scoped_items("pi_artifacts", current_user.organization_id))

    # --- Evolution sandbox (structure.md §5 — never mutate production DNA directly) ---

    def propose_evolution_variant(self, current_user: AuthenticatedUser, payload: dict[str, Any]) -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:create")
        if payload.get("direct_production_mutation") is True:
            self._append_audit(
                current_user.organization_id,
                current_user.id,
                "evolution",
                "evolution.direct_mutation_blocked",
                "evolution_variant",
                "blocked",
                {"reason": "direct_production_mutation_forbidden"},
                "failed",
            )
            self.store.save()
            raise PermissionDeniedError("Evolution path must never mutate production DNA directly")
        variant_type = payload.get("variant_type") or payload.get("type") or "workflow_dna"
        if variant_type == "agent_genome" and not payload.get("agent_id"):
            raise ValidationError("agent_genome variants require agent_id")
        base_workflow_id = payload.get("base_workflow_id")
        base = None
        if base_workflow_id:
            base = next((w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == base_workflow_id), None)
            if not base:
                raise NotFoundError(f"Base workflow not found: {base_workflow_id}")
        # Snapshot production DNA before any sandbox work — production collection untouched
        production_snapshot = deepcopy(base) if base else None
        variant = {
            "id": payload.get("id") or f"var_{uuid.uuid4().hex[:12]}",
            "organization_id": current_user.organization_id,
            "base_workflow_id": base_workflow_id,
            "name": payload.get("name") or f"Variant of {base_workflow_id or 'new'}",
            "status": "sandbox_proposed",
            "direct_production_mutation": False,
            "sandbox_only": True,
            "variant_type": variant_type,
            "agent_id": payload.get("agent_id"),
            "genome": payload.get("genome") if variant_type == "agent_genome" else None,
            "dna": payload.get("dna") or (deepcopy(base) if base else {}),
            "changes": payload.get("changes") or [],
            "rollback_plan": payload.get("rollback_plan")
            or ((payload.get("dna") or {}).get("rollback") or {}).get("rollback_steps")
            or [],
            "created_by": current_user.id,
            "created_at": utc_now(),
            "evaluation": None,
            "fitness_metrics": None,
            "promotion_decision": None,
            "production_snapshot_id": production_snapshot["id"] if production_snapshot else None,
        }
        if isinstance(variant["dna"], dict):
            variant["dna"]["id"] = variant["dna"].get("id") or f"{base_workflow_id or 'wf'}_sandbox_{variant['id']}"
            variant["dna"]["status"] = "sandbox"
            variant["dna"]["production_ready"] = False
        self.store.collection("evolution_variants").append(variant)
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "evolution",
            "evolution.variant_proposed",
            "evolution_variant",
            variant["id"],
            {"base_workflow_id": base_workflow_id, "sandbox_only": True},
            "success",
        )
        self.store.save()
        # Verify production DNA unchanged
        if base_workflow_id and production_snapshot:
            current = next((w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == base_workflow_id), None)
            if current and current.get("version") != production_snapshot.get("version"):
                raise ValidationError("Invariant violated: production DNA changed during propose")
        return deepcopy(variant)

    def sandbox_evaluate_variant(self, current_user: AuthenticatedUser, variant_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "evaluations:read")
        variant = next((v for v in self._scoped_items("evolution_variants", current_user.organization_id) if v["id"] == variant_id), None)
        if not variant:
            raise NotFoundError(f"Evolution variant not found: {variant_id}")
        if variant.get("direct_production_mutation"):
            raise PermissionDeniedError("Sandbox eval refused: variant marked for direct production mutation")
        from app.infrastructure.evolution.corpus_eval import evaluate_variant_against_corpus

        dna = variant.get("dna") or {}
        # Attach base workflow id for target matching when DNA id is sandbox-scoped
        if not dna.get("id") and variant.get("base_workflow_id"):
            dna = {**dna, "id": variant["base_workflow_id"]}
        evaluation = evaluate_variant_against_corpus(
            dna,
            self.repo_root,
            variant_meta={
                "sandbox_only": variant.get("sandbox_only", True),
                "variant_id": variant_id,
                "domain_id": (dna.get("domain") or dna.get("domain_id") or variant.get("domain_id")),
            },
        )
        evaluation["evaluator"] = current_user.id
        evaluation["auto_promote"] = False
        # Never auto-promote
        if evaluation.get("promotion_decision") == "promote":
            evaluation["promotion_decision"] = "canary_only"
        # Wave 3: enrich fitness with ALC growth/reuse when agent_id present
        fitness = dict(evaluation.get("fitness_metrics") or {})
        agent_id = variant.get("agent_id")
        if agent_id:
            try:
                alc = self.improvement_metrics(current_user, agent_id=str(agent_id))
            except Exception:
                alc = {}
            from app.infrastructure.evolution.coevolution import enrich_fitness_with_alc

            fitness = enrich_fitness_with_alc(fitness, alc)
        else:
            from app.infrastructure.evolution.coevolution import composite_fitness

            fitness = {
                **fitness,
                **composite_fitness(float(fitness.get("suite_pass_rate") or 0.0), 0.0, 0.0),
            }
        evaluation["fitness_metrics"] = fitness
        variant["evaluation"] = evaluation
        variant["fitness_metrics"] = fitness
        variant["status"] = "sandbox_evaluated"
        variant["promotion_decision"] = evaluation["promotion_decision"]
        # Never write DNA into workflows collection here
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "evolution",
            "evolution.sandbox_evaluated",
            "evolution_variant",
            variant_id,
            {
                "result": evaluation.get("result"),
                "promotion_decision": evaluation.get("promotion_decision"),
                "fitness_metrics": evaluation.get("fitness_metrics"),
                "corpus_loaded": evaluation.get("corpus_loaded"),
                "checks": evaluation.get("checks"),
            },
            "success" if evaluation.get("result") == "passed" else "failed",
        )
        self.store.save()
        return deepcopy(variant)

    def promote_evolution_variant(self, current_user: AuthenticatedUser, variant_id: str, *, mode: str = "canary") -> dict[str, Any]:
        self.assert_permission(current_user, "workflows:update")
        if mode not in {"canary", "promote"}:
            raise ValidationError("mode must be canary or promote")
        variant = next((v for v in self._scoped_items("evolution_variants", current_user.organization_id) if v["id"] == variant_id), None)
        if not variant:
            raise NotFoundError(f"Evolution variant not found: {variant_id}")
        evaluation = variant.get("evaluation") or {}
        if evaluation.get("result") != "passed" or evaluation.get("promotion_decision") == "blocked":
            raise PermissionDeniedError("Cannot promote: sandbox evaluation did not pass")
        if variant.get("direct_production_mutation"):
            raise PermissionDeniedError("Cannot promote: direct production mutation flag set")
        # Auto-promote is always forbidden
        if mode == "promote" and evaluation.get("auto_promote") is True:
            raise PermissionDeniedError("Automatic promote is forbidden; use explicit canary then versioned promote")

        default_rollback = [
            "set_active_version_to_previous",
            "mark_variant_rolled_back",
            "notify_ops_owner",
            "open_incident_if_billing_affected",
        ]
        rollback_plan = variant.get("rollback_plan") or (variant.get("dna") or {}).get("rollback", {}).get("rollback_steps") or default_rollback

        # Canary: mark approved_for_canary without replacing production workflow id
        if mode == "canary":
            variant["status"] = "approved_for_canary"
            variant["promotion_decision"] = "canary_only"
            variant["rollback_plan"] = list(rollback_plan)
            variant["canary_approved_at"] = utc_now()
            self._append_audit(
                current_user.organization_id,
                current_user.id,
                "evolution",
                "evolution.canary_approved",
                "evolution_variant",
                variant_id,
                {"mode": "canary", "rollback_plan": variant["rollback_plan"]},
                "success",
            )
            self.store.save()
            return deepcopy(variant)

        # Full promote still creates a NEW workflow version entry rather than silent overwrite
        # of the live record's steps without versioning — and requires owner/admin
        if current_user.role not in {"owner", "admin"}:
            raise PermissionDeniedError("Full promote requires owner or admin")
        # Require canary approval first for versioned promote
        if variant.get("status") not in {"approved_for_canary", "promoted_canary", "sandbox_evaluated"}:
            raise PermissionDeniedError("Versioned promote requires passed evaluation (prefer canary first)")
        dna = deepcopy(variant.get("dna") or {})
        base_id = variant.get("base_workflow_id")
        if not base_id:
            raise ValidationError("promote requires base_workflow_id")
        base = next((w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == base_id), None)
        if not base:
            raise NotFoundError(f"Base workflow not found: {base_id}")
        previous_version = base.get("active_version") or base.get("version") or "1.0.0"
        # Versioned promotion: append version; do not delete prior DNA
        new_version = f"{base.get('version', '1.0.0')}-evo-{variant_id[-6:]}"
        base.setdefault("versions", []).append(
            {
                "version": new_version,
                "status": "canary",
                "created_at": utc_now(),
                "immutable": True,
                "steps": deepcopy(dna.get("steps") or base.get("steps") or []),
                "from_variant_id": variant_id,
                "previous_version": previous_version,
                "rollback_plan": list(rollback_plan),
            }
        )
        base["previous_active_version"] = previous_version
        base["active_version"] = new_version
        # Keep status active but mark canary promotion path — never silent overwrite of base id
        base["status"] = "active"
        variant["status"] = "promoted_canary"
        variant["promotion_decision"] = "canary_only"
        variant["sandbox_only"] = False
        variant["rollback_plan"] = list(rollback_plan)
        variant["promoted_version"] = new_version
        variant["previous_version"] = previous_version
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "evolution",
            "evolution.promoted_canary_version",
            "workflow",
            base_id,
            {
                "variant_id": variant_id,
                "version": new_version,
                "previous_version": previous_version,
                "rollback_plan": rollback_plan,
            },
            "success",
        )
        self.store.save()
        return deepcopy(variant)

    def rollback_evolution_variant(self, current_user: AuthenticatedUser, variant_id: str) -> dict[str, Any]:
        """Roll back a canary/versioned promotion; restore previous active version."""
        self.assert_permission(current_user, "workflows:update")
        if current_user.role not in {"owner", "admin", "manager"}:
            raise PermissionDeniedError("Rollback requires manager or higher")
        variant = next((v for v in self._scoped_items("evolution_variants", current_user.organization_id) if v["id"] == variant_id), None)
        if not variant:
            raise NotFoundError(f"Evolution variant not found: {variant_id}")
        if variant.get("status") not in {"approved_for_canary", "promoted_canary"}:
            raise ValidationError("Rollback only applies to canary-approved or promoted variants")
        base_id = variant.get("base_workflow_id")
        base = None
        restored_version = None
        if base_id:
            base = next((w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == base_id), None)
            if base and variant.get("status") == "promoted_canary":
                restored_version = (
                    variant.get("previous_version")
                    or base.get("previous_active_version")
                    or base.get("version")
                )
                if restored_version:
                    base["active_version"] = restored_version
                # Mark the canary version entry as rolled_back
                for entry in base.get("versions") or []:
                    if entry.get("from_variant_id") == variant_id:
                        entry["status"] = "rolled_back"
                        entry["rolled_back_at"] = utc_now()
        variant["status"] = "rolled_back"
        variant["rolled_back_at"] = utc_now()
        variant["rolled_back_by"] = current_user.id
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "evolution",
            "evolution.rolled_back",
            "evolution_variant",
            variant_id,
            {
                "base_workflow_id": base_id,
                "restored_version": restored_version,
                "rollback_plan": variant.get("rollback_plan") or [],
            },
            "success",
        )
        self.store.save()
        return deepcopy(variant)

    def list_evolution_variants(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "workflows:read")
        return deepcopy(self._scoped_items("evolution_variants", current_user.organization_id))

    # --- Self-improvement (Reflexion + lesson library + auto-propose) ---

    def _actor_as_user(self, actor_user_id: str, organization_id: str) -> AuthenticatedUser:
        user = next((u for u in self.store.collection("users") if u.get("id") == actor_user_id), None)
        if user:
            return AuthenticatedUser(
                id=user["id"],
                organization_id=user.get("organization_id") or organization_id,
                email=user.get("email") or "unknown@local",
                name=user.get("name") or "User",
                role=user.get("role") or "operator",
            )
        return AuthenticatedUser(
            id=actor_user_id,
            organization_id=organization_id,
            email="system@local",
            name="System",
            role="admin",
        )

    def _auto_reflect_if_enabled(self, run: dict[str, Any], actor_user_id: str) -> None:
        from app.core.config import settings as app_settings

        if not app_settings.auto_reflect:
            return
        if run.get("auto_reflected"):
            return
        if run.get("status") not in {"completed", "failed", "waiting_for_approval"}:
            return
        user = self._actor_as_user(actor_user_id, run.get("organization_id") or "org_default")
        self.reflect_on_workflow_run(user, run["id"])
        run["auto_reflected"] = True
        self.store.save()

    def reflect_on_workflow_run(self, current_user: AuthenticatedUser, run_id: str) -> dict[str, Any]:
        """Inter-episode reflection: lessons + optional DNA tweak suggestions."""
        self.assert_permission(current_user, "workflow_runs:read")
        run = next((r for r in self._scoped_items("workflow_runs", current_user.organization_id) if r["id"] == run_id), None)
        if not run:
            raise NotFoundError(f"Workflow run not found: {run_id}")
        workflow = next(
            (w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == run.get("workflow_id")),
            None,
        )
        from app.core.config import settings as app_settings
        from app.infrastructure.self_improvement.lessons import Lesson, LessonLibrary
        from app.infrastructure.self_improvement.llm_critic import llm_critique_run
        from app.infrastructure.self_improvement.reflection import reflect_on_run

        llm_overlay = llm_critique_run(run, workflow, app_settings)
        reflection = reflect_on_run(run, workflow, llm_overlay=llm_overlay)
        org_lessons = [
            i
            for i in self.store.collection("improvement_lessons")
            if i.get("organization_id") == current_user.organization_id
        ]
        library = LessonLibrary(org_lessons)
        stored: list[dict[str, Any]] = []
        # Map step-level agents for multi-agent lesson tagging (ALC)
        step_agents: list[str | None] = []
        for step in run.get("steps") or []:
            step_agents.append(step.get("agent_id") or step.get("agent"))
        if not step_agents and workflow:
            for sdef in workflow.get("steps") or []:
                step_agents.append(sdef.get("agent"))
        unique_agents = [a for a in dict.fromkeys(step_agents) if a]

        def _store_lesson(text: str, agent_id: str | None) -> None:
            twin = next(
                (
                    i
                    for i in self.store.collection("improvement_lessons")
                    if i.get("text") == text
                    and i.get("workflow_id") == run.get("workflow_id")
                    and i.get("organization_id") == current_user.organization_id
                    and (i.get("agent_id") or None) == (agent_id or None)
                ),
                None,
            )
            if twin:
                stored.append(twin)
                return
            lesson = Lesson(
                id=f"lesson_{uuid.uuid4().hex[:10]}",
                text=text,
                source_run_id=run_id,
                workflow_id=run.get("workflow_id"),
                agent_id=agent_id,
                tags=["reflection", reflection.get("status") or "unknown"]
                + ([f"agent:{agent_id}"] if agent_id else []),
                provenance={
                    "source_refs": [run_id, run.get("workflow_id") or "workflow"]
                    + ([agent_id] if agent_id else []),
                    "captured_by": current_user.id,
                    "recorded_at": utc_now(),
                    "framework": "self_evolving_agents_reflexion",
                    "agent_id": agent_id,
                },
            )
            library.add(lesson)
            payload = lesson.to_dict()
            payload["organization_id"] = current_user.organization_id
            self.store.collection("improvement_lessons").append(payload)
            stored.append(payload)
            mem_agent = None
            if agent_id:
                mem_agent = next(
                    (
                        a
                        for a in self._scoped_items("agents", current_user.organization_id)
                        if a.get("id") == agent_id
                    ),
                    {"id": agent_id, "allowed_memory_scopes": ["agent", "organization", "organization_memory"]},
                )
            try:
                self._write_memory(
                    current_user.organization_id,
                    current_user.id,
                    "organization_memory",
                    f"Lesson from {run_id}" + (f" agent={agent_id}" if agent_id else ""),
                    text,
                    {
                        "source_refs": [run_id],
                        "captured_by": current_user.id,
                        "recorded_at": utc_now(),
                        "agent_id": agent_id,
                    },
                    agent=None,
                )
            except Exception:  # noqa: BLE001
                pass
            # Agent-scoped episode when ALC scopes allow
            if agent_id and mem_agent:
                try:
                    scopes = set(mem_agent.get("allowed_memory_scopes") or [])
                    if "agent" in scopes or "agent_memory" in scopes:
                        self.store.collection("agent_episodes").append(
                            {
                                "id": f"ep_{uuid.uuid4().hex[:10]}",
                                "organization_id": current_user.organization_id,
                                "agent_id": agent_id,
                                "run_id": run_id,
                                "text": text,
                                "created_at": utc_now(),
                            }
                        )
                except Exception:  # noqa: BLE001
                    pass

        for text in reflection.get("lessons") or []:
            if unique_agents:
                # Attribute generic lessons to each step agent for multi-agent runs
                for aid in unique_agents:
                    _store_lesson(text, aid)
            else:
                _store_lesson(text, None)

        # Persist lessons learned under business path when possible
        try:
            lessons_dir = self.repo_root / "business" / "evolution" / "lessons-learned"
            lessons_dir.mkdir(parents=True, exist_ok=True)
            path = lessons_dir / f"{run_id}.json"
            path.write_text(
                json.dumps({"reflection": reflection, "lessons": stored}, indent=2) + "\n",
                encoding="utf-8",
            )
            reflection["artifact_path"] = str(path.as_posix())
        except OSError:
            pass

        reflection["stored_lessons"] = stored
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "improvement",
            "improvement.reflected",
            "workflow_run",
            run_id,
            {"lesson_count": len(stored), "satisfactory": reflection.get("is_satisfactory")},
            "success",
        )
        self.store.save()
        return reflection

    def list_improvement_lessons(
        self,
        current_user: AuthenticatedUser,
        *,
        workflow_id: str | None = None,
        agent_id: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "memory:read")
        from app.infrastructure.self_improvement.lessons import LessonLibrary

        items = [
            i
            for i in self._scoped_items("improvement_lessons", current_user.organization_id)
            if (not workflow_id or i.get("workflow_id") == workflow_id)
            and (not agent_id or i.get("agent_id") == agent_id)
        ]
        library = LessonLibrary(items)
        # Return ranked by utility without double-counting uses for list view
        ranked = sorted(library.lessons, key=lambda l: l.utility, reverse=True)[:limit]
        return [l.to_dict() for l in ranked]

    def improvement_metrics(
        self,
        current_user: AuthenticatedUser,
        *,
        agent_id: str | None = None,
    ) -> dict[str, Any]:
        """ALC growth/reuse metrics (Wave 1)."""
        self.assert_permission(current_user, "memory:read")
        lessons = self.list_improvement_lessons(current_user, agent_id=agent_id, limit=200)
        total_uses = sum(int(l.get("uses") or 0) for l in lessons)
        total_wins = sum(int(l.get("wins") or 0) for l in lessons)
        growth = len(lessons)
        reuse = (total_uses / growth) if growth else 0.0
        episodes = [
            e
            for e in self.store.collection("agent_episodes")
            if e.get("organization_id") == current_user.organization_id
            and (not agent_id or e.get("agent_id") == agent_id)
        ]
        return {
            "agent_id": agent_id,
            "knowledge_growth_count": growth,
            "lesson_reuse_rate": round(reuse, 4),
            "lesson_win_rate": round((total_wins + 1) / (total_uses + 2), 4) if growth else 0.0,
            "episode_count": len(episodes),
        }

    def reflect_on_agent(
        self,
        current_user: AuthenticatedUser,
        agent_id: str,
        *,
        run_id: str | None = None,
    ) -> dict[str, Any]:
        """Reflect and return lessons filtered to a single agent."""
        self.assert_permission(current_user, "workflow_runs:read")
        if run_id:
            result = self.reflect_on_workflow_run(current_user, run_id)
            stored = [l for l in (result.get("stored_lessons") or []) if l.get("agent_id") == agent_id]
            result["stored_lessons"] = stored
            result["agent_id"] = agent_id
            return result
        lessons = self.list_improvement_lessons(current_user, agent_id=agent_id, limit=50)
        return {"agent_id": agent_id, "stored_lessons": lessons, "status": "listed"}

    def list_agent_episodes(
        self,
        current_user: AuthenticatedUser,
        *,
        agent_id: str,
    ) -> list[dict[str, Any]]:
        """Return agent-scoped episodes only for the requested agent (isolation)."""
        self.assert_permission(current_user, "memory:read")
        return deepcopy(
            [
                e
                for e in self.store.collection("agent_episodes")
                if e.get("organization_id") == current_user.organization_id and e.get("agent_id") == agent_id
            ]
        )

    def register_domain_pack(
        self,
        current_user: AuthenticatedUser,
        *,
        manifest: dict[str, Any] | None = None,
        manifest_path: str | None = None,
    ) -> dict[str, Any]:
        """Validate domain manifest and load agents as draft/registered (Wave 1)."""
        self.assert_permission(current_user, "agents:create")
        import sys

        sys_path = self.repo_root / "scripts" / "business"
        if str(sys_path) not in sys.path:
            sys.path.insert(0, str(sys_path))
        from schema_validate import SchemaError, validate  # type: ignore

        if manifest is None:
            if not manifest_path:
                raise ValidationError("manifest or manifest_path required")
            path = self.repo_root / manifest_path
            if not path.is_file():
                raise NotFoundError(f"Manifest not found: {manifest_path}")
            manifest = json.loads(path.read_text(encoding="utf-8"))
        schema_path = self.repo_root / "business" / "schemas" / "domain-manifest.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        try:
            validate(manifest, schema)
        except SchemaError as exc:
            raise ValidationError(f"Invalid domain manifest: {exc}") from exc

        domain_id = manifest["domain_id"]
        agent_ids_raw = manifest.get("agents") or []
        pack_ids: list[str] = []
        for item in agent_ids_raw:
            if isinstance(item, str):
                pack_ids.append(item)
            elif isinstance(item, dict) and item.get("id"):
                pack_ids.append(str(item["id"]))

        loaded: list[dict[str, Any]] = []
        for pack_id in pack_ids:
            # Prefer disk agent_spec under business/<domain>/agents/<pack_id>/
            disk_spec = (
                self.repo_root
                / "business"
                / domain_id
                / "agents"
                / pack_id
                / "agent_spec.json"
            )
            if disk_spec.is_file():
                spec = json.loads(disk_spec.read_text(encoding="utf-8"))
            else:
                spec = {
                    "id": pack_id,
                    "domain_id": domain_id,
                    "name": pack_id,
                    "status": "draft",
                    "requires_alc": bool(manifest.get("requires_alc", True)),
                    "allowed_memory_scopes": ["agent", "organization"],
                    "alc_version": "1.0",
                    "hooks": {"reflect": True},
                    "tools": [],
                }
            existing = next(
                (
                    a
                    for a in self._scoped_items("agents", current_user.organization_id)
                    if a.get("id") == pack_id
                ),
                None,
            )
            record = {
                "id": pack_id,
                "organization_id": current_user.organization_id,
                "name": spec.get("name") or pack_id,
                "role": spec.get("role") or spec.get("name") or pack_id,
                "status": "registered" if existing and existing.get("status") == "active" else "draft",
                "domain_id": domain_id,
                "requires_alc": bool(spec.get("requires_alc", manifest.get("requires_alc", True))),
                "allowed_memory_scopes": list(spec.get("allowed_memory_scopes") or ["agent"]),
                "alc_version": spec.get("alc_version") or "1.0",
                "hooks": dict(spec.get("hooks") or {"reflect": True}),
                "allowed_tools": list(spec.get("tools") or spec.get("allowed_tools") or []),
                "risk_tier": spec.get("risk_tier") or manifest.get("default_risk_tier") or "tier_2_draft",
                "knowledgeAccess": "pack",
                "provenance": dict(spec.get("provenance") or {}),
            }
            # Keep active if already active and ALC still ok
            if existing:
                if existing.get("status") == "active":
                    record["status"] = "active"
                existing.update({k: v for k, v in record.items() if k != "status" or existing.get("status") != "active"})
                if existing.get("status") != "active":
                    existing["status"] = record["status"]
                loaded.append(deepcopy(existing))
            else:
                self.store.collection("agents").append(record)
                loaded.append(deepcopy(record))

        pack_entry = {
            "domain_id": domain_id,
            "version": manifest.get("version"),
            "organization_id": current_user.organization_id,
            "requires_alc": bool(manifest.get("requires_alc")),
            "agent_ids": pack_ids,
            "registered_at": utc_now(),
            "display_name": manifest.get("display_name"),
        }
        packs = self.store.collection("domain_packs")
        packs[:] = [
            p
            for p in packs
            if not (
                p.get("domain_id") == domain_id
                and p.get("organization_id") == current_user.organization_id
            )
        ]
        packs.append(pack_entry)
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "domain",
            "domain.registered",
            "domain_pack",
            domain_id,
            {"agent_count": len(loaded)},
            "success",
        )
        self.store.save()
        return {
            "status": "draft",
            "domain_id": domain_id,
            "agents_loaded": len(loaded),
            "agents": loaded,
            "requires_alc": pack_entry["requires_alc"],
        }

    def list_domain_packs(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "agents:read")
        return deepcopy(
            [
                p
                for p in self.store.collection("domain_packs")
                if p.get("organization_id") == current_user.organization_id
            ]
        )

    def list_video_archetypes(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        """Return archetype A–J registry for UI / planner selection."""
        self.assert_permission(current_user, "agents:read")
        from app.domain.workflows.archetype_selector import load_registry

        reg = load_registry(repo_root=self.repo_root)
        return {
            "domain_id": reg.get("domain_id") or "video",
            "entry_agents": reg.get("entry_agents") or [],
            "selection_policy": reg.get("selection_policy") or {},
            "scale_profiles": reg.get("scale_profiles") or {},
            "archetypes": [
                {
                    "code": a.get("code"),
                    "name": a.get("name"),
                    "process_id": a.get("process_id"),
                    "dna_id": a.get("dna_id"),
                    "default_scale": a.get("default_scale"),
                    "allowed_scales": a.get("allowed_scales"),
                    "duration_sec_hint": a.get("duration_sec_hint"),
                    "depth": a.get("depth"),
                    "keywords": a.get("keywords"),
                }
                for a in (reg.get("archetypes") or [])
                if isinstance(a, dict)
            ],
            "registry_path": "business/video/archetype_registry.json",
        }

    def recommend_video_workflow(
        self,
        current_user: AuthenticatedUser,
        *,
        brief: str,
        duration_sec: int | None = None,
        top_k: int = 3,
        budget_hint: str | None = None,
        channel_hint: str | None = None,
    ) -> dict[str, Any]:
        """Score brief against archetype registry; recommend DNA id + scale."""
        self.assert_permission(current_user, "workflows:read")
        from app.domain.workflows.archetype_selector import recommend_workflow

        try:
            dur = int(duration_sec) if duration_sec is not None and str(duration_sec) != "" else None
        except (TypeError, ValueError) as exc:
            raise ValidationError("duration_sec must be an integer") from exc
        try:
            result = recommend_workflow(
                brief,
                duration_sec=dur,
                top_k=top_k,
                repo_root=self.repo_root,
                budget_hint=str(budget_hint) if budget_hint else None,
                channel_hint=str(channel_hint) if channel_hint else None,
            )
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        except FileNotFoundError as exc:
            raise ValidationError(str(exc)) from exc
        return result

    def video_n3_roster_status(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        """N3 completeness snapshot for the video pack (Wave 5). Reads pack disk artifacts."""
        self.assert_permission(current_user, "agents:read")
        video = self.repo_root / "business" / "video"
        roster_path = video / "ROSTER.json"
        standby_path = video / "standby_pool.json"
        coverage_path = video / "process_coverage.json"
        wf_dir = video / "workflows"
        registry_path = video / "archetype_registry.json"

        roster = json.loads(roster_path.read_text(encoding="utf-8")) if roster_path.is_file() else []
        pack_ids = [r.get("pack_id") for r in roster if isinstance(r, dict) and r.get("pack_id")]
        standby = {}
        if standby_path.is_file():
            standby = json.loads(standby_path.read_text(encoding="utf-8"))
        s_agents = standby.get("agents") if isinstance(standby, dict) else []
        s_ids = {a.get("pack_id") for a in (s_agents or []) if isinstance(a, dict)}
        orphans_missing_standby = sorted(set(pack_ids) - s_ids)
        orphans_extra_standby = sorted(s_ids - set(pack_ids))

        by_category: dict[str, int] = {}
        registered = 0
        for row in roster:
            if not isinstance(row, dict):
                continue
            cat = row.get("category") or "unknown"
            by_category[cat] = by_category.get(cat, 0) + 1
            pid = row.get("pack_id")
            if not pid:
                continue
            spec_path = video / "agents" / pid / "agent_spec.json"
            if spec_path.is_file():
                try:
                    spec = json.loads(spec_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    continue
                if (spec.get("status") or "").lower() in {"registered", "active"}:
                    registered += 1

        dna_files = sorted(p.name for p in wf_dir.glob("*.dna.json")) if wf_dir.is_dir() else []
        coverage = {"total": 0, "dna": 0, "pack_linked": 0, "va_only": 0}
        if coverage_path.is_file():
            cov = json.loads(coverage_path.read_text(encoding="utf-8"))
            procs = cov.get("processes") or []
            coverage["total"] = len(procs)
            for p in procs:
                rep = p.get("representation")
                if rep == "dna":
                    coverage["dna"] += 1
                elif rep == "pack_doc":
                    coverage["pack_linked"] += 1
                else:
                    coverage["va_only"] += 1
            if cov.get("va_only_count"):
                coverage["va_only"] = max(coverage["va_only"], int(cov.get("va_only_count") or 0))

        n3_complete = (
            len(pack_ids) == 114
            and len(s_ids) == 114
            and not orphans_missing_standby
            and not orphans_extra_standby
            and registered == 114
            and coverage["va_only"] == 0
            and coverage["total"] > 0
            and len(dna_files) >= 14
            and (video / "policies" / "roster-retention.md").is_file()
            and (video / "router_table.json").is_file()
        )
        return {
            "domain_id": "video",
            "roster_count": len(pack_ids),
            "standby_count": len(s_ids),
            "registered_or_active": registered,
            "by_category": by_category,
            "orphans": orphans_missing_standby + orphans_extra_standby,
            "dna_workflows": [n.replace(".dna.json", "") for n in dna_files],
            "dna_count": len(dna_files),
            "process_coverage": coverage,
            "entry": (standby.get("entry") if isinstance(standby, dict) else None) or "video.orchestrator",
            "retention_policy": "business/video/policies/roster-retention.md",
            "archetype_registry": registry_path.is_file(),
            "archetype_registry_path": "business/video/archetype_registry.json",
            "n3_complete": n3_complete,
        }

    def auto_propose_from_failures(
        self,
        current_user: AuthenticatedUser,
        *,
        workflow_id: str,
        run_id: str | None = None,
    ) -> dict[str, Any]:
        """Propose sandbox DNA variant from reflection (never mutates production)."""
        self.assert_permission(current_user, "workflows:create")
        base = next((w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == workflow_id), None)
        if not base:
            raise NotFoundError(f"Workflow not found: {workflow_id}")
        # Reflect latest failed run if not specified
        if not run_id:
            runs = [
                r
                for r in self._scoped_items("workflow_runs", current_user.organization_id)
                if r.get("workflow_id") == workflow_id and r.get("status") in {"failed", "waiting_for_approval"}
            ]
            runs.sort(key=lambda r: r.get("updated_at") or r.get("created_at") or "", reverse=True)
            if not runs:
                raise ValidationError("No failed/waiting runs found to learn from")
            run_id = runs[0]["id"]
        reflection = self.reflect_on_workflow_run(current_user, run_id)
        changes = reflection.get("suggested_changes") or []
        dna = deepcopy(base)
        dna["production_ready"] = False
        dna["status"] = "sandbox"
        # Apply safe structural tweaks only
        for change in changes:
            if change.get("type") == "evaluation_policy":
                dna.setdefault("evaluation_policy", {})
                dna["evaluation_policy"]["block_on_fail"] = True
                dna["evaluation_policy"]["auto_promote"] = False
            if change.get("type") == "human_gate_ops":
                for step in dna.get("steps") or []:
                    if step.get("id") == change.get("step_id") or step.get("irreversible"):
                        step["human_gate_required"] = True
        variant = self.propose_evolution_variant(
            current_user,
            {
                "base_workflow_id": workflow_id,
                "name": f"Auto-proposed from {run_id}",
                "changes": [c.get("description") or c.get("type") for c in changes] or ["reflection_no_structural_change"],
                "dna": {
                    "id": workflow_id,
                    "name": dna.get("name"),
                    "risk_tier": dna.get("risk_tier"),
                    "steps": dna.get("steps") or [],
                    "rollback": dna.get("rollback") or {"reversible": True, "rollback_steps": ["notify_ops_owner"]},
                    "evaluation_policy": dna.get("evaluation_policy") or {"block_on_fail": True, "auto_promote": False},
                    "production_ready": False,
                    "auto_promote": False,
                },
                "rollback_plan": (dna.get("rollback") or {}).get("rollback_steps") or ["notify_ops_owner"],
            },
        )
        variant["reflection"] = {
            "run_id": run_id,
            "lesson_count": len(reflection.get("lessons") or []),
            "suggested_changes": changes,
        }
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "improvement",
            "improvement.auto_proposed",
            "evolution_variant",
            variant["id"],
            {"from_run": run_id, "workflow_id": workflow_id},
            "success",
        )
        self.store.save()
        return deepcopy(variant)

    # --- Loop Engineering runner ---

    def start_improvement_loop(
        self,
        current_user: AuthenticatedUser,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Run prompt→observe→verify→iterate around a workflow (sandbox-safe)."""
        self.assert_permission(current_user, "workflows:execute")
        from app.infrastructure.loop_engineering.loop_dna import DEFAULT_LOOP_DNA, validate_loop_dna
        from app.infrastructure.loop_engineering.runner import evaluate_stop

        loop_dna = deepcopy(payload.get("loop_dna") or DEFAULT_LOOP_DNA)
        errors = validate_loop_dna(loop_dna)
        if errors:
            raise ValidationError(f"Invalid loop DNA: {', '.join(errors)}")
        workflow_id = payload.get("workflow_id") or (loop_dna.get("generator") or {}).get("workflow_id")
        if not workflow_id:
            raise ValidationError("workflow_id required")
        stopping = loop_dna.get("stopping") or {}
        max_iterations = int(stopping.get("max_iterations") or 3)
        fail_budget = int(stopping.get("fail_budget") or 2)
        success_statuses = list(stopping.get("success_statuses") or ["completed"])

        loop_run = {
            "id": f"loop_{uuid.uuid4().hex[:12]}",
            "organization_id": current_user.organization_id,
            "workflow_id": workflow_id,
            "status": "running",
            "loop_dna": loop_dna,
            "iterations": [],
            "created_by": current_user.id,
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        fail_count = 0
        last_status = None
        input_payload = payload.get("input_payload") or {"case_id": f"loop_case_{uuid.uuid4().hex[:8]}", "triggered_from": "improvement_loop"}

        for iteration in range(1, max_iterations + 1):
            # prompt: start or continue via new run (isolation = new run id)
            try:
                run = self.start_workflow_run(workflow_id, current_user, {**input_payload, "loop_run_id": loop_run["id"], "loop_iteration": iteration})
                self.dispatch_queued_runs(current_user)
                run = self.get_run(current_user, run["id"])
                # Auto-approve only if payload allows AND role is admin/owner (still audited)
                safety = 0
                while run.get("status") == "waiting_for_approval" and payload.get("auto_approve_gates") and current_user.role in {"owner", "admin"} and safety < 5:
                    if run.get("approval_request_id"):
                        self.decide_approval(run["approval_request_id"], "approved", f"loop {loop_run['id']} iter {iteration}", current_user)
                    run = self.get_run(current_user, run["id"])
                    safety += 1
            except Exception as exc:  # noqa: BLE001
                last_status = "failed"
                fail_count += 1
                loop_run["iterations"].append(
                    {
                        "iteration": iteration,
                        "status": "failed",
                        "error": str(exc),
                        "phase": "prompt_observe",
                    }
                )
                decision = evaluate_stop(
                    iteration=iteration,
                    max_iterations=max_iterations,
                    fail_count=fail_count,
                    fail_budget=fail_budget,
                    last_run_status=last_status,
                    success_statuses=success_statuses,
                )
                loop_run["iterations"][-1]["decision"] = decision.action
                loop_run["iterations"][-1]["decision_reason"] = decision.reason
                if decision.action != "continue":
                    loop_run["status"] = decision.action
                    break
                continue

            last_status = run.get("status")
            # verify: reflect
            reflection = self.reflect_on_workflow_run(current_user, run["id"])
            if last_status == "failed":
                fail_count += 1
            decision = evaluate_stop(
                iteration=iteration,
                max_iterations=max_iterations,
                fail_count=fail_count,
                fail_budget=fail_budget,
                last_run_status=last_status,
                success_statuses=success_statuses,
            )
            loop_run["iterations"].append(
                {
                    "iteration": iteration,
                    "run_id": run["id"],
                    "status": last_status,
                    "reflection_satisfactory": reflection.get("is_satisfactory"),
                    "lessons": reflection.get("lessons") or [],
                    "decision": decision.action,
                    "decision_reason": decision.reason,
                    "phase": "verify_iterate",
                }
            )
            if decision.action != "continue":
                loop_run["status"] = decision.action
                break
        else:
            loop_run["status"] = "stop_escalate"
            loop_run["stop_reason"] = "max_iterations"

        # Optional: auto-propose DNA if loop failed and requested
        if payload.get("auto_propose_on_fail") and loop_run["status"] in {"stop_fail", "stop_escalate"}:
            try:
                last_run_id = next(
                    (i.get("run_id") for i in reversed(loop_run["iterations"]) if i.get("run_id")),
                    None,
                )
                if last_run_id:
                    variant = self.auto_propose_from_failures(current_user, workflow_id=workflow_id, run_id=last_run_id)
                    loop_run["proposed_variant_id"] = variant.get("id")
            except Exception as exc:  # noqa: BLE001
                loop_run["propose_error"] = str(exc)

        loop_run["updated_at"] = utc_now()
        loop_run["final_status"] = last_status
        self.store.collection("loop_runs").append(loop_run)
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "loop",
            "loop.completed",
            "loop_run",
            loop_run["id"],
            {"status": loop_run["status"], "iterations": len(loop_run["iterations"])},
            "success",
        )
        self.store.save()
        return deepcopy(loop_run)

    def get_loop_run(self, current_user: AuthenticatedUser, loop_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "workflow_runs:read")
        item = next((l for l in self._scoped_items("loop_runs", current_user.organization_id) if l["id"] == loop_id), None)
        if not item:
            raise NotFoundError(f"Loop run not found: {loop_id}")
        return deepcopy(item)

    def list_loop_runs(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "workflow_runs:read")
        return deepcopy(self._scoped_items("loop_runs", current_user.organization_id))

    # --- Knowledge orchestration (Agents-K1 lite) ---

    def _merge_knowledge_graph(self, organization_id: str, graph: dict[str, Any]) -> None:
        for node in graph.get("nodes") or []:
            node = dict(node)
            node["organization_id"] = organization_id
            existing = next(
                (
                    n
                    for n in self.store.collection("knowledge_nodes")
                    if n.get("id") == node.get("id") and n.get("organization_id") == organization_id
                ),
                None,
            )
            if existing:
                existing.update(node)
            else:
                self.store.collection("knowledge_nodes").append(node)
        for edge in graph.get("edges") or []:
            edge = dict(edge)
            edge["organization_id"] = organization_id
            existing = next(
                (
                    e
                    for e in self.store.collection("knowledge_edges")
                    if e.get("id") == edge.get("id") and e.get("organization_id") == organization_id
                ),
                None,
            )
            if existing:
                existing.update(edge)
            else:
                self.store.collection("knowledge_edges").append(edge)

    def extract_knowledge_graph(self, current_user: AuthenticatedUser, document_id: str) -> dict[str, Any]:
        self.assert_permission(current_user, "knowledge:write")
        document = next(
            (d for d in self._scoped_items("knowledge_documents", current_user.organization_id) if d["id"] == document_id),
            None,
        )
        if not document:
            raise NotFoundError(f"Knowledge document not found: {document_id}")
        from app.infrastructure.knowledge_orchestration.extract import extract_document_graph

        graph = extract_document_graph(document)
        self._merge_knowledge_graph(current_user.organization_id, graph)
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "knowledge",
            "knowledge.graph_extracted",
            "knowledge",
            document_id,
            {"nodes": len(graph.get("nodes") or []), "edges": len(graph.get("edges") or [])},
            "success",
        )
        self.store.save()
        return graph

    def query_knowledge_graph(
        self,
        current_user: AuthenticatedUser,
        *,
        seed: str,
        max_hops: int = 2,
    ) -> dict[str, Any]:
        self.assert_permission(current_user, "knowledge:read")
        from app.infrastructure.knowledge_orchestration.operators import lineage, resolve_seed

        nodes = self._scoped_items("knowledge_nodes", current_user.organization_id)
        edges = self._scoped_items("knowledge_edges", current_user.organization_id)
        seeds = resolve_seed(nodes, seed)
        if not seeds:
            return {"seed": seed, "matches": [], "lineage": [], "provenance_policy": "stable_ids_required"}
        primary = seeds[0]
        path = lineage(nodes, edges, primary["id"], max_hops=max_hops)
        return {
            "seed": seed,
            "matches": seeds[:5],
            "lineage": path,
            "operator": "O1+O2",
            "schema": "agents_k1_lite_v1",
        }

    def knowledge_graph_gaps(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        self.assert_permission(current_user, "knowledge:read")
        from app.infrastructure.knowledge_orchestration.operators import detect_gaps

        nodes = self._scoped_items("knowledge_nodes", current_user.organization_id)
        edges = self._scoped_items("knowledge_edges", current_user.organization_id)
        gaps = detect_gaps(nodes, edges)
        return {
            "gap_count": len(gaps),
            "gaps": gaps[:50],
            "node_count": len(nodes),
            "edge_count": len(edges),
            "operator": "O5",
        }

    def federate_knowledge_graph(self, current_user: AuthenticatedUser, *, push_neo4j: bool = False) -> dict[str, Any]:
        """Export graph to Cypher/JSON; optional Neo4j bolt push."""
        self.assert_permission(current_user, "knowledge:write")
        from app.core.config import settings as app_settings
        from app.infrastructure.knowledge_orchestration.federation import try_push_neo4j, write_federation_artifacts

        nodes = self._scoped_items("knowledge_nodes", current_user.organization_id)
        edges = self._scoped_items("knowledge_edges", current_user.organization_id)
        artifacts = write_federation_artifacts(
            self.repo_root,
            organization_id=current_user.organization_id,
            nodes=nodes,
            edges=edges,
        )
        neo = try_push_neo4j(nodes, edges, app_settings) if push_neo4j else {"pushed": False, "reason": "push_not_requested"}
        result = {**artifacts, "neo4j": neo, "format": "graphanything_compatible"}
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "knowledge",
            "knowledge.federated",
            "knowledge_graph",
            "export",
            {"nodes": len(nodes), "edges": len(edges), "neo4j": neo.get("pushed")},
            "success",
        )
        self.store.save()
        return result

    def evolution_archive(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        """Population / archive view of evolution variants (DGM-style)."""
        self.assert_permission(current_user, "workflows:read")
        variants = self._scoped_items("evolution_variants", current_user.organization_id)
        scored = []
        for v in variants:
            fitness = v.get("fitness_metrics") or (v.get("evaluation") or {}).get("fitness_metrics") or {}
            suite_pass = float(fitness.get("suite_pass_rate") or (1.0 if (v.get("evaluation") or {}).get("result") == "passed" else 0.0))
            scored.append(
                {
                    "id": v.get("id"),
                    "name": v.get("name"),
                    "base_workflow_id": v.get("base_workflow_id"),
                    "status": v.get("status"),
                    "sandbox_only": v.get("sandbox_only"),
                    "fitness": suite_pass,
                    "fitness_metrics": fitness,
                    "promotion_decision": v.get("promotion_decision"),
                    "created_at": v.get("created_at"),
                    "lineage": v.get("lineage") or [v.get("base_workflow_id")],
                    "evaluation_result": (v.get("evaluation") or {}).get("result"),
                }
            )
        scored.sort(key=lambda item: (item.get("fitness") or 0, item.get("created_at") or ""), reverse=True)
        elite = scored[0] if scored else None
        return {
            "archive_size": len(scored),
            "elite": elite,
            "variants": scored,
            "selection_policy": "fitness_desc_with_sandbox_only_default",
            "framework": "dgm_population_archive_lite",
        }

    def propose_skill_sandbox(
        self,
        current_user: AuthenticatedUser,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Propose skill/prompt patch into sandbox path only."""
        self.assert_permission(current_user, "workflows:create")
        from app.infrastructure.self_improvement.skill_sandbox import propose_skill_patch, write_skill_sandbox

        skill_name = payload.get("skill_name") or "improved-skill"
        content = payload.get("content") or ""
        if len(content) < 20:
            raise ValidationError("Skill content too short")
        proposal = propose_skill_patch(
            skill_name=skill_name,
            content=content,
            rationale=payload.get("rationale") or "auto skill improvement",
            source_run_id=payload.get("source_run_id"),
            organization_id=current_user.organization_id,
            actor_id=current_user.id,
        )
        if payload.get("domain") or payload.get("domain_id"):
            proposal["domain"] = payload.get("domain") or payload.get("domain_id")
        if payload.get("agent_id"):
            proposal["agent_id"] = payload.get("agent_id")
        path = write_skill_sandbox(self.repo_root, proposal)
        proposal["written_path"] = path
        self.store.state.setdefault("skill_proposals", [])
        self.store.collection("skill_proposals").append(proposal)
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "improvement",
            "skill.sandbox_proposed",
            "skill_proposal",
            proposal["id"],
            {"sandbox_path": path, "skill_name": skill_name, "domain": proposal.get("domain")},
            "success",
        )
        self.store.save()
        return deepcopy(proposal)

    def promote_skill_sandbox(self, current_user: AuthenticatedUser, proposal_id: str) -> dict[str, Any]:
        """Explicit promote of sandboxed skill to production path (admin/owner)."""
        self.assert_permission(current_user, "workflows:update")
        if current_user.role not in {"owner", "admin"}:
            raise PermissionDeniedError("Skill promote requires owner or admin")
        from app.infrastructure.self_improvement.skill_sandbox import promote_skill_to_production

        proposal = next(
            (
                p
                for p in self.store.collection("skill_proposals")
                if p.get("id") == proposal_id and p.get("organization_id") == current_user.organization_id
            ),
            None,
        )
        if not proposal:
            raise NotFoundError(f"Skill proposal not found: {proposal_id}")
        prod_path = promote_skill_to_production(self.repo_root, proposal)
        proposal["status"] = "promoted"
        proposal["sandbox_only"] = False
        proposal["promoted_path"] = prod_path
        proposal["promoted_at"] = utc_now()
        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "improvement",
            "skill.promoted",
            "skill_proposal",
            proposal_id,
            {"production_path": prod_path},
            "success",
        )
        self.store.save()
        return deepcopy(proposal)

    def list_skill_proposals(self, current_user: AuthenticatedUser) -> list[dict[str, Any]]:
        self.assert_permission(current_user, "workflows:read")
        self.store.state.setdefault("skill_proposals", [])
        return deepcopy(
            [p for p in self.store.collection("skill_proposals") if p.get("organization_id") == current_user.organization_id]
        )

    # --- Wave 3: coevolution, lesson utility, governance review ---

    def run_coevolution_experiment(
        self,
        current_user: AuthenticatedUser,
        *,
        generations: int = 2,
        domain_id: str = "video",
        agent_ids: list[str] | None = None,
        base_workflow_id: str = "wf_video_arch_a_viral_hook_v1",
    ) -> dict[str, Any]:
        """Multi-generation sandbox coevolution (planner × aesthetics genomes). Never auto-promotes."""
        self.assert_permission(current_user, "workflows:create")
        from app.infrastructure.evolution.coevolution import (
            build_genome_propose_payload,
            default_agent_pair,
            load_pack_workflow_dna,
            select_elite,
            summarize_generation,
        )

        gens = max(2, int(generations or 2))
        domain = (domain_id or "video").strip() or "video"
        if agent_ids and len(agent_ids) >= 2:
            planner_id, aesthetics_id = agent_ids[0], agent_ids[1]
        else:
            planner_id, aesthetics_id = default_agent_pair(domain)

        base = next(
            (w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == base_workflow_id),
            None,
        )
        production_version = base.get("version") if base else None
        dna = deepcopy(base) if base else load_pack_workflow_dna(self.repo_root, domain, base_workflow_id)
        if not dna:
            dna = {
                "id": base_workflow_id,
                "domain": domain,
                "production_ready": False,
                "auto_promote": False,
                "steps": [],
                "risk_tier": "tier_3_execute_reversible",
            }
        dna = deepcopy(dna)
        dna["domain"] = dna.get("domain") or domain
        dna["production_ready"] = False
        dna["auto_promote"] = False

        # Only pass base_workflow_id into propose when present in production store
        propose_base_id = base_workflow_id if base else None

        parent_genomes: dict[str, dict[str, Any] | None] = {planner_id: None, aesthetics_id: None}
        parent_variant_ids: dict[str, str | None] = {planner_id: None, aesthetics_id: None}
        generation_summaries: list[dict[str, Any]] = []
        all_variant_ids: list[str] = []

        for g in range(1, gens + 1):
            gen_variants: list[dict[str, Any]] = []
            for agent_id, role in ((planner_id, "planner"), (aesthetics_id, "aesthetics")):
                payload = build_genome_propose_payload(
                    agent_id=agent_id,
                    generation=g,
                    parent_genome=parent_genomes.get(agent_id),
                    base_workflow_id=propose_base_id,
                    dna=dna,
                    role=role,
                    parent_variant_id=parent_variant_ids.get(agent_id),
                )
                variant = self.propose_evolution_variant(current_user, payload)
                evaluated = self.sandbox_evaluate_variant(current_user, variant["id"])
                gen_variants.append(evaluated)
                all_variant_ids.append(evaluated["id"])
            summary = summarize_generation(g, gen_variants)
            generation_summaries.append(summary)
            # Seed next gen from each role's best-of-generation for that agent, else overall elite
            for v in gen_variants:
                aid = v.get("agent_id")
                if aid in parent_genomes:
                    parent_genomes[aid] = v.get("genome")
                    parent_variant_ids[aid] = v.get("id")
            elite = select_elite(gen_variants)
            if elite and elite.get("agent_id") in parent_genomes:
                parent_genomes[elite["agent_id"]] = elite.get("genome")
                parent_variant_ids[elite["agent_id"]] = elite.get("id")

        run_id = f"coevo_{uuid.uuid4().hex[:12]}"
        run_record = {
            "id": run_id,
            "organization_id": current_user.organization_id,
            "domain_id": domain,
            "generations_requested": gens,
            "generations": generation_summaries,
            "agent_ids": [planner_id, aesthetics_id],
            "base_workflow_id": base_workflow_id,
            "variant_ids": all_variant_ids,
            "sandbox_only": True,
            "auto_promote": False,
            "created_at": utc_now(),
            "created_by": current_user.id,
        }
        self.store.state.setdefault("coevolution_runs", [])
        self.store.collection("coevolution_runs").append(run_record)

        # Invariant: production DNA version unchanged when base was in store
        if base is not None and production_version is not None:
            current = next(
                (w for w in self._scoped_items("workflows", current_user.organization_id) if w["id"] == base_workflow_id),
                None,
            )
            if current and current.get("version") != production_version:
                raise ValidationError("Invariant violated: production DNA changed during coevolution")

        self._append_audit(
            current_user.organization_id,
            current_user.id,
            "evolution",
            "evolution.coevolution_completed",
            "coevolution_run",
            run_id,
            {
                "generations": gens,
                "domain_id": domain,
                "variant_count": len(all_variant_ids),
                "auto_promote": False,
                "sandbox_only": True,
            },
            "success",
        )
        self.store.save()
        return deepcopy(run_record)

    def lesson_utility_dashboard(
        self,
        current_user: AuthenticatedUser,
        *,
        agent_id: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Ranked lesson utility + aggregate reuse/growth metrics (Wave 3)."""
        self.assert_permission(current_user, "memory:read")
        lim = max(1, min(int(limit or 20), 200))
        lessons = self.list_improvement_lessons(current_user, agent_id=agent_id, limit=lim)
        metrics = self.improvement_metrics(current_user, agent_id=agent_id)
        by_agent: dict[str, dict[str, Any]] = {}
        for lesson in lessons:
            aid = lesson.get("agent_id") or "_unscoped"
            bucket = by_agent.setdefault(aid, {"count": 0, "utility_sum": 0.0, "uses": 0})
            bucket["count"] += 1
            bucket["utility_sum"] += float(lesson.get("utility") or 0.0)
            bucket["uses"] += int(lesson.get("uses") or 0)
        by_agent_out = {
            k: {
                "count": v["count"],
                "avg_utility": round(v["utility_sum"] / max(v["count"], 1), 4),
                "uses": v["uses"],
            }
            for k, v in by_agent.items()
        }
        return {
            "lessons": lessons,
            "aggregates": {
                "total_lessons": metrics.get("knowledge_growth_count", len(lessons)),
                "knowledge_growth_count": metrics.get("knowledge_growth_count", len(lessons)),
                "lesson_reuse_rate": metrics.get("lesson_reuse_rate", 0.0),
                "lesson_win_rate": metrics.get("lesson_win_rate", 0.0),
                "by_agent": by_agent_out,
            },
            "limit": lim,
            "agent_id": agent_id,
        }

    def governance_review_learned_artifacts(self, current_user: AuthenticatedUser) -> dict[str, Any]:
        """List pending sandbox variants and skill proposals for human sign-off (no promote)."""
        self.assert_permission(current_user, "workflows:read")
        pending_statuses = {"sandbox_proposed", "sandbox_evaluated", "approved_for_canary"}
        variants = self._scoped_items("evolution_variants", current_user.organization_id)
        pending_variants = []
        for v in variants:
            if v.get("status") not in pending_statuses:
                continue
            if v.get("sandbox_only") is False and v.get("status") == "promoted":
                continue
            pending_variants.append(
                {
                    "id": v.get("id"),
                    "name": v.get("name"),
                    "status": v.get("status"),
                    "sandbox_only": v.get("sandbox_only", True),
                    "variant_type": v.get("variant_type"),
                    "agent_id": v.get("agent_id"),
                    "fitness_metrics": v.get("fitness_metrics")
                    or (v.get("evaluation") or {}).get("fitness_metrics")
                    or {},
                    "promotion_decision": v.get("promotion_decision"),
                    "created_at": v.get("created_at"),
                }
            )
        self.store.state.setdefault("skill_proposals", [])
        skills = [
            p
            for p in self.store.collection("skill_proposals")
            if p.get("organization_id") == current_user.organization_id
            and p.get("status") in {None, "sandbox_proposed", "proposed"}
            and p.get("sandbox_only", True)
        ]
        pending_skills = [
            {
                "id": s.get("id"),
                "skill_name": s.get("skill_name"),
                "status": s.get("status"),
                "sandbox_only": s.get("sandbox_only", True),
                "sandbox_path": s.get("sandbox_path") or s.get("written_path"),
                "domain": s.get("domain"),
                "created_at": s.get("created_at"),
            }
            for s in skills
        ]
        return {
            "pending_variants": pending_variants,
            "pending_skills": pending_skills,
            "policy": "human_signoff_required",
            "auto_promote": False,
            "counts": {
                "variants": len(pending_variants),
                "skills": len(pending_skills),
            },
        }


runtime = RuntimeServices()
