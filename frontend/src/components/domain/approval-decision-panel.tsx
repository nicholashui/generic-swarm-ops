"use client";

import { useState } from "react";
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

export function ApprovalDecisionPanel({ approvalId }: { approvalId?: string }) {
  const [decision, setDecision] = useState<string | null>(null);
  const [backendState, setBackendState] = useState<BackendDecision | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(next: "approved" | "rejected") {
    setError(null);
    setBusy(true);
    try {
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

  return (
    <div className="rounded-[24px] border border-white/10 bg-white/5 p-5">
      <p className="text-sm font-semibold text-white">Decision panel</p>
      <p className="mt-2 text-muted">
        High-risk actions require reviewer confirmation and surface backend request state on failure.
        {approvalId ? ` Approval: ${approvalId}` : " (no approval id — preview mode)"}
      </p>
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
