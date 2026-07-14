import Link from "next/link";
import type { ReactNode } from "react";
import { ArrowRight, FileKey2, Play, Plus } from "lucide-react";
import { ApiKeyTable } from "@/components/domain/api-key-table";
import { ApprovalDecisionPanel } from "@/components/domain/approval-decision-panel";
import { DetailMetadata } from "@/components/domain/detail-metadata";
import { EvolutionArchivePanel } from "@/components/domain/evolution-archive-panel";
import { FormRouteActions, type FormMutationKind } from "@/components/domain/form-route-actions";
import { ImproveRunButton } from "@/components/domain/improve-run-button";
import { OrganizationSettingsForm } from "@/components/domain/organization-settings-form";
import { RunWorkflowButton } from "@/components/domain/run-workflow-button";
import { UserAdminPanel } from "@/components/domain/user-admin-panel";
import { WorkflowRunConsole } from "@/components/domain/workflow-run-console";
import { DomainPackPanel } from "@/components/domain/domain-pack-panel";
import { RecommendWorkflowPanel } from "@/components/domain/recommend-workflow-panel";
import { SpecialSkillsPanel } from "@/components/domain/special-skills-panel";
import { VideoN3RosterPanel } from "@/components/domain/video-n3-roster-panel";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { DataTable } from "@/components/ui/data-table";
import { EmptyState } from "@/components/ui/empty-state";
import { ErrorState } from "@/components/ui/error-state";
import { MetricCard } from "@/components/ui/metric-card";
import { SearchInput } from "@/components/ui/search-input";
import { Section } from "@/components/ui/section";
import { StatusBadge } from "@/components/ui/status-badge";
import { loadProductBundle } from "@/lib/data/product-data";
import { env } from "@/lib/config/env";
import { formatDateTime } from "@/lib/formatting/dates";

type Column<T> = {
  key: keyof T | string;
  label: string;
  render?: (row: T) => ReactNode;
};

type Metric = {
  label: string;
  value: string;
  delta: string;
};

type KnowledgeSource = {
  id: string;
  name: string;
  type: string;
  status: string;
  documentCount: number;
  lastSync: string;
  errorCount: number;
};

const knowledgeSources: KnowledgeSource[] = [
  {
    id: "source_confluence",
    name: "Confluence space",
    type: "Confluence",
    status: "connected",
    documentCount: 48,
    lastSync: "2026-07-07T05:30:00Z",
    errorCount: 0,
  },
  {
    id: "source_notion",
    name: "Operations Notion",
    type: "Notion",
    status: "failed",
    documentCount: 22,
    lastSync: "2026-07-07T06:12:00Z",
    errorCount: 3,
  },
  {
    id: "source_uploads",
    name: "Internal uploads",
    type: "File upload",
    status: "indexing",
    documentCount: 13,
    lastSync: "2026-07-07T08:03:00Z",
    errorCount: 0,
  },
];

const roleMatrix = [
  {
    id: "role_owner",
    role: "Owner",
    focus: "Organization-wide governance",
    permissions: "Full access across agents, workflows, settings, and billing.",
  },
  {
    id: "role_admin",
    role: "Admin",
    focus: "Runtime and configuration operations",
    permissions: "Can manage users, settings, agents, tools, and workflows.",
  },
  {
    id: "role_reviewer",
    role: "Reviewer",
    focus: "Approval and audit coverage",
    permissions: "Reviews high-risk approvals and investigates audit activity.",
  },
  {
    id: "role_viewer",
    role: "Viewer",
    focus: "Read-only observability",
    permissions: "Can inspect the system without mutating sensitive assets.",
  },
];

const integrationCards = [
  {
    href: "/app/tools/tool_slack",
    title: "Slack workspace",
    description: "Communication channel for workflow alerts and human approvals.",
  },
  {
    href: "/app/tools/tool_notion",
    title: "Knowledge sync",
    description: "Index documents and policy references with freshness indicators.",
  },
  {
    href: "/app/settings/api-keys",
    title: "API automation",
    description: "Provision masked machine credentials for internal integrations.",
  },
];

function ListRoutePage<T extends { id: string | number }>(props: {
  eyebrow: string;
  title: string;
  description: string;
  rows: T[];
  columns: Column<T>[];
  metrics: Metric[];
  actions?: ReactNode;
  searchPlaceholder: string;
  emptyTitle: string;
  emptyDescription: string;
  children?: ReactNode;
}) {
  return (
    <Section
      eyebrow={props.eyebrow}
      title={props.title}
      description={props.description}
      actions={props.actions}
    >
      <div className="grid gap-4 xl:grid-cols-4">
        {props.metrics.map((metric) => (
          <MetricCard key={metric.label} delta={metric.delta} label={metric.label} value={metric.value} />
        ))}
      </div>
      <SearchInput placeholder={props.searchPlaceholder} />
      {props.rows.length ? (
        <DataTable caption={props.title} rows={props.rows} columns={props.columns} />
      ) : (
        <EmptyState title={props.emptyTitle} description={props.emptyDescription} />
      )}
      {props.children}
    </Section>
  );
}

function DetailRoutePage(props: {
  eyebrow: string;
  title: string;
  description: string;
  status?: string;
  metadata: Array<{ label: string; value: string }>;
  actions?: ReactNode;
  children: ReactNode;
}) {
  return (
    <Section
      eyebrow={props.eyebrow}
      title={props.title}
      description={props.description}
      actions={
        <>
          {props.status ? <StatusBadge status={props.status} /> : null}
          {props.actions}
        </>
      }
    >
      <DetailMetadata items={props.metadata} />
      {props.children}
    </Section>
  );
}

