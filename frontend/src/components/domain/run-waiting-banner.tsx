"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";

export function RunWaitingBanner({ runId }: { runId: string }) {
  const [approvalId, setApprovalId] = useState<string | null>(null);
  const [nodeId, setNodeId] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (env.demoMode) return;
      try {
        const run = (await backendApi.getWorkflowRun(runId)) as {
          status?: string;
          approval_request_id?: string;
          current_step?: string;
        };
        if (cancelled) return;
        setStatus(run.status || null);
        setApprovalId(run.approval_request_id || null);
        setNodeId(run.current_step || null);
      } catch {
        /* ignore */
      }
    }
    void load();
    const t = setInterval(() => void load(), 4000);
    return () => {
      cancelled = true;
      clearInterval(t);
    };
  }, [runId]);

  if (status !== "waiting_for_approval" || !approvalId) return null;

  return (
    <div className="rounded-[20px] border border-amber-400/30 bg-amber-500/10 px-4 py-3 text-sm text-amber-50">
      Waiting for human gate
      {nodeId ? (
        <>
          {" "}
          on node <span className="font-semibold text-white">{nodeId}</span>
        </>
      ) : null}
      .{" "}
      <Link className="underline underline-offset-2" href={`/app/approvals/${approvalId}`}>
        Review approval →
      </Link>
    </div>
  );
}
