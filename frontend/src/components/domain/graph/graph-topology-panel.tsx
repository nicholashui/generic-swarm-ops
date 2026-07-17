"use client";

import { useEffect, useState } from "react";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";

type TopoNode = {
  id: string;
  kind?: string;
  label?: string;
  agent_id?: string;
  human_gate?: boolean;
  status?: string;
};

type TopoEdge = { from: string; to: string; kind?: string };

type Topology = {
  pattern?: string;
  engine?: string;
  nodes?: TopoNode[];
  edges?: TopoEdge[];
};

export function GraphTopologyPanel({
  workflowId,
  runId,
}: {
  workflowId?: string;
  runId?: string;
}) {
  const [topo, setTopo] = useState<Topology | null>(null);
  const [graphState, setGraphState] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setError(null);
      try {
        if (env.demoMode) {
          setTopo({
            pattern: "pipeline",
            engine: "demo",
            nodes: [
              { id: "START", kind: "start" },
              { id: "step_a", kind: "step", label: "step_a" },
              { id: "END", kind: "end" },
            ],
            edges: [
              { from: "START", to: "step_a" },
              { from: "step_a", to: "END" },
            ],
          });
          return;
        }
        if (workflowId) {
          const t = (await backendApi.getWorkflowTopology(workflowId)) as Topology;
          if (!cancelled) setTopo(t);
        }
        if (runId) {
          const gs = (await backendApi.getWorkflowRunGraphState(runId)) as Record<string, unknown>;
          if (!cancelled) setGraphState(gs);
        }
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load topology");
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, [workflowId, runId]);

  const completed = new Set(
    ((graphState?.completed_step_ids as string[]) || []).filter(Boolean),
  );
  const current = (graphState?.current_step_id as string) || null;
  const engine = (graphState?.engine as string) || topo?.engine || "—";
  const pattern = (graphState?.pattern as string) || topo?.pattern || "pipeline";

  return (
    <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-sm font-semibold text-white">Orchestration graph</p>
        <p className="text-xs text-muted">
          engine={engine} · pattern={pattern}
        </p>
      </div>
      {error ? <p className="mt-3 text-sm text-[var(--danger)]">{error}</p> : null}
      {!topo ? (
        <p className="mt-3 text-sm text-muted">Loading topology…</p>
      ) : (
        <div className="mt-4 flex flex-wrap items-center gap-2">
          {(topo.nodes || [])
            .filter((n) => n.id !== "START" && n.id !== "END")
            .map((node) => {
              let tone = "border-white/15 bg-black/20 text-muted";
              if (completed.has(node.id)) tone = "border-emerald-400/40 bg-emerald-500/10 text-emerald-200";
              if (current === node.id) tone = "border-amber-400/50 bg-amber-500/15 text-amber-100";
              if (node.human_gate) tone += " ring-1 ring-fuchsia-400/30";
              return (
                <div
                  key={node.id}
                  className={`rounded-2xl border px-3 py-2 text-xs ${tone}`}
                  title={node.agent_id || node.kind || node.id}
                >
                  <div className="font-medium text-white">{node.label || node.id}</div>
                  <div className="mt-0.5 opacity-80">
                    {node.kind || "step"}
                    {node.human_gate ? " · gate" : ""}
                    {completed.has(node.id) ? " · done" : ""}
                    {current === node.id ? " · current" : ""}
                  </div>
                </div>
              );
            })}
        </div>
      )}
      {topo?.edges && topo.edges.length > 0 ? (
        <p className="mt-4 text-[11px] leading-5 text-muted">
          {topo.edges
            .slice(0, 12)
            .map((e) => `${e.from}→${e.to}`)
            .join(" · ")}
          {topo.edges.length > 12 ? " …" : ""}
        </p>
      ) : null}
    </div>
  );
}
