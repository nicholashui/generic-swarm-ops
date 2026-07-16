/**
 * AC1 live-ops mutation surface manifest.
 * Each surface must be implemented by a client component that calls the listed backendApi method.
 */
export const LIVE_OPS_SURFACES = [
  {
    id: "approve",
    method: "decideApproval",
    component: "src/components/domain/approval-decision-panel.tsx",
  },
  {
    id: "reject",
    method: "decideApproval",
    component: "src/components/domain/approval-decision-panel.tsx",
  },
  {
    id: "retry",
    method: "retryWorkflowRun",
    component: "src/components/domain/workflow-run-console.tsx",
  },
  {
    id: "cancel",
    method: "cancelWorkflowRun",
    component: "src/components/domain/workflow-run-console.tsx",
  },
  {
    id: "pause",
    method: "pauseWorkflowRun",
    component: "src/components/domain/workflow-run-console.tsx",
  },
  {
    id: "resume",
    method: "resumeWorkflowRun",
    component: "src/components/domain/workflow-run-console.tsx",
  },
  {
    id: "expire",
    method: "expireWorkflowRun",
    component: "src/components/domain/workflow-run-console.tsx",
  },
  {
    id: "create_agent",
    method: "createAgent",
    component: "src/components/domain/form-route-actions.tsx",
  },
  {
    id: "create_workflow",
    method: "createWorkflow",
    component: "src/components/domain/form-route-actions.tsx",
  },
  {
    id: "run_now",
    method: "startWorkflowRun",
    component: "src/components/domain/run-workflow-button.tsx",
  },
  {
    id: "invite_user",
    method: "createInvitation",
    component: "src/components/domain/user-admin-panel.tsx",
  },
  {
    id: "disable_user",
    method: "updateUser",
    component: "src/components/domain/user-admin-panel.tsx",
  },
  {
    id: "org_save",
    method: "updateOrganization",
    component: "src/components/domain/organization-settings-form.tsx",
  },
  // accept-invite uses same-origin BFF /api/auth/accept-invite (httpOnly cookies), not backendApi.*
] as const;

export type LiveOpsSurfaceId = (typeof LIVE_OPS_SURFACES)[number]["id"];