function FormRoutePage(props: {
  eyebrow: string;
  title: string;
  description: string;
  sections: Array<{ title: string; description: string; fields: string[] }>;
  draftLabel: string;
  submitLabel: string;
  notes: string[];
  mutationKind: FormMutationKind;
  resourceHint?: string;
}) {
  const realForm = props.mutationKind === "agent" || props.mutationKind === "workflow";
  return (
    <Section eyebrow={props.eyebrow} title={props.title} description={props.description}>
      <div className={`grid gap-6 ${realForm ? "xl:grid-cols-[1.25fr_0.75fr]" : "xl:grid-cols-[1.15fr_0.85fr]"}`}>
        <div className="space-y-5">
          {realForm ? (
            <Card className="p-6">
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Form</p>
              <p className="mt-2 text-sm leading-7 text-muted">
                Fill real fields below. Mutations call the FastAPI backend when demo mode is off; errors include backend message and request id.
              </p>
              <div className="mt-5">
                <FormRouteActions
                  kind={props.mutationKind}
                  draftLabel={props.draftLabel}
                  submitLabel={props.submitLabel}
                  resourceHint={props.resourceHint}
                />
              </div>
            </Card>
          ) : (
            props.sections.map((section) => (
              <Card key={section.title} className="p-6">
                <h2 className="text-lg font-semibold text-white">{section.title}</h2>
                <p className="mt-2 leading-7 text-muted">{section.description}</p>
                <div className="mt-5 grid gap-3 md:grid-cols-2">
                  {section.fields.map((field) => (
                    <div
                      key={field}
                      className="rounded-2xl border border-dashed border-white/12 bg-white/4 px-4 py-3 text-sm text-white"
                    >
                      {field}
                    </div>
                  ))}
                </div>
              </Card>
            ))
          )}
        </div>
        <div className="space-y-5">
          <Card className="p-6">
            <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Guidance</p>
            <ul className="mt-4 space-y-3 text-sm leading-7 text-muted">
              {props.notes.map((note) => (
                <li key={note}>{note}</li>
              ))}
            </ul>
          </Card>
          {!realForm ? (
            <Card className="p-6">
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Actions</p>
              <div className="mt-4">
                <FormRouteActions
                  kind={props.mutationKind}
                  draftLabel={props.draftLabel}
                  submitLabel={props.submitLabel}
                  resourceHint={props.resourceHint}
                />
              </div>
            </Card>
          ) : null}
        </div>
      </div>
    </Section>
  );
}

function HubCards(props: {
  eyebrow: string;
  title: string;
  description: string;
  metrics: Metric[];
  cards: Array<{ href: string; title: string; description: string }>;
}) {
  return (
    <Section eyebrow={props.eyebrow} title={props.title} description={props.description}>
      <div className="grid gap-4 xl:grid-cols-4">
        {props.metrics.map((metric) => (
          <MetricCard key={metric.label} delta={metric.delta} label={metric.label} value={metric.value} />
        ))}
      </div>
      <div className="grid gap-5 lg:grid-cols-3">
        {props.cards.map((card) => (
          <Link
            key={card.href}
            href={card.href}
            className="surface-card rounded-[24px] border px-6 py-5 transition hover:border-white/20 hover:bg-white/7"
          >
            <p className="text-sm font-semibold text-white">{card.title}</p>
            <p className="mt-3 leading-7 text-muted">{card.description}</p>
            <p className="mt-5 inline-flex items-center gap-2 text-sm text-[var(--accent)]">
              Open route
              <ArrowRight className="size-4" />
            </p>
          </Link>
        ))}
      </div>
    </Section>
  );
}

function NotFoundPanel({ slug }: { slug: string[] }) {
  return (
    <Section
      eyebrow="Route"
      title="Unknown application path"
      description="The requested operational view is not defined in the current frontend scaffold."
    >
      <ErrorState
        title="Route not found"
        description={`No page configuration exists for /app/${slug.join("/")}.`}
      />
    </Section>
  );
}

