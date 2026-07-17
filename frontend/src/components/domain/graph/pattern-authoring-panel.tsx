"use client";

import { useEffect, useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { GraphTopologyPanel } from "@/components/domain/graph/graph-topology-panel";

type Pattern = {
  id: string;
  name: string;
  description?: string;
  config_schema?: Record<string, unknown>;
};

type AgentRow = { id?: string; name?: string; status?: string };

const PATTERNS_FALLBACK: Pattern[] = [
  { id: "pipeline", name: "Pipeline", description: "Linear DNA steps" },
  { id: "supervisor", name: "Supervisor", description: "Handoffs to specialists" },
  { id: "router", name: "Router", description: "Branch by route" },
  { id: "critique", name: "Critique loop", description: "Produce → critique" },
  { id: "map_reduce", name: "Map-reduce", description: "Fan-out / join" },
  { id: "pack_spine", name: "Pack spine", description: "Domain pack entry spine" },
];

export function PatternAuthoringPanel({
  workflowId,
  initialPattern,
  initialEngine,
  initialSupervisor,
  initialSpecialists,
}: {
  workflowId: string;
  initialPattern?: string;
  initialEngine?: string;
  initialSupervisor?: string;
  initialSpecialists?: string[];
}) {
  const [patterns, setPatterns] = useState<Pattern[]>(PATTERNS_FALLBACK);
  const [agents, setAgents] = useState<AgentRow[]>([]);
  const [pattern, setPattern] = useState(initialPattern || "pipeline");
  const [engine, setEngine] = useState(initialEngine || "legacy");
  const [supervisor, setSupervisor] = useState(initialSupervisor || "business_orchestrator");
  const [specialists, setSpecialists] = useState<string[]>(initialSpecialists || []);
  const [maxHandoffs, setMaxHandoffs] = useState(12);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState<string | null>(null);
  const [topoKey, setTopoKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      if (env.demoMode) return;
      try {
        const [p, a] = await Promise.all([
          backendApi.listOrchestrationPatterns() as Promise<{ items?: Pattern[] }>,
          backendApi.listAgents() as Promise<AgentRow[] | { items?: AgentRow[] }>,
        ]);
        if (cancelled) return;
        if (Array.isArray(p?.items) && p.items.length) setPatterns(p.items);
        const list = Array.isArray(a) ? a : a?.items || [];
        setAgents(list.filter((x) => x?.id));
      } catch {
        /* keep fallbacks */
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  const agentOptions = useMemo(() => {
    const ids = agents.map((a) => String(a.id));
    const extras = [supervisor, ...specialists].filter(Boolean);
    return Array.from(new Set([...ids, ...extras]));
  }, [agents, supervisor, specialists]);

  function toggleSpecialist(id: string) {
    setSpecialists((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
  }

  async function onSave() {
    setBusy(true);
    setError(null);
    setSaved(null);
    try {
      if (env.demoMode) {
        setSaved("Demo mode — not persisted");
        return;
      }
      const config: Record<string, unknown> = {};
      if (pattern === "supervisor") {
        if (!supervisor.trim()) throw new Error("Supervisor agent is required");
        if (!specialists.length) throw new Error("Select at least one specialist");
        config.supervisor_agent = supervisor.trim();
        config.specialists = specialists;
        config.max_handoffs = maxHandoffs;
      }
      await backendApi.updateWorkflow(workflowId, {
        execution_engine: engine,
        orchestration: { pattern, config },
      });
      setSaved(`Saved ${pattern} · engine=${engine}`);
      setTopoKey((k) => k + 1);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Save failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="space-y-5 rounded-[24px] border border-white/10 bg-white/5 p-5">
      <div>
        <p className="text-sm font-semibold text-white">Orchestration pattern</p>
        <p className="mt-1 text-sm text-muted">
          Choose LangGraph pattern and engine. No free-form code — config only (LG-13).
        </p>
      </div>

      <label className="block text-xs text-muted">
        Pattern
        <select
          className="mt-1 w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm text-white"
          value={pattern}
          onChange={(e) => setPattern(e.target.value)}
        >
          {patterns.map((p) => (
            <option key={p.id} value={p.id}>
              {p.name}
            </option>
          ))}
        </select>
        <span className="mt-1 block text-[11px] opacity-80">
          {patterns.find((p) => p.id === pattern)?.description}
        </span>
      </label>

      <label className="block text-xs text-muted">
        Execution engine
        <select
          className="mt-1 w-full rounded-xl border border-white/10 bg-black/30 px-3 py-2 text-sm text-white"
          value={engine}
          onChange={(e) => setEngine(e.target.value)}
        >
          <option value="legacy">legacy (linear runner)</option>
          <option value="langgraph">langgraph (StateGraph)</option>
        </select>
      </label>

      {pattern === "supervisor" ? (
        <div className="space-y-3 rounded-2xl border border-white/10 bg-black/20 p-4">
          <label className="block text-xs text-muted">
            Supervisor agent
            <select
              className="mt-1 w-full rounded-xl border border-white/10 bg-black/40 px-3 py-2 text-sm text-white"
              value={supervisor}
              onChange={(e) => setSupervisor(e.target.value)}
            >
              {agentOptions.map((id) => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-xs text-muted">
            Max handoffs
            <input
              type="number"
              min={1}
              max={64}
              className="mt-1 w-full rounded-xl border border-white/10 bg-black/40 px-3 py-2 text-sm text-white"
              value={maxHandoffs}
              onChange={(e) => setMaxHandoffs(Number(e.target.value) || 12)}
            />
          </label>
          <div>
            <p className="text-xs text-muted">Specialists</p>
            <div className="mt-2 flex max-h-40 flex-wrap gap-2 overflow-y-auto">
              {agentOptions.slice(0, 40).map((id) => {
                const on = specialists.includes(id);
                return (
                  <button
                    key={id}
                    type="button"
                    onClick={() => toggleSpecialist(id)}
                    className={`rounded-full border px-2.5 py-1 text-[11px] ${
                      on
                        ? "border-emerald-400/40 bg-emerald-500/15 text-emerald-100"
                        : "border-white/10 bg-black/30 text-muted"
                    }`}
                  >
                    {id}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      ) : null}

      <div className="flex flex-wrap gap-3">
        <Button disabled={busy} onClick={() => void onSave()}>
          {busy ? "Saving…" : "Save orchestration"}
        </Button>
      </div>
      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
      {saved ? <p className="text-sm text-[var(--accent-2)]">{saved}</p> : null}

      <div className="pt-2">
        <p className="mb-2 text-xs uppercase tracking-[0.2em] text-[var(--accent)]">Preview</p>
        <GraphTopologyPanel key={topoKey} workflowId={workflowId} />
      </div>
    </div>
  );
}
