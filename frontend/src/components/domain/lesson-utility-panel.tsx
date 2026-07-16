"use client";

import { useCallback, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { backendApi } from "@/lib/api/client";
import { cachedFetch } from "@/lib/api/client-cache";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

type LessonRow = {
  id?: string;
  text?: string;
  agent_id?: string | null;
  utility?: number;
  uses?: number;
  wins?: number;
};

type UtilityState = {
  lessons?: LessonRow[];
  aggregates?: {
    total_lessons?: number;
    knowledge_growth_count?: number;
    lesson_reuse_rate?: number;
    lesson_win_rate?: number;
    by_agent?: Record<string, { count?: number; avg_utility?: number; uses?: number }>;
  };
  agent_id?: string | null;
};

const DEMO_UTILITY: UtilityState = {
  lessons: [
    {
      id: "lesson_demo_1",
      text: "Keep viral hooks under 3 seconds before the payoff.",
      agent_id: "video.planner",
      utility: 0.75,
      uses: 4,
      wins: 3,
    },
    {
      id: "lesson_demo_2",
      text: "QC consistency: same palette across hook frames.",
      agent_id: "video.aiqaconsistency",
      utility: 0.67,
      uses: 2,
      wins: 1,
    },
  ],
  aggregates: {
    total_lessons: 2,
    knowledge_growth_count: 2,
    lesson_reuse_rate: 3.0,
    lesson_win_rate: 0.6,
    by_agent: {
      "video.planner": { count: 1, avg_utility: 0.75, uses: 4 },
      "video.aiqaconsistency": { count: 1, avg_utility: 0.67, uses: 2 },
    },
  },
};

async function fetchUtility(): Promise<UtilityState> {
  if (env.demoMode) {
    return DEMO_UTILITY;
  }
  return cachedFetch("improvement:lesson-utility", async () =>
    (await backendApi.lessonUtilityDashboard()) as UtilityState,
  );
}

export function LessonUtilityPanel() {
  const [data, setData] = useState<UtilityState | null>(() => (env.demoMode ? DEMO_UTILITY : null));
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(!env.demoMode);

  useEffect(() => {
    if (env.demoMode) {
      return;
    }
    let cancelled = false;
    void (async () => {
      try {
        const next = await fetchUtility();
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

  const load = useCallback(async () => {
    try {
      const next = await fetchUtility();
      setData(next);
      setError(null);
      setLoading(false);
    } catch (err) {
      setError(formatMutationError(err));
      setLoading(false);
    }
  }, []);

  const lessons = data?.lessons || [];
  const agg = data?.aggregates;

  return (
    <div className="space-y-5" data-testid="lesson-utility">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Lesson utility</p>
          <p className="mt-1 text-sm text-muted">
            ALC ranked lessons by utility and reuse — sandbox learning signal for coevolution fitness.
          </p>
        </div>
        <Button variant="secondary" onClick={() => void load()} data-testid="lesson-utility-refresh">
          Refresh
        </Button>
      </div>
      {loading && !data ? <p className="text-sm text-muted">Loading lesson utility…</p> : null}
      {error ? <p className="text-sm text-[var(--danger)]">{error}</p> : null}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="p-4">
          <p className="text-xs uppercase tracking-wide text-muted">Knowledge growth</p>
          <p className="mt-2 text-2xl font-semibold">{agg?.knowledge_growth_count ?? agg?.total_lessons ?? 0}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs uppercase tracking-wide text-muted">Lesson reuse rate</p>
          <p className="mt-2 text-2xl font-semibold">{Number(agg?.lesson_reuse_rate ?? 0).toFixed(2)}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs uppercase tracking-wide text-muted">Win rate</p>
          <p className="mt-2 text-2xl font-semibold">{Number(agg?.lesson_win_rate ?? 0).toFixed(2)}</p>
        </Card>
      </div>
      <div className="space-y-2">
        <p className="text-xs uppercase tracking-wide text-muted">Top lessons</p>
        {lessons.length === 0 ? (
          <p className="text-sm text-muted">No lessons yet. Reflect on video runs to grow agent knowledge.</p>
        ) : (
          <ul className="space-y-2">
            {lessons.slice(0, 8).map((lesson) => (
              <li key={lesson.id || lesson.text} className="rounded-lg border border-[var(--border)] p-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-xs text-muted">{lesson.agent_id || "unscoped"}</span>
                  <span className="text-xs font-medium">
                    u={Number(lesson.utility ?? 0).toFixed(2)} · uses={lesson.uses ?? 0}
                  </span>
                </div>
                <p className="mt-1 text-sm">{lesson.text}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
