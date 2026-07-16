"use client";

import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { backendApi } from "@/lib/api/client";
import { cachedFetch } from "@/lib/api/client-cache";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

type SpecialSkill = {
  skill_id: string;
  kind?: string;
  status?: string;
  summary?: string;
  score?: number;
  full_mark?: boolean;
  agents?: string[];
  dna?: string[];
  has_skill_md?: boolean;
};

type SpecialSkillsResponse = {
  count?: number;
  skills?: SpecialSkill[];
  residuals_note?: string;
  registry_path?: string;
};

const DEMO_SKILLS: SpecialSkillsResponse = {
  count: 17,
  registry_path: "business/video/special_skills/REGISTRY.json",
  residuals_note: "Demo mode — pack catalog not loaded from API.",
  skills: Array.from({ length: 17 }, (_, i) => ({
    skill_id: `demo_skill_${i + 1}`,
    kind: "demo",
    status: "mvp_integrated",
    score: 90,
  })),
};

async function fetchSkills(): Promise<SpecialSkillsResponse> {
  if (env.demoMode) {
    return DEMO_SKILLS;
  }
  return cachedFetch("domains:video:special-skills", async () =>
    (await backendApi.videoSpecialSkills()) as SpecialSkillsResponse,
  );
}

export function SpecialSkillsPanel() {
  const [data, setData] = useState<SpecialSkillsResponse | null>(() =>
    env.demoMode ? DEMO_SKILLS : null,
  );
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(!env.demoMode);

  const load = useCallback(async () => {
    try {
      const next = await fetchSkills();
      setData(next);
      setError(null);
      setLoading(false);
    } catch (err) {
      setError(formatMutationError(err));
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (env.demoMode) return;
    let cancelled = false;
    void (async () => {
      try {
        const next = await fetchSkills();
        if (cancelled) return;
        setData(next);
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

  const skills = data?.skills || [];
  const count = data?.count ?? skills.length;

  return (
    <div className="space-y-4" data-testid="special-skills-panel">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">
            Special skills
          </p>
          <p className="mt-1 text-sm text-muted">
            Pack integrations from{" "}
            <code className="text-xs text-white/80">business/video/special_skills/</code>
            {" — "}
            catalog visibility only (not live media execution).
          </p>
        </div>
        <div className="flex items-center gap-2">
          <StatusBadge status={count >= 17 ? "completed" : "pending"} />
          <span className="text-sm text-white" data-testid="special-skills-count">
            {loading ? "…" : `${count} skills`}
          </span>
          {!env.demoMode ? (
            <Button type="button" variant="secondary" onClick={() => void load()}>
              Refresh
            </Button>
          ) : null}
        </div>
      </div>

      {error ? (
        <p className="text-sm text-red-400" data-testid="special-skills-error">
          {error}
        </p>
      ) : null}

      <div className="overflow-x-auto rounded-md border border-white/10">
        <table className="min-w-full text-left text-sm" data-testid="special-skills-table">
          <thead className="bg-white/[0.04] text-xs uppercase tracking-wide text-muted">
            <tr>
              <th className="px-3 py-2">skill_id</th>
              <th className="px-3 py-2">kind</th>
              <th className="px-3 py-2">status</th>
              <th className="px-3 py-2">score</th>
              <th className="px-3 py-2">summary</th>
            </tr>
          </thead>
          <tbody>
            {skills.map((s) => (
              <tr
                key={s.skill_id}
                className="border-t border-white/5 text-white/90"
                data-testid={`special-skill-row-${s.skill_id}`}
              >
                <td className="px-3 py-2 font-mono text-xs">{s.skill_id}</td>
                <td className="px-3 py-2 text-xs">{s.kind || "—"}</td>
                <td className="px-3 py-2 text-xs">{s.status || "—"}</td>
                <td className="px-3 py-2 text-xs">
                  {typeof s.score === "number" ? s.score : "—"}
                  {s.full_mark ? " ✓" : ""}
                </td>
                <td className="max-w-md truncate px-3 py-2 text-xs text-muted">
                  {s.summary || "—"}
                </td>
              </tr>
            ))}
            {!loading && skills.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-3 py-4 text-muted">
                  No special skills registered.
                </td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>

      {data?.residuals_note ? (
        <p className="text-xs text-muted">{data.residuals_note}</p>
      ) : null}
      {data?.registry_path ? (
        <p className="text-xs text-muted">Source: {data.registry_path}</p>
      ) : null}
    </div>
  );
}
