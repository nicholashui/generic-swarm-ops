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
}: {
  workflowId: string;
  /** Optional schema so required fields (case_id, …) are filled for live runs */
  inputSchema?: {
    type?: string;
    required?: string[];
    properties?: Record<string, { type?: string; default?: unknown }>;
  } | null;
}) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  async function onRun() {
    setError(null);
    setBusy(true);
    try {
      const payload = buildWorkflowRunPayload(
        { id: workflowId, input_schema: inputSchema },
        { triggered_from: "frontend_run_now" },
      );
      if (env.demoMode) {
        setResult({ demo: true, workflowId, status: "queued", input_payload: payload });
        return;
      }
      const run = (await backendApi.startWorkflowRun(workflowId, payload)) as Record<string, unknown>;
      setResult(run);
      const runId = String(run.id || "");
      if (runId) router.push(`/app/workflow-runs/${runId}`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="inline-flex flex-col items-start gap-2">
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
