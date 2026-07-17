"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";

type BackendDecision = {
  id?: string;
  status?: string;
  decision?: string;
  decision_reason?: string;
  [key: string]: unknown;
};

type ApprovalDetail = {
  id?: string;
  run_id?: string;
  workflow_id?: string;
  step_id?: string;
  graph_node_id?: string;
  engine?: string;
  risk_level?: string;
  status?: string;
  payload_preview?: Record<string, unknown>;
};

/**
 * LG-14: interrupt-aware decision panel with graph/node context.
 */
export function ApprovalDecisionPanel({ approvalId }: { approvalId?: string }) {
  const [decision, setDecision] = useState<string | null>(null);
  const [backendState, setBackendState] = useState<BackendDecision | null>(null);
  const [detail, setDetail] = useState<ApprovalDetail | null>(null);
  const [graphState, setGraphState] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [overrideJson, setOverrideJson] = useState("");

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (!approvalId || env.demoMode) return;
      try {
        const ap = (await backendApi.getApproval(approvalId)) as ApprovalDetail;
        if (cancelled) return;
        setDetail(ap);
        if (ap.run_id) {
          const gs = (await backendApi.getWorkflowRunGraphState(ap.run_id).catch(() => null)) as Record<
            string,
            unknown
          > | null;
          if (!cancelled && gs) setGraphState(gs);
        }
      } catch {
        /* legacy rows may still work without detail */
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, [approvalId]);

  async function submit(next: "approved" | "rejected") {
    setError(null);
    setBusy(true);
    try {
      if (overrideJson.trim()) {
        try {
          JSON.parse(overrideJson);
        } catch {
          throw new Error("Override JSON is invalid");
        }
        // Overrides are validated client-side; server resume uses approval decision only for now.
      }
      if (env.demoMode || !approvalId) {
        setDecision(next);
        setBackendState({ status: next, id: approvalId || "preview", decision: next, demo: true });
        return;
      }
      const result = (await backendApi.decideApproval(approvalId, next, `UI ${next}`)) as BackendDecision;
      setDecision(next);
      setBackendState(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Decision failed");
    } finally {
      setBusy(false);
    }
  }

  const nodeId = detail?.graph_node_id || detail?.step_id || (graphState?.current_step_id as string) || null;
  const engine = detail?.engine || (graphState?.engine as string) || "—";
  const runId = detail?.run_id;

  return (
    <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
      <p className="text-sm font-semibold text-white">Decision panel</p>
      <p className="mt-2 text-sm text-muted">
        High-risk actions require reviewer confirmation.
        {approvalId ? ` Approval: ${approvalId}` : " (no approval id — preview mode)"}
      </p>

      <div className="mt-4 space-y-2 rounded-2xl border border-white/10 bg-black/25 p-4 text-xs text-muted">
        <p>
          <span className="text-white/80">Engine:</span> {engine}
        </p>
        {nodeId ? (
          <p>
            <span className="text-white/80">Graph node:</span> {nodeId}
          </p>
        ) : null}
        {detail?.workflow_id ? (
          <p>
            <span className="text-white/80">Workflow:</span> {detail.workflow_id}
          </p>
        ) : null}
        {detail?.risk_level ? (
          <p>
            <span className="text-white/80">Risk:</span> {detail.risk_level}
          </p>
        ) : null}
        {detail?.payload_preview ? (
          <pre className="mt-2 max-h-32 overflow-auto rounded-xl bg-black/40 p-2 text-[10px] text-[var(--accent-2)]">
            {JSON.stringify(detail.payload_preview, null, 2)}
          </pre>
        ) : null}
        {runId ? (
          <p className="pt-1">
            <Link className="underline underline-offset-2" href={`/app/workflow-runs/${runId}`}>
              Open related run →
            </Link>
          </p>
        ) : null}
      </div>

      <label className="mt-4 block text-xs text-muted">
        Optional override JSON (validated client-side)
        <textarea
          className="mt-1 w-full rounded-xl border border-white/10 bg-black/30 p-2 font-mono text-[11px] text-white"
          rows={3}
          placeholder='{"note":"optional resume hint"}'
          value={overrideJson}
          onChange={(e) => setOverrideJson(e.target.value)}
        />
      </label>

      <div className="mt-5 flex flex-wrap gap-3">
        <Button disabled={busy} onClick={() => void submit("approved")}>
          Approve
        </Button>
        <Button disabled={busy} variant="danger" onClick={() => void submit("rejected")}>
          Reject
        </Button>
      </div>
      {error ? <p className="mt-4 text-sm text-[var(--danger)]">{error}</p> : null}
      {decision ? (
        <p className="mt-4 text-sm text-[var(--accent-2)]">
          Action: {decision}
          {backendState?.status ? ` · backend status: ${String(backendState.status)}` : ""}
          {backendState?.id ? ` · id: ${String(backendState.id)}` : ""}
          {runId && decision === "approved" ? (
            <>
              {" · "}
              <Link className="underline" href={`/app/workflow-runs/${runId}`}>
                return to run
              </Link>
            </>
          ) : null}
        </p>
      ) : null}
      {backendState ? (
        <pre className="mt-3 overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]">
          {JSON.stringify(backendState, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}
