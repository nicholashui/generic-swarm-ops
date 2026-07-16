import { ArrowRight, FileKey2, Play, Plus, ShieldAlert } from "lucide-react";
import { DetailMetadata } from "@/components/domain/detail-metadata";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { DataTable } from "@/components/ui/data-table";
import { MetricCard } from "@/components/ui/metric-card";
import { Section } from "@/components/ui/section";
import { StatusBadge } from "@/components/ui/status-badge";
import { loadProductSlice, productSlicesForRoute } from "@/lib/data/product-data";
import { formatDateTime } from "@/lib/formatting/dates";

export default async function DashboardPage() {
  const {
    approvals,
    auditLogs,
    dashboardMetrics,
    knowledgeDocuments,
    onboardingChecklist,
    processes,
    workflows,
  } = await loadProductSlice(productSlicesForRoute(undefined));
  return (
    <Section
      eyebrow="Operations"
      title="Governed automation command surface"
      description="Track workflow execution, review approvals, inspect knowledge freshness, and keep security posture visible from one shared dashboard."
      actions={
        <>
          <Button asChild href="/app/agents/new">
            <Plus className="size-4" />
            Create agent
          </Button>
          <Button asChild href="/app/workflows/new" variant="secondary">
            <Play className="size-4" />
            Create workflow
          </Button>
        </>
      }
    >
      <div className="grid gap-4 xl:grid-cols-4">
        {dashboardMetrics.map((metric) => (
          <MetricCard
            key={metric.label}
            delta={metric.delta}
            label={metric.label}
            value={metric.value}
          />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card className="p-6">
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">
            Onboarding checklist
          </p>
          <div className="mt-5 grid gap-3 md:grid-cols-2">
            {onboardingChecklist.map((step, index) => (
              <div
                key={step}
                className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white"
              >
                <span className="mr-3 text-[var(--accent-2)]">{String(index + 1).padStart(2, "0")}</span>
                {step}
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-6">
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Posture summary</p>
          <div className="mt-4 space-y-4">
            <DetailMetadata
              items={[
                { label: "Pending approvals", value: String(approvals.filter((item) => item.status === "pending").length) },
                { label: "Failed knowledge docs", value: String(knowledgeDocuments.filter((item) => item.status === "failed").length) },
                { label: "Running processes", value: String(processes.filter((item) => item.status === "running").length) },
                { label: "Live workflows", value: String(workflows.filter((item) => item.status === "active").length) },
              ]}
            />
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <p className="font-semibold text-white">Fallback design workflow</p>
              <p className="mt-2 leading-7 text-muted">
                Major page layouts use the documented fallback described in `frontend/docs/design/open-design-reference.md`
                because the required OpenDesign MCP server is not available in this workspace.
              </p>
            </div>
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <Card className="p-6">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Approvals queue</p>
              <h2 className="mt-2 text-lg font-semibold text-white">Human gates requiring attention</h2>
            </div>
            <Button asChild href="/app/approvals" variant="ghost">
              Review queue
              <ArrowRight className="size-4" />
            </Button>
          </div>
          <div className="mt-5">
            <DataTable
              caption="Pending approvals"
              rows={approvals}
              columns={[
                { key: "title", label: "Request" },
                { key: "risk", label: "Risk" },
                { key: "workflow", label: "Workflow" },
                {
                  key: "status",
                  label: "Status",
                  render: (row) => <StatusBadge status={row.status} />,
                },
              ]}
            />
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3">
            <ShieldAlert className="size-5 text-[var(--warning)]" />
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Security feed</p>
              <h2 className="mt-2 text-lg font-semibold text-white">Recent audit and key activity</h2>
            </div>
          </div>
          <div className="mt-5 space-y-4">
            {auditLogs.map((entry) => (
              <div key={entry.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-medium text-white">{entry.action}</p>
                    <p className="mt-1 text-sm text-muted">{entry.actor}</p>
                  </div>
                  <StatusBadge status={entry.status} />
                </div>
                <p className="mt-3 font-[var(--font-mono)] text-xs text-[var(--accent-2)]">
                  {formatDateTime(entry.createdAt)}
                </p>
              </div>
            ))}
            <Button asChild href="/app/settings/api-keys" variant="secondary">
              <FileKey2 className="size-4" />
              Open API key controls
            </Button>
          </div>
        </Card>
      </div>
    </Section>
  );
}
