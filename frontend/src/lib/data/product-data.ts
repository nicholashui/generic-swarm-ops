/**
 * Product data facade: demo fixtures when demoMode, live backend otherwise.
 * Live path uses backendApi which resolves gso_access_token from cookies on the server.
 */
import { env } from "@/lib/config/env";
import {
  agents as demoAgents,
  apiKeys as demoApiKeys,
  approvals as demoApprovals,
  auditLogs as demoAudit,
  dashboardMetrics as demoMetrics,
  evaluations as demoEvals,
  knowledgeDocuments as demoKnowledge,
  memoryItems as demoMemory,
  onboardingChecklist,
  processes as demoProcesses,
  tools as demoTools,
  userRows as demoUsers,
  workflowRunEvents as demoEvents,
  workflows as demoWorkflows,
} from "@/lib/demo-data";
import {
  fetchLiveAgents,
  fetchLiveApiKeys,
  fetchLiveApprovals,
  fetchLiveAuditLogs,
  fetchLiveEvaluations,
  fetchLiveKnowledge,
  fetchLiveMemory,
  fetchLiveProcessSummary,
  fetchLiveTools,
  fetchLiveUsers,
  fetchLiveWorkflowRuns,
  fetchLiveWorkflows,
} from "@/lib/api/live-data";

export async function loadProductBundle() {
  if (env.demoMode) {
    return {
      demoMode: true as const,
      agents: demoAgents,
      tools: demoTools,
      workflows: demoWorkflows,
      approvals: demoApprovals,
      knowledgeDocuments: demoKnowledge,
      memoryItems: demoMemory,
      evaluations: demoEvals,
      processes: demoProcesses,
      auditLogs: demoAudit,
      apiKeys: demoApiKeys,
      userRows: demoUsers,
      workflowRunEvents: demoEvents,
      dashboardMetrics: demoMetrics,
      onboardingChecklist,
    };
  }

  const [
    agents,
    tools,
    workflows,
    approvals,
    knowledgeDocuments,
    memoryItems,
    evaluations,
    processes,
    auditLogs,
    apiKeys,
    userRows,
    workflowRunEvents,
  ] = await Promise.all([
    fetchLiveAgents(),
    fetchLiveTools(),
    fetchLiveWorkflows(),
    fetchLiveApprovals(),
    fetchLiveKnowledge(),
    fetchLiveMemory(),
    fetchLiveEvaluations(),
    fetchLiveProcessSummary(),
    fetchLiveAuditLogs(),
    fetchLiveApiKeys(),
    fetchLiveUsers(),
    fetchLiveWorkflowRuns(),
  ]);

  return {
    demoMode: false as const,
    agents,
    tools,
    workflows,
    approvals,
    knowledgeDocuments,
    memoryItems,
    evaluations,
    processes,
    auditLogs,
    apiKeys,
    userRows,
    workflowRunEvents,
    dashboardMetrics: [
      { label: "Active agents", value: String(agents.length), delta: "Live API" },
      { label: "Workflows", value: String(workflows.length), delta: "Live API" },
      { label: "Pending approvals", value: String(approvals.filter((a) => a.status === "pending").length), delta: "Live API" },
      { label: "Audit events", value: String(auditLogs.length), delta: "Live API" },
    ],
    onboardingChecklist,
  };
}

export async function loadAgents() {
  return (await loadProductBundle()).agents;
}
export async function loadTools() {
  return (await loadProductBundle()).tools;
}
export async function loadWorkflows() {
  return (await loadProductBundle()).workflows;
}
export async function loadApprovals() {
  return (await loadProductBundle()).approvals;
}
export async function loadKnowledge() {
  return (await loadProductBundle()).knowledgeDocuments;
}
export async function loadMemory() {
  return (await loadProductBundle()).memoryItems;
}
export async function loadEvaluations() {
  return (await loadProductBundle()).evaluations;
}
export async function loadProcesses() {
  return (await loadProductBundle()).processes;
}
export async function loadAuditLogs() {
  return (await loadProductBundle()).auditLogs;
}
