import type { AppRole, Permission } from "@/types/permissions";

const rolePermissions: Record<AppRole, Permission[]> = {
  owner: ["agents:read","agents:create","agents:update","tools:read","tools:update","workflows:read","workflows:create","workflows:update","workflow_runs:read","workflow_runs:cancel","workflow_runs:retry","approvals:read","approvals:approve","knowledge:read","knowledge:write","memory:read","memory:write","evaluations:read","processes:read","audit:read","settings:read","settings:update","users:read","billing:read"],
  admin: ["agents:read","agents:create","agents:update","tools:read","tools:update","workflows:read","workflows:create","workflows:update","workflow_runs:read","workflow_runs:cancel","workflow_runs:retry","approvals:read","approvals:approve","knowledge:read","knowledge:write","memory:read","memory:write","evaluations:read","processes:read","audit:read","settings:read","settings:update","users:read"],
  developer: ["agents:read","agents:create","agents:update","tools:read","tools:update","workflows:read","workflows:create","workflows:update","workflow_runs:read","knowledge:read","knowledge:write","memory:read","evaluations:read","processes:read"],
  operator: ["agents:read","tools:read","workflows:read","workflow_runs:read","workflow_runs:cancel","workflow_runs:retry","approvals:read","knowledge:read","memory:read","evaluations:read","processes:read"],
  reviewer: ["approvals:read","approvals:approve","workflow_runs:read","audit:read"],
  viewer: ["agents:read","tools:read","workflows:read","workflow_runs:read","knowledge:read","memory:read","evaluations:read","processes:read","audit:read"],
  billing_manager: ["settings:read","billing:read"],
  security_auditor: ["audit:read","settings:read"],
};

export function getPermissionsForRole(role: AppRole): Permission[] { return rolePermissions[role] ?? []; }
export function hasPermission(role: AppRole, permission: Permission): boolean { return getPermissionsForRole(role).includes(permission); }
