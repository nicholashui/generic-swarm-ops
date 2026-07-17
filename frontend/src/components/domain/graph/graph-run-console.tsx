"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { GraphTopologyPanel } from "@/components/domain/graph/graph-topology-panel";
import { RunWaitingBanner } from "@/components/domain/run-waiting-banner";

type StreamEvent = {
  id?: string;
  type?: string;
  event?: string;
  nodeId?: string;
  step_id?: string;
  message?: string;
  timestamp?: string;
};

export function GraphRunConsole({ runId }: { runId: string }) {
  const [run, setRun] = useState<Record<string, unknown> | null>(null);
  const [events, setEvents] = useState<StreamEvent[]>([]);
  const [trajectory, setTrajectory] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (env.demoMode) {
      setRun({ id: runId, status: "demo", engine: "demo" });
      return;
    }
    try {
      const r = (await backendApi.getWorkflowRun(runId)) as Record<string, unknown>;
      setRun(r);
      const gs = (await backendApi.getWorkflowRunGraphState(runId).catch(() => null)) as Record<
        string,
        unknown
      > | null;
      if (gs?.trajectory) setTrajectory(gs.trajectory as Record<string, unknown>);
      else if (r.trajectory) setTrajectory(r.trajectory as Record<string, unknown>);
      try {
        const traj = (await backendApi.getWorkflowRunTrajectory(runId)) as {
          trajectory?: Record<string, unknown>;
        };
        if (traj?.trajectory) setTrajectory(traj.trajectory);
      } catch {
        /* optional */
      }
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load run");
    }
  }, [runId]);

  useEffect(() => {
    void refresh();
    const t = setInterval(() => void refresh(), 3000);
    return () => clearInterval(t);
  }, [refresh]);

  useEffect(() => {
    if (env.demoMode) return;
    let cancelled = false;
    async function pollEvents() {
      try {
        // Prefer stream endpoint as one-shot list via fetch (SSE body)
        // Poll graph-state messages as event proxy (SSE streaming is one-shot on some proxies)
        const gs = (await backendApi.getWorkflowRunGraphState(runId)) as {
          live?: { messages?: Array<Record<string, unknown>> };
          status?: string;
          current_step_id?: string;
        };
        if (cancelled) return;
        const msgs = gs?.live?.messages || [];
        if (msgs.length) {
          setEvents(
            msgs.slice(-40).map((m, i) => ({
              id: `m${i}`,
              type: String(m.role || "message"),
              message: String(m.content || m.to || JSON.stringify(m)),
              nodeId: m.step_id ? String(m.step_id) : m.to ? String(m.to) : undefined,
            })),
          );
        } else if (gs?.current_step_id) {
          setEvents([
            {
              id: "cur",
              type: "node",
              nodeId: String(gs.current_step_id),
              message: `status=${gs.status || ""}`,
            },
          ]);
        }
      } catch {
        /* stream optional */
      }
    }
    void pollEvents();
    const t = setInterval(() => void pollEvents(), 5000);
    return () => {
      cancelled = true;
      clearInterval(t);
    };
  }, [runId]);

  const status = String(run?.status || "…");
  const engine = String(run?.engine || "…");
  const pattern = String(run?.orchestration_pattern || "…");
  const workflowId = run?.workflow_id ? String(run.workflow_id) : undefined;

  return (
    <div className="space-y-4">
      <RunWaitingBanner runId={runId} />
      <div className="grid gap-3 rounded-[24px] border border-white/10 bg-white/5 p-5 sm:grid-cols-4">
        <div>
          <p className="text-[10px] uppercase tracking-widest text-muted">Status</p>
          <p className="mt-1 text-sm font-semibold text-white">{status}</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-widest text-muted">Engine</p>
          <p className="mt-1 text-sm font-semibold text-white">{engine}</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-widest text-muted">Pattern</p>
          <p className="mt-1 text-sm font-semibold text-white">{pattern}</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-widest text-muted">Workflow</p>
          <p className="mt-1 text-sm font-semibold text-white">
            {workflowId ? (
              <Link className="underline underline-offset-2" href={`/app/workflows/${workflowId}`}>
                {workflowId}
              </Link>
            ) : (
              "—"
            )}
          </p>
        </div>
      </div>
      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
      <GraphTopologyPanel workflowId={workflowId} runId={runId} />
      {trajectory ? (
        <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
          <p className="text-sm font-semibold text-white">Trajectory score</p>
          <pre className="mt-3 overflow-x-auto rounded-xl bg-black/30 p-3 text-[11px] text-[var(--accent-2)]">
            {JSON.stringify(trajectory, null, 2)}
          </pre>
        </div>
      ) : null}
      <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
        <p className="text-sm font-semibold text-white">Graph events</p>
        <ul className="mt-3 max-h-64 space-y-2 overflow-y-auto text-xs text-muted">
          {events.length === 0 ? (
            <li>No stream events yet.</li>
          ) : (
            events.map((e, i) => (
              <li key={e.id || i} className="rounded-lg border border-white/5 bg-black/20 px-2 py-1.5">
                <span className="text-white/90">{e.type || e.event}</span>
                {e.nodeId || e.step_id ? ` · ${e.nodeId || e.step_id}` : ""}
                {e.message ? ` — ${e.message}` : ""}
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}
