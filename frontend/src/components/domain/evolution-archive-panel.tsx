"use client";

import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

type ArchiveVariant = {
  id?: string;
  name?: string;
  status?: string;
  fitness?: number;
  base_workflow_id?: string;
  evaluation_result?: string;
  sandbox_only?: boolean;
};

type ArchiveState = {
  archive_size?: number;
  elite?: ArchiveVariant | null;
  variants?: ArchiveVariant[];
};

const DEMO_ARCHIVE: ArchiveState = {
  archive_size: 1,
  elite: { id: "var_demo", name: "Demo elite", fitness: 0.91, status: "sandbox_evaluated" },
  variants: [{ id: "var_demo", name: "Demo elite", fitness: 0.91, status: "sandbox_evaluated" }],
};

async function fetchArchive(): Promise<ArchiveState> {
  if (env.demoMode) {
    return DEMO_ARCHIVE;
  }
  return (await backendApi.evolutionArchive()) as ArchiveState;
}

export function EvolutionArchivePanel() {
  const [archive, setArchive] = useState<ArchiveState | null>(() => (env.demoMode ? DEMO_ARCHIVE : null));
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [loading, setLoading] = useState(!env.demoMode);

  // Mount load: all setState calls are deferred until after await (not synchronous in the effect body).
  useEffect(() => {
    if (env.demoMode) {
      return;
    }
    let cancelled = false;
    void (async () => {
      try {
        const data = await fetchArchive();
        if (cancelled) return;
        setArchive(data);
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
    // Event-handler path (Refresh / post-action): setState after await only where possible
    try {
      const data = await fetchArchive();
      setArchive(data);
      setError(null);
      setLoading(false);
    } catch (err) {
      setError(formatMutationError(err));
      setLoading(false);
    }
  }, []);

  async function evaluate(id: string) {
    setBusy(id);
    setError(null);
    try {
      if (!env.demoMode) {
        await backendApi.evaluateVariant(id);
      }
      await load();
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function canary(id: string) {
    setBusy(`canary-${id}`);
    setError(null);
    try {
      if (!env.demoMode) {
        try {
          await backendApi.evaluateVariant(id);
        } catch {
          /* already evaluated or blocked */
        }
        await backendApi.promoteVariant(id, "canary");
      }
      await load();
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function evaluateThenCanary(id: string) {
    setBusy(`pipeline-${id}`);
    setError(null);
    try {
      if (!env.demoMode) {
        const evaluated = (await backendApi.evaluateVariant(id)) as {
          evaluation?: { result?: string };
        };
        if (evaluated.evaluation?.result !== "passed") {
          setError("Evaluation did not pass — canary blocked");
          await load();
          return;
        }
        await backendApi.promoteVariant(id, "canary");
      }
      await load();
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  const variants = archive?.variants || [];

  return (
    <div className="space-y-5" data-testid="evolution-archive">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Population archive</p>
          <p className="mt-1 text-sm text-muted">
            DGM-lite archive: variants ranked by fitness. Sandbox only until canary/promote.
          </p>
        </div>
        <Button variant="secondary" onClick={() => void load()} data-testid="archive-refresh">
          Refresh
        </Button>
      </div>
      {loading && !archive ? <p className="text-sm text-muted">Loading archive…</p> : null}
      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="p-4">
          <p className="text-xs text-muted">Archive size</p>
          <p className="mt-2 text-2xl font-semibold text-white">{archive?.archive_size ?? "—"}</p>
        </Card>
        <Card className="p-4 md:col-span-2">
          <p className="text-xs text-muted">Elite</p>
          <p className="mt-2 text-sm text-white">
            {archive?.elite
              ? `${archive.elite.name || archive.elite.id} · fitness ${archive.elite.fitness ?? "n/a"}`
              : "No variants yet — propose from Improve on a run"}
          </p>
        </Card>
      </div>
      <div className="space-y-3">
        {variants.map((v) => (
          <Card key={String(v.id)} className="flex flex-col gap-3 p-4 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="font-medium text-white">{v.name || v.id}</p>
              <p className="mt-1 text-xs text-muted">
                base={v.base_workflow_id || "—"} · fitness={v.fitness ?? "—"} · eval={v.evaluation_result || "—"}
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2">
              {v.status ? <StatusBadge status={String(v.status)} /> : null}
              <Button variant="secondary" disabled={busy !== null} onClick={() => void evaluate(String(v.id))}>
                {busy === v.id ? "Evaluating…" : "Evaluate"}
              </Button>
              <Button disabled={busy !== null} onClick={() => void canary(String(v.id))}>
                {busy === `canary-${v.id}` ? "…" : "Canary"}
              </Button>
              <Button
                disabled={busy !== null}
                onClick={() => void evaluateThenCanary(String(v.id))}
                data-testid="archive-eval-canary"
              >
                {busy === `pipeline-${v.id}` ? "…" : "Eval → Canary"}
              </Button>
            </div>
          </Card>
        ))}
        {!variants.length && !loading ? (
          <p className="text-sm text-muted">Archive empty. Use Reflect / Propose sandbox variant on a workflow run.</p>
        ) : null}
      </div>
    </div>
  );
}
