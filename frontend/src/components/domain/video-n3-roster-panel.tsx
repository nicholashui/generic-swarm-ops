"use client";

import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

type N3Status = {
  roster_count?: number;
  standby_count?: number;
  registered_or_active?: number;
  dna_count?: number;
  n3_complete?: boolean;
  by_category?: Record<string, number>;
  process_coverage?: {
    total?: number;
    dna?: number;
    pack_linked?: number;
    va_only?: number;
  };
  orphans?: string[];
};

const DEMO_STATUS: N3Status = {
  roster_count: 114,
  standby_count: 114,
  registered_or_active: 114,
  dna_count: 14,
  n3_complete: true,
  by_category: {
    "1-ATL": 5,
    "9-Meta": 28,
    "10-Sup": 34,
  },
  process_coverage: { total: 30, dna: 24, pack_linked: 6, va_only: 0 },
  orphans: [],
};

async function fetchStatus(): Promise<N3Status> {
  if (env.demoMode) {
    return DEMO_STATUS;
  }
  return (await backendApi.videoN3Status()) as N3Status;
}

export function VideoN3RosterPanel() {
  const [status, setStatus] = useState<N3Status | null>(() => (env.demoMode ? DEMO_STATUS : null));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(!env.demoMode);

  useEffect(() => {
    if (env.demoMode) return;
    let cancelled = false;
    void (async () => {
      try {
        const data = await fetchStatus();
        if (cancelled) return;
        setStatus(data);
        setError(null);
        setLoading(false);
      } catch (err) {
        if (cancelled) return;
        setError(formatMutationError(err));
        setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const load = useCallback(async () => {
    try {
      const data = await fetchStatus();
      setStatus(data);
      setError(null);
      setLoading(false);
    } catch (err) {
      setError(formatMutationError(err));
      setLoading(false);
    }
  }, []);

  const cats = Object.entries(status?.by_category || {}).sort(([a], [b]) => a.localeCompare(b));
  const complete = Boolean(status?.n3_complete);

  return (
    <div className="space-y-4" data-testid="video-n3-roster">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Video N3</p>
          <p className="mt-1 text-sm text-muted">
            Full roster retention + process wiring — all 114 agents orchestrator-reachable.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <StatusBadge status={complete ? "completed" : "pending"} />
          <Button variant="secondary" onClick={() => void load()} data-testid="video-n3-refresh">
            Refresh
          </Button>
        </div>
      </div>
      {loading && !status ? <p className="text-sm text-muted">Loading N3 status…</p> : null}
      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-3">
          <p className="text-xs text-muted">Roster</p>
          <p className="text-xl font-semibold">{status?.roster_count ?? "—"}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted">Standby / registered</p>
          <p className="text-xl font-semibold">
            {status?.standby_count ?? "—"} / {status?.registered_or_active ?? "—"}
          </p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted">DNA workflows</p>
          <p className="text-xl font-semibold">{status?.dna_count ?? "—"}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted">Processes (dna / linked / va-only)</p>
          <p className="text-xl font-semibold">
            {status?.process_coverage?.dna ?? 0} / {status?.process_coverage?.pack_linked ?? 0} /{" "}
            {status?.process_coverage?.va_only ?? 0}
          </p>
        </Card>
      </div>
      {cats.length > 0 ? (
        <div className="flex flex-wrap gap-2 text-xs text-muted">
          {cats.map(([cat, n]) => (
            <span key={cat} className="rounded border border-white/10 px-2 py-1">
              {cat}: {n}
            </span>
          ))}
        </div>
      ) : null}
      {(status?.orphans || []).length > 0 ? (
        <p className="text-sm text-[var(--danger)]">Orphans: {(status?.orphans || []).join(", ")}</p>
      ) : (
        <p className="text-xs text-muted">No orphans · retention policy enforced (N3).</p>
      )}
    </div>
  );
}
