"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Play } from "lucide-react";
import { Button } from "@/components/ui/button";
import { backendApi } from "@/lib/api/client";
import { buildWorkflowRunPayload } from "@/lib/api/workflow-run-payload";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

export function RunWorkflowButton({
  workflowId,
  inputSchema,
  defaultEngine,
}: {
  workflowId: string;
  /** Optional schema so required fields (case_id, …) are filled for live runs */
  inputSchema?: {
    type?: string;
    required?: string[];
    properties?: Record<string, { type?: string; default?: unknown }>;
  } | null;
  /** Prefer workflow.execution_engine when set */
  defaultEngine?: string;
}) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [engine, setEngine] = useState(defaultEngine || "langgraph");

  async function onRun() {
    setError(null);
    setBusy(true);
    try {
      const payload = buildWorkflowRunPayload(
        { id: workflowId, input_schema: inputSchema },
        { triggered_from: "frontend_run_now" },
      );
      if (env.demoMode) {
        setResult({ demo: true, workflowId, status: "queued", engine, input_payload: payload });
        return;
      }
      let run = (await backendApi.startWorkflowRun(workflowId, payload, engine)) as Record<
        string,
        unknown
      >;
      const runId = String(run.id || "");
      try {
        await backendApi.dispatchWorkflowRuns();
        if (runId) {
          const refreshed = (await backendApi.getWorkflowRun(runId).catch(() => null)) as Record<
            string,
            unknown
          > | null;
          if (refreshed) run = refreshed;
        }
      } catch {
        /* keep queued */
      }
      setResult(run);
      if (runId) router.push(`/app/workflow-runs/${runId}`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="inline-flex flex-col items-start gap-2">
      <label className="flex items-center gap-2 text-[11px] text-muted">
        Engine
        <select
          className="rounded-lg border border-white/10 bg-black/40 px-2 py-1 text-xs text-white"
          value={engine}
          onChange={(e) => setEngine(e.target.value)}
          data-testid="run-engine"
        >
          <option value="langgraph">langgraph</option>
          <option value="legacy">legacy</option>
        </select>
      </label>
      <Button data-testid="run-now" disabled={busy} onClick={() => void onRun()}>
        <Play className="size-4" />
        {busy ? "Starting…" : "Run now"}
      </Button>
      {error ? (
        <p className="text-xs text-[var(--danger)]" data-testid="run-now-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre
          data-testid="run-now-result"
          className="max-w-md overflow-x-auto rounded-xl bg-black/30 p-2 text-[10px] text-[var(--accent-2)]"
        >
          {JSON.stringify(result)}
        </pre>
      ) : null}
    </div>
  );
}
