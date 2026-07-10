"use client";

import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { LogViewer } from "@/components/ui/log-viewer";
import { Timeline } from "@/components/ui/timeline";
import { useRealtimeRun } from "@/hooks/use-realtime-run";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";
import type { WorkflowRunEvent } from "@/types/domain";

type LifecycleAction = "retry" | "cancel" | "pause" | "resume" | "expire";

export function WorkflowRunConsole({
  runId,
  initialEvents,
}: {
  runId: string;
  initialEvents: WorkflowRunEvent[];
}) {
  const { connectionState, events } = useRealtimeRun(runId, initialEvents);
  const logLines = useMemo(
    () => events.map((event) => `${event.timestamp} :: ${event.type} :: ${JSON.stringify(event.payload)}`),
    [events],
  );
  const [actionState, setActionState] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<LifecycleAction | null>(null);

  async function runAction(kind: LifecycleAction) {
    setError(null);
    setBusy(kind);
    try {
      if (env.demoMode) {
        const demoStatus: Record<LifecycleAction, string> = {
          retry: "retry_queued",
          cancel: "cancelled",
          pause: "paused",
          resume: "running",
          expire: "expired",
        };
        setActionState({ demo: true, action: kind, runId, status: demoStatus[kind] });
        return;
      }
      let result: unknown;
      if (kind === "retry") result = await backendApi.retryWorkflowRun(runId);
      else if (kind === "cancel") result = await backendApi.cancelWorkflowRun(runId);
      else if (kind === "pause") result = await backendApi.pauseWorkflowRun(runId);
      else if (kind === "resume") result = await backendApi.resumeWorkflowRun(runId);
      else result = await backendApi.expireWorkflowRun(runId, "operator_expire");
      setActionState(result as Record<string, unknown>);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
      <div className="space-y-6">
        <Card className="p-5">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-muted">Realtime connection</p>
              <h2 className="mt-2 text-lg font-semibold text-white">Run {runId}</h2>
            </div>
            <Badge className="bg-white/8 text-white">{connectionState}</Badge>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            <Button
              variant="secondary"
              disabled={busy !== null}
              data-testid="run-retry"
              onClick={() => void runAction("retry")}
            >
              {busy === "retry" ? "Retrying…" : "Retry"}
            </Button>
            <Button
              variant="secondary"
              disabled={busy !== null}
              data-testid="run-pause"
              onClick={() => void runAction("pause")}
            >
              {busy === "pause" ? "Pausing…" : "Pause"}
            </Button>
            <Button
              variant="secondary"
              disabled={busy !== null}
              data-testid="run-resume"
              onClick={() => void runAction("resume")}
            >
              {busy === "resume" ? "Resuming…" : "Resume"}
            </Button>
            <Button
              variant="secondary"
              disabled={busy !== null}
              data-testid="run-expire"
              onClick={() => void runAction("expire")}
            >
              {busy === "expire" ? "Expiring…" : "Expire"}
            </Button>
            <Button
              variant="danger"
              disabled={busy !== null}
              data-testid="run-cancel"
              onClick={() => void runAction("cancel")}
            >
              {busy === "cancel" ? "Cancelling…" : "Cancel"}
            </Button>
          </div>
          {error ? (
            <p className="mt-3 text-sm text-[var(--danger)]" data-testid="run-action-error">
              {error}
            </p>
          ) : null}
          {actionState ? (
            <pre
              data-testid="run-action-result"
              className="mt-3 overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]"
            >
              {JSON.stringify(actionState, null, 2)}
            </pre>
          ) : null}
        </Card>
        <Timeline events={events} />
      </div>
      <div className="space-y-6">
        <Card className="p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-muted">Selected step details</p>
          <p className="mt-3 text-white">
            The split view keeps the timeline readable while surfacing tool calls, approval waits, and
            errors with operational clarity.
          </p>
        </Card>
        <Card className="p-5">
          <p className="text-xs uppercase tracking-[0.24em] text-muted">Live logs</p>
          <div className="mt-4">
            <LogViewer lines={logLines} />
          </div>
        </Card>
      </div>
    </div>
  );
}
