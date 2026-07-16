"use client";

import { useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { useWorkspaceHelpOptional } from "@/components/help/workspace-help-context";
import { backendApi } from "@/lib/api/client";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

export type DomainPackAgent = {
  id: string;
  name: string;
  status: string;
  domain_id?: string | null;
  domainId?: string | null;
  requires_alc?: boolean | null;
  requiresAlc?: boolean | null;
  alc_version?: string | null;
  alcVersion?: string | null;
  allowed_memory_scopes?: string[] | null;
  allowedMemoryScopes?: string[] | null;
  hooks?: { reflect?: boolean } | null;
  owner?: string;
  knowledgeAccess?: string;
};

function isAlcReady(agent: DomainPackAgent): boolean {
  const requires = agent.requires_alc ?? agent.requiresAlc;
  if (requires === false || requires == null) return true;
  const scopes = agent.allowed_memory_scopes ?? agent.allowedMemoryScopes ?? [];
  const version = agent.alc_version ?? agent.alcVersion;
  const reflect = agent.hooks?.reflect;
  const hasAgentScope = scopes.includes("agent") || scopes.includes("agent_memory");
  if (!version || !hasAgentScope) return false;
  if (reflect === false) return false;
  return true;
}

export function DomainPackPanel({ agents }: { agents: DomainPackAgent[] }) {
  const help = useWorkspaceHelpOptional();
  const domains = useMemo(() => {
    const set = new Set<string>();
    for (const a of agents) {
      const d = a.domain_id ?? a.domainId;
      if (d) set.add(d);
    }
    return ["all", ...Array.from(set).sort()];
  }, [agents]);

  const [domain, setDomain] = useState<string>("all");

  const filtered = useMemo(() => {
    if (domain === "all") return agents;
    return agents.filter((a) => (a.domain_id ?? a.domainId) === domain);
  }, [agents, domain]);

  const alcReadyCount = filtered.filter(isAlcReady).length;
  const packCount = domains.filter((d) => d !== "all").length;

  async function openAgentSpec(agent: DomainPackAgent) {
    const name = agent.name || agent.id;
    if (!help) return;
    help.openAgentSpecInPanel({
      agentId: agent.id,
      name,
      loading: true,
    });
    try {
      const data = await backendApi.getAgentSpec(agent.id);
      help.openAgentSpecInPanel({
        agentId: data.agent_id,
        name: data.name || name,
        path: data.path,
        source: (data as { source?: string }).source,
        markdown: data.markdown,
        loading: false,
      });
    } catch (err) {
      help.openAgentSpecInPanel({
        agentId: agent.id,
        name,
        loading: false,
        error: formatMutationError(err),
      });
    }
  }

  return (
    <Card className="space-y-4 p-5" data-testid="domain-pack-panel">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-muted">Domain packs</p>
          <h3 className="mt-1 text-lg font-semibold text-white">Roster by domain + ALC</h3>
          <p className="mt-1 text-sm text-muted">
            Multi-pack ops view — filter registered pack agents and ALC readiness (N1/N2). Click an
            agent name to open its{" "}
            <code className="text-[var(--accent-2)]">SPEC.md</code> in the right help panel.
          </p>
          <p className="mt-1 text-xs text-muted" data-testid="domain-pack-summary">
            {packCount} domain pack{packCount === 1 ? "" : "s"} · isolation: agent_id lessons + tool
            allow-list (N2)
          </p>
        </div>
        <label className="text-sm text-muted">
          Domain{" "}
          <select
            className="ml-2 rounded-md border border-white/10 bg-black/40 px-2 py-1 text-white"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
          >
            {domains.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="flex flex-wrap gap-4 text-sm text-muted">
        <span>Packs: {packCount}</span>
        <span>Shown: {filtered.length}</span>
        <span>ALC ready: {alcReadyCount}</span>
        <span>ALC gaps: {filtered.length - alcReadyCount}</span>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="text-xs uppercase tracking-wide text-muted">
            <tr>
              <th className="px-2 py-2">Agent</th>
              <th className="px-2 py-2">Domain</th>
              <th className="px-2 py-2">Status</th>
              <th className="px-2 py-2">ALC</th>
            </tr>
          </thead>
          <tbody>
            {filtered.slice(0, 50).map((agent) => {
              const d = agent.domain_id ?? agent.domainId ?? "—";
              const ready = isAlcReady(agent);
              return (
                <tr key={agent.id} className="border-t border-white/5">
                  <td className="px-2 py-2">
                    <button
                      type="button"
                      className="text-left font-medium text-[var(--accent)] underline-offset-2 hover:underline"
                      data-testid={`agent-spec-link-${agent.id}`}
                      title={`Open SPEC in right panel: ${agent.id}`}
                      onClick={() => void openAgentSpec(agent)}
                    >
                      {agent.name || agent.id}
                    </button>
                    <p className="mt-0.5 font-[var(--font-mono)] text-[10px] text-muted">{agent.id}</p>
                  </td>
                  <td className="px-2 py-2 text-muted">{d}</td>
                  <td className="px-2 py-2">
                    <StatusBadge status={agent.status} />
                  </td>
                  <td className="px-2 py-2">
                    <StatusBadge status={ready ? "active" : "draft"} />
                    <span className="ml-2 text-xs text-muted">{ready ? "ready" : "incomplete"}</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {filtered.length > 50 ? (
          <p className="mt-2 text-xs text-muted">Showing first 50 of {filtered.length} agents.</p>
        ) : null}
        {filtered.length === 0 ? (
          <p className="py-6 text-sm text-muted">
            No agents for this domain filter. Register a pack (Wave 1 API) or create agents with
            domain_id.
          </p>
        ) : null}
      </div>
    </Card>
  );
}