export default async function AppCatchAllPage({
  params,
}: {
  params: Promise<{ slug?: string[] }>;
}) {
  const slug = (await params).slug ?? [];
  const {
    agents,
    apiKeys,
    approvals,
    auditLogs,
    evaluations,
    knowledgeDocuments,
    memoryItems,
    processes,
    tools,
    userRows,
    workflowRunEvents,
    workflows,
  } = await loadProductBundle();

  if (!slug.length) {
    return <NotFoundPanel slug={[""]} />;
  }

  const [section, child, grandchild] = slug;

  if (section === "domains") {
    return (
      <div className="space-y-6">
        <DomainPackPanel agents={agents as never[]} />
        <Card className="p-6">
          <VideoN3RosterPanel />
        </Card>
        <Card className="p-6">
          <RecommendWorkflowPanel />
        </Card>
        <Card className="p-6">
          <SpecialSkillsPanel />
        </Card>
      </div>
    );
  }

  if (section === "agents") {
    if (!child) {
      return (
        <div className="space-y-6">
          <DomainPackPanel agents={agents as never[]} />
          <ListRoutePage
            eyebrow="Agents"
            title="Organization agent catalog"
            description="Inspect AI workers, capability coverage, knowledge access, and operational ownership before you expose them to live business workflows."
            rows={agents}
            columns={[
              {
                key: "name",
                label: "Agent",
                render: (row) => (
                  <div>
                    <p className="font-medium text-white">{row.name}</p>
                    <p className="mt-1 text-xs text-muted">{row.description}</p>
                  </div>
                ),
              },
              { key: "owner", label: "Owner" },
              { key: "toolCount", label: "Tools" },
              { key: "knowledgeAccess", label: "Knowledge" },
              {
                key: "status",
                label: "Status",
                render: (row) => <StatusBadge status={row.status} />,
              },
              {
                key: "updatedAt",
                label: "Updated",
                render: (row) => formatDateTime(row.updatedAt),
              },
            ]}
            metrics={[
              { label: "Total agents", value: String(agents.length), delta: "Scoped to the current organization" },
              { label: "Active", value: String(agents.filter((item) => item.status === "active").length), delta: "Ready for governed workflows" },
              { label: "Draft", value: String(agents.filter((item) => item.status === "draft").length), delta: "Still waiting for release review" },
              { label: "Knowledge-linked", value: String(agents.filter((item) => item.knowledgeAccess !== "None").length), delta: "Attached to curated sources" },
            ]}
            actions={
              <Button asChild href="/app/agents/new">
                <Plus className="size-4" />
                Create agent
              </Button>
            }
            searchPlaceholder="Search agents by owner, status, tool scope, or knowledge access"
            emptyTitle="No agents yet"
            emptyDescription="Create your first agent to begin governed business automation."
          />
        </div>
      );
    }

    if (child === "new") {
      return (
        <FormRoutePage
          eyebrow="Agents"
          title="Create agent"
          description="Define the agent identity, its instruction set, the tools it may call, and the safety controls that govern high-risk behavior."
          mutationKind="agent"
          resourceHint="ui_created_agent"
          sections={[
            {
              title: "Identity and purpose",
              description: "Capture who the agent is, what it owns, and how it should be described in audits and approvals.",
              fields: ["Agent name", "Business description", "Owner team", "Primary outcome"],
            },
            {
              title: "Instructions and model profile",
              description: "Set explicit behavior, escalation rules, and provider assumptions before the agent can execute live work.",
              fields: ["System instructions", "Model or provider", "Success criteria", "Fallback behavior"],
            },
            {
              title: "Access controls",
              description: "Choose tools, memory scopes, knowledge sources, and reviewer gates deliberately.",
              fields: ["Tool permissions", "Knowledge sources", "Memory policy", "Approval threshold"],
            },
          ]}
          draftLabel="Save draft"
          submitLabel="Create agent"
          notes={[
            "Dangerous tool access should remain explicit and reviewable.",
            "Knowledge and memory visibility belong to the backend authorization model.",
            "Add a test prompt before you graduate this agent into production workflows.",
          ]}
        />
      );
    }

    const agent = agents.find((item) => item.id === child);
    if (!agent) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Agents"
        title={agent.name}
        description="Review the current agent posture, knowledge reach, recent evaluations, and runtime ownership before enabling changes."
        status={agent.status}
        metadata={[
          { label: "Owner", value: agent.owner },
          { label: "Tool count", value: String(agent.toolCount) },
          { label: "Knowledge", value: agent.knowledgeAccess },
          { label: "Updated", value: formatDateTime(agent.updatedAt) },
        ]}
        actions={
          <>
            <Button variant="secondary">Run test</Button>
            <Button variant="ghost">Archive</Button>
          </>
        }
      >
        <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Instructions overview</h2>
            <p className="mt-3 leading-7 text-muted">
              {agent.description} This agent follows governed tool permissions and uses role-aware escalation before it triggers reviewer checkpoints.
            </p>
          </Card>
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Recent evaluation posture</h2>
            <DataTable
              caption="Agent evaluations"
              rows={evaluations}
              columns={[
                { key: "name", label: "Suite" },
                { key: "target", label: "Target" },
                { key: "score", label: "Score" },
                {
                  key: "status",
                  label: "Status",
                  render: (row) => <StatusBadge status={row.status} />,
                },
              ]}
            />
          </Card>
        </div>
      </DetailRoutePage>
    );
  }

  if (section === "tools") {
    if (!child) {
      return (
        <ListRoutePage
          eyebrow="Tools"
          title="Integration and tool catalog"
          description="Track connection health, credential posture, adoption, and which capabilities are available to governed agents and workflows."
          rows={tools}
          columns={[
            { key: "name", label: "Tool" },
            { key: "category", label: "Category" },
            { key: "usageCount", label: "Usage" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "lastUsed",
              label: "Last used",
              render: (row) => formatDateTime(row.lastUsed),
            },
          ]}
          metrics={[
            { label: "Connected", value: String(tools.filter((item) => item.status === "connected").length), delta: "Healthy integrations ready for execution" },
            { label: "Errors", value: String(tools.filter((item) => item.status === "error").length), delta: "Need reconnection or credentials review" },
            { label: "Categories", value: String(new Set(tools.map((item) => item.category)).size), delta: "Coverage across the automation surface" },
            { label: "Calls", value: String(tools.reduce((total, item) => total + item.usageCount, 0)), delta: "Recorded recent usage count" },
          ]}
          searchPlaceholder="Search tools by category, connection state, or credential posture"
          emptyTitle="No tools configured"
          emptyDescription="Connect an integration before agents and workflows can use external capabilities."
        />
      );
    }

    const tool = tools.find((item) => item.id === child);
    if (!tool) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Tools"
        title={tool.name}
        description="Inspect connection state, credential handling posture, and downstream usage before enabling the tool for more automation paths."
        status={tool.status}
        metadata={[
          { label: "Category", value: tool.category },
          { label: "Usage count", value: String(tool.usageCount) },
          { label: "Last used", value: formatDateTime(tool.lastUsed) },
          { label: "Credential state", value: tool.credentials },
        ]}
        actions={
          <>
            <Button variant="secondary">Test connection</Button>
            <Button variant="ghost">Rotate credentials</Button>
          </>
        }
      >
        <div className="grid gap-6 xl:grid-cols-2">
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Credential posture</h2>
            <p className="mt-3 leading-7 text-muted">
              Secret values are never rendered in the frontend. This view only exposes masked operational status and required actions.
            </p>
          </Card>
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Downstream usage</h2>
            <p className="mt-3 leading-7 text-muted">
              Agents and workflows that depend on this integration should be reviewed before any disconnect or scope reduction happens.
            </p>
          </Card>
        </div>
      </DetailRoutePage>
    );
  }

  if (section === "workflows") {
    if (!child) {
      return (
        <ListRoutePage
          eyebrow="Workflows"
          title="Workflow operating inventory"
          description="Monitor repeatable business processes, their release posture, trigger configuration, and recent execution performance."
          rows={workflows}
          columns={[
            { key: "name", label: "Workflow" },
            { key: "trigger", label: "Trigger" },
            { key: "owner", label: "Owner" },
            { key: "successRate", label: "Success rate" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "updatedAt",
              label: "Updated",
              render: (row) => formatDateTime(row.updatedAt),
            },
          ]}
          metrics={[
            { label: "Total workflows", value: String(workflows.length), delta: "Tracked inside the current organization" },
            { label: "Active", value: String(workflows.filter((item) => item.status === "active").length), delta: "Eligible to run now" },
            { label: "Paused", value: String(workflows.filter((item) => item.status === "paused").length), delta: "Held behind operator intent" },
            { label: "Pending approvals", value: String(approvals.filter((item) => item.status === "pending").length), delta: "Human review still required" },
          ]}
          actions={
            <Button asChild href="/app/workflows/new">
              <Plus className="size-4" />
              Create workflow
            </Button>
          }
          searchPlaceholder="Search workflows by trigger, owner, status, or release posture"
          emptyTitle="No workflows yet"
          emptyDescription="Create a workflow to automate a repeatable business process."
        />
      );
    }

    if (child === "new") {
      return (
        <FormRoutePage
          eyebrow="Workflows"
          title="Create workflow"
          description="Compose agent steps, tool actions, approvals, and branching rules in a flow that the backend can execute and audit safely."
          mutationKind="workflow"
          resourceHint="ui_created_workflow"
          sections={[
            {
              title: "Workflow identity",
              description: "Define the business goal, trigger, and owner who will be responsible for runtime quality.",
              fields: ["Workflow name", "Business description", "Trigger type", "Owner"],
            },
            {
              title: "Execution graph",
              description: "Sketch the sequence of agent, tool, approval, and condition steps that make up the automation.",
              fields: ["Agent step", "Tool call", "Condition branch", "Approval gate"],
            },
            {
              title: "Release checks",
              description: "Capture the evaluation posture, rollout guardrails, and operational notes before publishing.",
              fields: ["Evaluation suite", "Rollback strategy", "Escalation path", "Runtime notes"],
            },
          ]}
          draftLabel="Save draft"
          submitLabel="Publish workflow"
          notes={[
            "Redirect users to the workflow run view immediately after the backend starts a run.",
            "Approval checkpoints should remain explicit and explainable.",
            "Version history belongs in the detail page after publication.",
          ]}
        />
      );
    }

    const workflow = workflows.find((item) => item.id === child);
    if (!workflow) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Workflows"
        title={workflow.name}
        description="Inspect the release posture, runtime success rate, approval dependencies, and the latest execution path for this workflow."
        status={workflow.status}
        metadata={[
          { label: "Owner", value: workflow.owner },
          { label: "Trigger", value: workflow.trigger },
          { label: "Success rate", value: workflow.successRate },
          { label: "Updated", value: formatDateTime(workflow.updatedAt) },
        ]}
        actions={
          <>
            <Button asChild href="/app/workflow-runs/run_01" variant="secondary">
              <Play className="size-4" />
              View latest run
            </Button>
            <RunWorkflowButton
              workflowId={workflow.id}
              inputSchema={
                (workflow as { input_schema?: { type?: string; required?: string[]; properties?: Record<string, { type?: string }> } })
                  .input_schema || {
                  type: "object",
                  required: ["case_id"],
                  properties: { case_id: { type: "string" }, triggered_from: { type: "string" } },
                }
              }
            />
          </>
        }
      >
        <div className="grid gap-6 xl:grid-cols-2">
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Visual step map</h2>
            <p className="mt-3 leading-7 text-muted">
              {workflow.description} This scaffold reserves space for the full step graph, approval checkpoints, and branching conditions.
            </p>
          </Card>
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Version and release notes</h2>
            <p className="mt-3 leading-7 text-muted">
              Use this panel to compare revisions, inspect rollout history, and verify that evaluation coverage exists before publishing changes.
            </p>
          </Card>
        </div>
      </DetailRoutePage>
    );
  }

  if (section === "workflow-runs" && child) {
    return (
      <Section
        eyebrow="Workflow runs"
        title={`Run ${child}`}
        description="Follow live execution, inspect approval waits, and keep logs, tool calls, and status transitions visible in one operations-first split view."
        actions={
          <Button asChild href="/app/workflows/wf_customer_onboarding_v12" variant="secondary">
            <ArrowRight className="size-4" />
            Open workflow
          </Button>
        }
      >
        <div className="space-y-6">
          <Card className="p-5">
            <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Self-improvement</p>
            <p className="mt-2 text-sm text-muted">
              Reflect extracts lessons (auto-runs on terminal states server-side too). Propose opens a sandbox DNA variant only.
            </p>
            <div className="mt-4">
              <ImproveRunButton runId={child} />
            </div>
          </Card>
          <WorkflowRunConsole runId={child} initialEvents={workflowRunEvents} />
        </div>
      </Section>
    );
  }

  if (section === "evolution") {
    return (
      <Section
        eyebrow="Evolution"
        title="Population archive"
        description="DGM-lite archive of sandbox variants ranked by fitness. Evaluate and canary without silent production mutation. Lesson utility feeds coevolution ALC fitness."
      >
        <Card className="p-6">
          <EvolutionArchivePanel />
        </Card>
        <Card className="mt-4 p-6">
          <LessonUtilityPanel />
        </Card>
      </Section>
    );
  }

  if (section === "approvals") {
    if (!child) {
      return (
        <ListRoutePage
          eyebrow="Approvals"
          title="Approval review queue"
          description="Resolve human decision gates with clear risk posture, workflow context, and an audit-ready explanation before the run proceeds."
          rows={approvals}
          columns={[
            { key: "title", label: "Request" },
            { key: "workflow", label: "Workflow" },
            { key: "requester", label: "Requester" },
            { key: "risk", label: "Risk" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "createdAt",
              label: "Created",
              render: (row) => formatDateTime(row.createdAt),
            },
          ]}
          metrics={[
            { label: "Pending", value: String(approvals.filter((item) => item.status === "pending").length), delta: "Still waiting for human action" },
            { label: "High risk", value: String(approvals.filter((item) => item.risk === "High" || item.risk === "Critical").length), delta: "Need careful reviewer attention" },
            { label: "Approved", value: String(approvals.filter((item) => item.status === "approved").length), delta: "Decisions already completed" },
            { label: "Linked workflows", value: String(new Set(approvals.map((item) => item.workflow)).size), delta: "Decision coverage across multiple flows" },
          ]}
          searchPlaceholder="Search approvals by workflow, risk, requester, or state"
          emptyTitle="No approvals need review"
          emptyDescription="Everything is moving automatically right now."
        />
      );
    }

    const approval = approvals.find((item) => item.id === child);
    if (!approval) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Approvals"
        title={approval.title}
        description="Review the reasoning, risk indicators, and downstream effect before you approve or reject this gated workflow action."
        status={approval.status}
        metadata={[
          { label: "Workflow", value: approval.workflow },
          { label: "Requester", value: approval.requester },
          { label: "Risk", value: approval.risk },
          { label: "Created", value: formatDateTime(approval.createdAt) },
        ]}
        actions={
          <Button asChild href="/app/workflow-runs/run_01" variant="secondary">
            <ArrowRight className="size-4" />
            View related run
          </Button>
        }
      >
        <div className="grid gap-6 xl:grid-cols-[1.05fr_0.95fr]">
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Decision context</h2>
            <p className="mt-3 leading-7 text-muted">{approval.reason}</p>
          </Card>
          <ApprovalDecisionPanel approvalId={child} />
        </div>
      </DetailRoutePage>
    );
  }

  if (section === "knowledge") {
    if (!child) {
      return (
        <HubCards
          eyebrow="Knowledge"
          title="Knowledge operations center"
          description="Track connected sources, freshness, failures, and the search surface that powers grounded workflow decisions."
          metrics={[
            { label: "Sources", value: String(knowledgeSources.length), delta: "Connected to multiple systems of record" },
            { label: "Documents", value: String(knowledgeDocuments.length), delta: "Indexed into the searchable corpus" },
            { label: "Failures", value: String(knowledgeDocuments.filter((item) => item.status === "failed").length), delta: "Need remediation or re-index" },
            { label: "Healthy", value: String(knowledgeSources.filter((item) => item.status === "connected").length), delta: "Sources in good standing" },
          ]}
          cards={[
            {
              href: "/app/knowledge/sources",
              title: "Knowledge sources",
              description: "Inspect connections, sync posture, and source-specific indexing errors.",
            },
            {
              href: "/app/knowledge/documents",
              title: "Indexed documents",
              description: "Review document freshness, source attribution, and failure states.",
            },
            {
              href: "/app/knowledge/search",
              title: "Knowledge search",
              description: "Search the curated corpus with citation-friendly context and source badges.",
            },
          ]}
        />
      );
    }

    if (child === "sources" && !grandchild) {
      return (
        <ListRoutePage
          eyebrow="Knowledge"
          title="Knowledge sources"
          description="Manage source connectivity, last sync times, indexing quality, and the operational freshness of each upstream knowledge system."
          rows={knowledgeSources}
          columns={[
            { key: "name", label: "Source" },
            { key: "type", label: "Type" },
            { key: "documentCount", label: "Documents" },
            { key: "errorCount", label: "Errors" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "lastSync",
              label: "Last sync",
              render: (row) => formatDateTime(row.lastSync),
            },
          ]}
          metrics={[
            { label: "Connected", value: String(knowledgeSources.filter((item) => item.status === "connected").length), delta: "Stable source integrations" },
            { label: "Indexing", value: String(knowledgeSources.filter((item) => item.status === "indexing").length), delta: "Currently refreshing content" },
            { label: "Failed", value: String(knowledgeSources.filter((item) => item.status === "failed").length), delta: "Require operator intervention" },
            { label: "Documents", value: String(knowledgeSources.reduce((total, item) => total + item.documentCount, 0)), delta: "Source-side document coverage" },
          ]}
          searchPlaceholder="Search knowledge sources by type, status, or source name"
          emptyTitle="No knowledge sources"
          emptyDescription="Add a source before the system can ground answers on organizational knowledge."
        />
      );
    }

    if (child === "sources" && grandchild) {
      const source = knowledgeSources.find((item) => item.id === grandchild);
      if (!source) {
        return <NotFoundPanel slug={slug} />;
      }

      return (
        <DetailRoutePage
          eyebrow="Knowledge"
          title={source.name}
          description="Inspect sync health, document volume, and source-specific remediation needs for this knowledge connector."
          status={source.status}
          metadata={[
            { label: "Type", value: source.type },
            { label: "Documents", value: String(source.documentCount) },
            { label: "Errors", value: String(source.errorCount) },
            { label: "Last sync", value: formatDateTime(source.lastSync) },
          ]}
        >
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Indexed document sample</h2>
            <DataTable
              caption="Knowledge documents"
              rows={knowledgeDocuments}
              columns={[
                { key: "title", label: "Document" },
                { key: "source", label: "Source" },
                {
                  key: "status",
                  label: "Status",
                  render: (row) => <StatusBadge status={row.status} />,
                },
              ]}
            />
          </Card>
        </DetailRoutePage>
      );
    }

    if (child === "documents" && !grandchild) {
      return (
        <ListRoutePage
          eyebrow="Knowledge"
          title="Indexed documents"
          description="Inspect the current document corpus, track failures, and verify that sources stay fresh enough for grounded automation."
          rows={knowledgeDocuments}
          columns={[
            { key: "title", label: "Document" },
            { key: "source", label: "Source" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "updatedAt",
              label: "Updated",
              render: (row) => formatDateTime(row.updatedAt),
            },
          ]}
          metrics={[
            { label: "Indexed", value: String(knowledgeDocuments.filter((item) => item.status === "indexed").length), delta: "Available to search and retrieval flows" },
            { label: "Failed", value: String(knowledgeDocuments.filter((item) => item.status === "failed").length), delta: "Require ingestion attention" },
            { label: "Sources", value: String(new Set(knowledgeDocuments.map((item) => item.source)).size), delta: "Documents arrive from multiple systems" },
            { label: "Freshness", value: "Hourly", delta: "Demo posture for the search index" },
          ]}
          searchPlaceholder="Search indexed documents by title, source, or ingestion state"
          emptyTitle="No indexed documents"
          emptyDescription="Connect sources and finish indexing to populate this view."
        />
      );
    }

    if (child === "documents" && grandchild) {
      const document = knowledgeDocuments.find((item) => item.id === grandchild);
      if (!document) {
        return <NotFoundPanel slug={slug} />;
      }

      return (
        <DetailRoutePage
          eyebrow="Knowledge"
          title={document.title}
          description="Review source attribution, freshness, indexing outcome, and a citation-friendly snippet before using the document in operations."
          status={document.status}
          metadata={[
            { label: "Source", value: document.source },
            { label: "Updated", value: formatDateTime(document.updatedAt) },
            { label: "Document ID", value: document.id },
            { label: "Usage", value: "Ready for retrieval and review" },
          ]}
        >
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Indexed snippet</h2>
            <p className="mt-3 leading-7 text-muted">{document.snippet}</p>
          </Card>
        </DetailRoutePage>
      );
    }

    if (child === "search") {
      return (
        <Section
          eyebrow="Knowledge"
          title="Search indexed knowledge"
          description="Search across the current knowledge corpus with source attribution and enough context to explain why a result was returned."
        >
          <SearchInput placeholder="Search knowledge by phrase, source, or policy topic" />
          <div className="grid gap-5">
            {knowledgeDocuments.map((document) => (
              <Card key={document.id} className="p-6">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="text-lg font-semibold text-white">{document.title}</p>
                    <p className="mt-1 text-sm text-muted">{document.source}</p>
                  </div>
                  <StatusBadge status={document.status} />
                </div>
                <p className="mt-4 leading-7 text-muted">{document.snippet}</p>
              </Card>
            ))}
          </div>
        </Section>
      );
    }
  }

  if (section === "memory") {
    if (!child) {
      return (
        <ListRoutePage
          eyebrow="Memory"
          title="Memory inspection surface"
          description="Inspect memory records, sensitivity posture, and recency before you depend on them for agent reasoning."
          rows={memoryItems}
          columns={[
            { key: "title", label: "Memory item" },
            { key: "scope", label: "Scope" },
            { key: "sensitivity", label: "Sensitivity" },
            {
              key: "lastUsed",
              label: "Last used",
              render: (row) => formatDateTime(row.lastUsed),
            },
            {
              key: "createdAt",
              label: "Created",
              render: (row) => formatDateTime(row.createdAt),
            },
          ]}
          metrics={[
            { label: "Total items", value: String(memoryItems.length), delta: "Current accessible memory records" },
            { label: "Restricted", value: String(memoryItems.filter((item) => item.sensitivity === "restricted").length), delta: "Backend redaction still applies" },
            { label: "Org scope", value: String(memoryItems.filter((item) => item.scope === "organization").length), delta: "Broadly shareable within the org" },
            { label: "Recent", value: String(memoryItems.filter((item) => item.lastUsed.startsWith("2026-07-07")).length), delta: "Used during recent runs" },
          ]}
          searchPlaceholder="Search memory by scope, sensitivity, or recency"
          emptyTitle="No memory records"
          emptyDescription="Memory will appear once agents start storing reusable context."
        />
      );
    }

    const memory = memoryItems.find((item) => item.id === child);
    if (!memory) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Memory"
        title={memory.title}
        description="Inspect the current preview, sensitivity posture, and lifecycle metadata for this stored memory record."
        metadata={[
          { label: "Scope", value: memory.scope },
          { label: "Sensitivity", value: memory.sensitivity },
          { label: "Created", value: formatDateTime(memory.createdAt) },
          { label: "Last used", value: formatDateTime(memory.lastUsed) },
        ]}
      >
        <Card className="p-6">
          <h2 className="text-lg font-semibold text-white">Preview</h2>
          <p className="mt-3 leading-7 text-muted">{memory.preview}</p>
        </Card>
      </DetailRoutePage>
    );
  }

  if (section === "evaluations") {
    if (!child) {
      return (
        <ListRoutePage
          eyebrow="Evaluations"
          title="Evaluation center"
          description="Track quality gates, regression posture, and recent evaluation runs before workflows are promoted or expanded."
          rows={evaluations}
          columns={[
            { key: "name", label: "Suite" },
            { key: "target", label: "Target" },
            { key: "score", label: "Score" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "updatedAt",
              label: "Updated",
              render: (row) => formatDateTime(row.updatedAt),
            },
          ]}
          metrics={[
            { label: "Suites", value: String(evaluations.length), delta: "Current tracked evaluation surfaces" },
            { label: "Passes", value: String(evaluations.filter((item) => item.status === "passed").length), delta: "Healthy quality posture" },
            { label: "Warnings", value: String(evaluations.filter((item) => item.status === "warning").length), delta: "Need investigation before release" },
            { label: "Average score", value: "0.88", delta: "Current demo baseline" },
          ]}
          actions={
            <Button variant="secondary">
              <Play className="size-4" />
              Run evaluation
            </Button>
          }
          searchPlaceholder="Search evaluation suites by target, score, or status"
          emptyTitle="No evaluation suites"
          emptyDescription="Add evaluation coverage before promoting higher-risk workflows."
        />
      );
    }

    if (child === "runs" && grandchild) {
      const evaluationRun =
        evaluations.find((item) => item.id === grandchild) ??
        evaluations[0];

      return (
        <DetailRoutePage
          eyebrow="Evaluations"
          title={`${evaluationRun.name} run`}
          description="Inspect the latest evaluation outcome, score posture, and what this run means for workflow release confidence."
          status={evaluationRun.status}
          metadata={[
            { label: "Target", value: evaluationRun.target },
            { label: "Score", value: evaluationRun.score },
            { label: "Updated", value: formatDateTime(evaluationRun.updatedAt) },
            { label: "Run ID", value: grandchild },
          ]}
        >
          <Card className="p-6">
            <h2 className="text-lg font-semibold text-white">Failure analysis</h2>
            <p className="mt-3 leading-7 text-muted">
              Use this view to list failing cases, regression diffs, and release-blocking risks before a workflow is promoted.
            </p>
          </Card>
        </DetailRoutePage>
      );
    }

    const evaluation = evaluations.find((item) => item.id === child);
    if (!evaluation) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Evaluations"
        title={evaluation.name}
        description="Inspect the target, score, and recent quality posture for this evaluation suite."
        status={evaluation.status}
        metadata={[
          { label: "Target", value: evaluation.target },
          { label: "Score", value: evaluation.score },
          { label: "Updated", value: formatDateTime(evaluation.updatedAt) },
          { label: "Suite ID", value: evaluation.id },
        ]}
        actions={
          <Button asChild href={`/app/evaluations/runs/${evaluation.id}`} variant="secondary">
            <ArrowRight className="size-4" />
            Open latest run
          </Button>
        }
      >
        <Card className="p-6">
          <h2 className="text-lg font-semibold text-white">Quality gate summary</h2>
          <p className="mt-3 leading-7 text-muted">
            Promote workflows only when this suite remains healthy and critical regressions stay resolved.
          </p>
        </Card>
      </DetailRoutePage>
    );
  }

  if (section === "processes") {
    if (!child) {
      return (
        <ListRoutePage
          eyebrow="Processes"
          title="Process monitoring"
          description="Track backend jobs, long-running tasks, and operational progress for indexing, evaluation, and automation support routines."
          rows={processes}
          columns={[
            { key: "name", label: "Process" },
            { key: "type", label: "Type" },
            { key: "duration", label: "Duration" },
            { key: "progress", label: "Progress" },
            {
              key: "status",
              label: "Status",
              render: (row) => <StatusBadge status={row.status} />,
            },
            {
              key: "startedAt",
              label: "Started",
              render: (row) => formatDateTime(row.startedAt),
            },
          ]}
          metrics={[
            { label: "Running", value: String(processes.filter((item) => item.status === "running").length), delta: "Active backend workstreams" },
            { label: "Succeeded", value: String(processes.filter((item) => item.status === "succeeded").length), delta: "Completed successfully" },
            { label: "Retrying", value: "0", delta: "No demo retries in progress" },
            { label: "Coverage", value: String(new Set(processes.map((item) => item.type)).size), delta: "Distinct process categories" },
          ]}
          searchPlaceholder="Search processes by type, status, or execution owner"
          emptyTitle="No processes running"
          emptyDescription="Background jobs will appear here when backend tasks are active."
        />
      );
    }

    const process = processes.find((item) => item.id === child);
    if (!process) {
      return <NotFoundPanel slug={slug} />;
    }

    return (
      <DetailRoutePage
        eyebrow="Processes"
        title={process.name}
        description="Inspect lifecycle state, progress, and why this process matters for the overall automation platform."
        status={process.status}
        metadata={[
          { label: "Type", value: process.type },
          { label: "Started", value: formatDateTime(process.startedAt) },
          { label: "Duration", value: process.duration },
          { label: "Progress", value: process.progress },
        ]}
      >
        <Card className="p-6">
          <h2 className="text-lg font-semibold text-white">Operational summary</h2>
          <p className="mt-3 leading-7 text-muted">
            Processes connect runtime work such as indexing and evaluation to the visible health of the broader operations system.
          </p>
        </Card>
      </DetailRoutePage>
    );
  }

  if (section === "audit-logs") {
    return (
      <ListRoutePage
        eyebrow="Security"
        title="Audit log explorer"
        description="Review immutable activity history for security, approvals, authentication, and runtime changes across the system."
        rows={auditLogs}
        columns={[
          { key: "action", label: "Action" },
          { key: "actor", label: "Actor" },
          { key: "resource", label: "Resource" },
          {
            key: "status",
            label: "Status",
            render: (row) => <StatusBadge status={row.status} />,
          },
          {
            key: "createdAt",
            label: "Created",
            render: (row) => formatDateTime(row.createdAt),
          },
        ]}
        metrics={[
          { label: "Events", value: String(auditLogs.length), delta: "Recent entries loaded into the explorer" },
          { label: "Actors", value: String(new Set(auditLogs.map((item) => item.actor)).size), delta: "Distinct human or machine actors" },
          { label: "Success", value: String(auditLogs.filter((item) => item.status === "success").length), delta: "Events completed without issue" },
          { label: "Security", value: "Read-only", delta: "Frontend does not mutate audit history" },
        ]}
        searchPlaceholder="Search audit logs by actor, action, resource, or date"
        emptyTitle="No audit entries"
        emptyDescription="Audit records will appear here once the backend emits runtime activity."
      >
        <Card className="p-6">
          <p className="text-sm leading-7 text-muted">
            This scaffold keeps audit history read-only and emphasizes search, filters, and export controls rather than mutation.
          </p>
        </Card>
      </ListRoutePage>
    );
  }

  if (section === "settings") {
    if (!child) {
      return (
        <HubCards
          eyebrow="Admin"
          title="Settings hub"
          description="Navigate organization controls, security posture, user access, masked credentials, and integration management from one administrative surface."
          metrics={[
            { label: "Users", value: String(userRows.length), delta: "Tracked within the workspace" },
            { label: "API keys", value: String(apiKeys.length), delta: "Masked credentials under review" },
            { label: "Security alerts", value: "2", delta: "Illustrative policy attention points" },
            { label: "Billing", value: env.enableBilling ? "Enabled" : "Disabled", delta: "Feature availability for this environment" },
          ]}
          cards={[
            { href: "/app/settings/organization", title: "Organization", description: "Brand, locale, and retention posture." },
            { href: "/app/settings/users", title: "Users", description: "Roles, invitations, and access state." },
            { href: "/app/settings/roles", title: "Roles", description: "Permission matrix and responsibility boundaries." },
            { href: "/app/settings/billing", title: "Billing", description: "Commercial plan and invoicing posture." },
            { href: "/app/settings/api-keys", title: "API keys", description: "Machine credentials with masked display rules." },
            { href: "/app/settings/security", title: "Security", description: "Session, MFA, and allowed-domain controls." },
            { href: "/app/settings/integrations", title: "Integrations", description: "Connected systems and automation endpoints." },
            { href: "/app/settings/profile", title: "Profile", description: "Personal identity and notification preferences." },
          ]}
        />
      );
    }

    if (child === "organization") {
      return (
        <Section
          eyebrow="Settings"
          title="Organization settings"
          description="Manage organization identity and defaults. Saves call the backend organization PATCH API; authorization stays server-side."
        >
          <OrganizationSettingsForm />
        </Section>
      );
    }

    if (child === "users") {
      return (
        <Section
          eyebrow="Settings"
          title="User management"
          description="Invite collaborators, disable access, and track who participates in governed workflow operations."
        >
          <UserAdminPanel initialRows={userRows} />
        </Section>
      );
    }

    if (child === "roles") {
      return (
        <Section
          eyebrow="Settings"
          title="Role matrix"
          description="Review the responsibility boundaries that shape who can read, approve, update, or audit automation assets."
        >
          <div className="grid gap-5 md:grid-cols-2">
            {roleMatrix.map((role) => (
              <Card key={role.id} className="p-6">
                <p className="text-lg font-semibold text-white">{role.role}</p>
                <p className="mt-2 text-sm text-[var(--accent)]">{role.focus}</p>
                <p className="mt-4 leading-7 text-muted">{role.permissions}</p>
              </Card>
            ))}
          </div>
        </Section>
      );
    }

    if (child === "billing") {
      return (
        <Section
          eyebrow="Settings"
          title="Billing"
          description="Inspect subscription posture, plan notes, and operational ownership for commercial controls."
        >
          {env.enableBilling ? (
            <Card className="p-6">
              <p className="text-lg font-semibold text-white">Billing enabled</p>
              <p className="mt-3 leading-7 text-muted">
                This scaffold reserves space for plan tier, invoice history, spend limits, and billing manager workflows.
              </p>
            </Card>
          ) : (
            <EmptyState
              title="Billing is disabled"
              description="This environment does not expose billing controls yet. Keep a placeholder visible so routing remains complete."
            />
          )}
        </Section>
      );
    }

    if (child === "api-keys") {
      return (
        <Section
          eyebrow="Settings"
          title="API key management"
          description="Provision machine credentials safely, keep full values one-time only, and make revoke actions explicit and auditable."
          actions={
            <Button>
              <FileKey2 className="size-4" />
              Create key
            </Button>
          }
        >
          <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <ApiKeyTable rows={apiKeys} />
            <Card className="p-6">
              <p className="text-lg font-semibold text-white">Security rules</p>
              <ul className="mt-4 space-y-3 text-sm leading-7 text-muted">
                <li>Show the full key only once after creation.</li>
                <li>Mask stored keys on every subsequent render.</li>
                <li>Confirm revoke actions before they execute.</li>
                <li>Surface scope and last-used context for reviewers.</li>
              </ul>
            </Card>
          </div>
        </Section>
      );
    }

    if (child === "security") {
      return (
        <FormRoutePage
          eyebrow="Settings"
          title="Security settings"
          description="Control session posture, MFA expectations, domain restrictions, and other organization-level security defaults."
          mutationKind="settings"
          sections={[
            {
              title: "Authentication safeguards",
              description: "Strengthen who can sign in and what additional checks are required.",
              fields: ["MFA requirement", "Password policy", "Session timeout", "Suspicious login alerts"],
            },
            {
              title: "Workspace controls",
              description: "Set domain and export guardrails for a high-trust operating model.",
              fields: ["Allowed domains", "SSO mode", "Audit export", "Support override process"],
            },
          ]}
          draftLabel="Reset"
          submitLabel="Save security settings"
          notes={[
            "High-risk changes should require stronger human confirmation.",
            "Frontend route protection remains UX-only; backend authorization is final.",
            "Security changes should preserve clear audit visibility.",
          ]}
        />
      );
    }

    if (child === "integrations") {
      return (
        <HubCards
          eyebrow="Settings"
          title="Integration settings"
          description="Review external system posture, credential expectations, and which downstream workflows depend on each integration."
          metrics={[
            { label: "Connected tools", value: String(tools.filter((item) => item.status === "connected").length), delta: "Healthy operational integrations" },
            { label: "Errors", value: String(tools.filter((item) => item.status === "error").length), delta: "Need operator remediation" },
            { label: "Automation endpoints", value: String(integrationCards.length), delta: "Key integration surfaces tracked here" },
            { label: "Secrets", value: "Masked", delta: "Never exposed in browser views" },
          ]}
          cards={integrationCards}
        />
      );
    }

    if (child === "profile") {
      return (
        <FormRoutePage
          eyebrow="Settings"
          title="Profile"
          description="Manage personal identity details, notification posture, and how you appear in audit and approval trails."
          mutationKind="settings"
          sections={[
            {
              title: "Identity",
              description: "The basics that teammates see in workflows, reviews, and audit records.",
              fields: ["Display name", "Email", "Job title", "Timezone"],
            },
            {
              title: "Preferences",
              description: "Tune how operational events reach you across notification channels.",
              fields: ["Approval alerts", "Run failure alerts", "Digest schedule", "On-call preference"],
            },
          ]}
          draftLabel="Discard"
          submitLabel="Save profile"
          notes={[
            "Use backend validation for identity changes and email ownership.",
            "Preference changes should not bypass organization security policy.",
            "Notification posture should remain easy to audit for critical roles.",
          ]}
        />
      );
    }
  }

  return <NotFoundPanel slug={slug} />;
}
