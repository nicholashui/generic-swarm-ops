from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: str
    new_password: str


class ApiKeyCreateRequest(BaseModel):
    name: str = "service-key"


class UserCreateRequest(BaseModel):
    email: str
    name: str
    role: str = "viewer"
    password: str = "change-me"
    department: str = "general"
    status: str = "active"


class UserUpdateRequest(BaseModel):
    name: str | None = None
    role: str | None = None
    department: str | None = None
    status: str | None = None


class InvitationCreateRequest(BaseModel):
    email: str
    name: str | None = None
    role: str = "viewer"
    department: str = "general"


class InvitationAcceptRequest(BaseModel):
    token: str
    password: str
    name: str | None = None


class OrganizationUpdateRequest(BaseModel):
    name: str | None = None
    slug: str | None = None
    status: str | None = None


class RunExpireRequest(BaseModel):
    reason: str | None = None


class AgentCreateRequest(BaseModel):
    id: str
    name: str
    description: str | None = None
    version: str = "1.0.0"
    department: str = "general"
    allowed_tools: list[str] = Field(default_factory=list)
    allowed_memory_scopes: list[str] = Field(default_factory=list)
    allowed_workflow_types: list[str] = Field(default_factory=list)
    risk_level: str = "tier_2_draft"
    runtime_configuration: dict[str, Any] = Field(default_factory=dict)
    status: str = "draft"
    role: str = "execution"


class ToolCreateRequest(BaseModel):
    id: str
    name: str
    description: str | None = None
    category: str = "internal_api"
    input_schema: dict[str, Any] = Field(default_factory=lambda: {"type": "object"})
    output_schema: dict[str, Any] = Field(default_factory=lambda: {"type": "object"})
    risk_level: str = "tier_2_draft"
    required_permissions: list[str] = Field(default_factory=lambda: ["workflows:execute"])
    approval_requirement: bool = False
    timeout: int = 30
    retry_policy: dict[str, Any] = Field(default_factory=lambda: {"max_retries": 1})
    enabled: bool = True
    allowed_actions: list[str] = Field(default_factory=list)
    scope: str = "custom"


class StatusUpdateRequest(BaseModel):
    status: str | None = None
    enabled: bool | None = None


class WorkflowStartRequest(BaseModel):
    input_payload: dict[str, Any] = Field(default_factory=dict)


class WorkflowCreateRequest(BaseModel):
    id: str
    name: str
    description: str | None = None
    version: str = "1.0.0"
    department: str = "general"
    risk_tier: str = "tier_2_draft"
    input_schema: dict[str, Any] = Field(default_factory=lambda: {"type": "object", "properties": {}, "required": []})
    output_schema: dict[str, Any] = Field(default_factory=lambda: {"type": "object", "properties": {}, "required": []})
    steps: list[dict[str, Any]]
    governance_policy: dict[str, Any] = Field(default_factory=dict)
    evaluation_policy: dict[str, Any] = Field(default_factory=dict)
    status: str = "draft"
    memory_reads: list[str] = Field(default_factory=list)
    memory_writes: list[str] = Field(default_factory=list)
    guardrails: dict[str, Any] = Field(default_factory=dict)
    verification: dict[str, Any] = Field(default_factory=dict)
    rollback: dict[str, Any] = Field(default_factory=dict)
    fitness_metrics: list[str] = Field(default_factory=list)
    audit_log_write_required: bool = True
    provenance: dict[str, Any] = Field(default_factory=dict)


class WorkflowUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    department: str | None = None
    risk_tier: str | None = None
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    steps: list[dict[str, Any]] = Field(default_factory=list)
    status: str | None = None
    memory_reads: list[str] = Field(default_factory=list)
    memory_writes: list[str] = Field(default_factory=list)
    guardrails: dict[str, Any] | None = None
    verification: dict[str, Any] | None = None
    rollback: dict[str, Any] | None = None
    fitness_metrics: list[str] = Field(default_factory=list)


class WorkflowVersionCreateRequest(BaseModel):
    version: str
    steps: list[dict[str, Any]] = Field(default_factory=list)


class ApprovalDecisionRequest(BaseModel):
    decision: str
    reason: str | None = None


class ApprovalReassignRequest(BaseModel):
    reviewer_user_id: str


class MemoryCreateRequest(BaseModel):
    scope: str
    title: str
    content: str
    department: str = "general"
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding_reference: str | None = None
    sensitivity_level: str = "internal"
    allowed_roles: list[str] = Field(default_factory=list)
    expires_at: str | None = None


class MemoryUpdateRequest(BaseModel):
    scope: str | None = None
    title: str | None = None
    content: str | None = None
    department: str | None = None
    metadata: dict[str, Any] | None = None
    embedding_reference: str | None = None
    sensitivity_level: str | None = None
    allowed_roles: list[str] = Field(default_factory=list)
    expires_at: str | None = None


class KnowledgeUploadRequest(BaseModel):
    id: str
    title: str
    content: str
    path: str | None = None
    status: str = "indexed"
    sensitivity: str = "internal"
    allowed_roles: list[str] = Field(default_factory=list)
    failure_reason: str | None = None


class KnowledgeSearchRequest(BaseModel):
    query: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)
    limit: int = 10
    multi_hop: bool = False


class MemorySearchRequest(BaseModel):
    query: str | None = None
    scope: str | None = None
    acting_agent_id: str | None = None


class EvaluationRunRequest(BaseModel):
    run_id: str


class GovernancePolicyRequest(BaseModel):
    id: str | None = None
    name: str
    conditions: dict[str, Any] = Field(default_factory=dict)
    action: str = "allow"
    reviewer_role: str | None = None
    risk_level: str = "medium"
    status: str = "active"


class GovernanceCheckRequest(BaseModel):
    action: str = "allow"
    risk_level: str | None = None
    workflow_id: str | None = None
    step_id: str | None = None
    tool_category: str | None = None
    resource_type: str | None = None
    sensitivity: str | None = None
