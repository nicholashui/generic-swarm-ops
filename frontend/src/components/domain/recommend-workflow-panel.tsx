"use client";

import { useCallback, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/ui/status-badge";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

type Recommendation = {
  code?: string | null;
  name?: string;
  process_id?: string;
  dna_id?: string;
  recommended_scale?: string;
  score?: number;
  depth?: string;
  reasons?: string[];
  lead_agents?: string[];
};

type RecommendResponse = {
  recommendation?: Recommendation;
  alternatives?: Array<{
    code?: string;
    name?: string;
    dna_id?: string;
    score?: number;
    recommended_scale?: string;
  }>;
  confidence?: number;
  hitl_confirm_required?: boolean;
  inferred_scale?: string;
  duration_sec?: number | null;
  residuals_note?: string;
};

const DEMO_RESULT: RecommendResponse = {
  recommendation: {
    code: "A",
    name: "Viral Hook Clip / Meme",
    process_id: "video.arch.a.viral_hook",
    dna_id: "wf_video_arch_a_viral_hook_v1",
    recommended_scale: "S1",
    score: 9.2,
    reasons: ["demo mode — live API not called"],
  },
  alternatives: [
    { code: "B", dna_id: "wf_video_arch_b_ugc_ad_v1", score: 3.8 },
  ],
  confidence: 0.8,
  hitl_confirm_required: true,
  inferred_scale: "S1",
};

export function RecommendWorkflowPanel() {
  const [brief, setBrief] = useState("15s viral TikTok hook about coffee");
  const [duration, setDuration] = useState<string>("15");
  const [result, setResult] = useState<RecommendResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const runRecommend = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      if (env.demoMode) {
        setResult(DEMO_RESULT);
        setLoading(false);
        return;
      }
      const durationSec = duration.trim() === "" ? undefined : Number(duration);
      const data = (await backendApi.recommendVideoWorkflow({
        brief,
        duration_sec: Number.isFinite(durationSec) ? durationSec : undefined,
        top_k: 3,
      })) as RecommendResponse;
      setResult(data);
    } catch (err) {
      setError(formatMutationError(err));
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, [brief, duration]);

  const rec = result?.recommendation;

  return (
    <div className="space-y-4" data-testid="recommend-workflow-panel">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">
            Recommend workflow
          </p>
          <p className="mt-1 text-sm text-muted">
            Free-text brief → ranked A–J DNA (real selector API). Not a live media studio; HiTL
            confirm before launch.
          </p>
        </div>
        {result ? (
          <StatusBadge status={result.hitl_confirm_required ? "pending" : "completed"} />
        ) : null}
      </div>

      <label className="block space-y-1">
        <span className="text-xs text-muted">Production brief</span>
        <textarea
          data-testid="recommend-brief"
          className="min-h-[88px] w-full rounded-md border border-white/10 bg-black/30 px-3 py-2 text-sm text-white"
          value={brief}
          onChange={(e) => setBrief(e.target.value)}
          placeholder="e.g. 15s viral TikTok hook about coffee"
        />
      </label>

      <div className="flex flex-wrap items-end gap-3">
        <label className="space-y-1">
          <span className="text-xs text-muted">Duration (sec, optional)</span>
          <input
            data-testid="recommend-duration"
            type="number"
            min={0}
            className="w-28 rounded-md border border-white/10 bg-black/30 px-3 py-2 text-sm text-white"
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
          />
        </label>
        <Button
          type="button"
          data-testid="recommend-submit"
          disabled={loading || !brief.trim()}
          onClick={() => void runRecommend()}
        >
          {loading ? "Recommending…" : "Recommend DNA"}
        </Button>
      </div>

      {error ? (
        <p className="text-sm text-red-400" data-testid="recommend-error">
          {error}
        </p>
      ) : null}

      {rec ? (
        <Card className="space-y-3 border-white/10 bg-white/[0.03] p-4" data-testid="recommend-result">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-lg font-semibold text-white">
              {rec.code ? `${rec.code} — ` : ""}
              {rec.name || "Recommendation"}
            </span>
            {typeof result?.confidence === "number" ? (
              <span className="text-xs text-muted">
                confidence {(result.confidence * 100).toFixed(0)}%
              </span>
            ) : null}
          </div>
          <dl className="grid gap-2 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-xs text-muted">dna_id</dt>
              <dd className="font-mono text-white" data-testid="recommend-dna-id">
                {rec.dna_id || "—"}
              </dd>
            </div>
            <div>
              <dt className="text-xs text-muted">process_id</dt>
              <dd className="font-mono text-white">{rec.process_id || "—"}</dd>
            </div>
            <div>
              <dt className="text-xs text-muted">scale</dt>
              <dd className="text-white">{rec.recommended_scale || result?.inferred_scale || "—"}</dd>
            </div>
            <div>
              <dt className="text-xs text-muted">selector score</dt>
              <dd className="text-white">{rec.score ?? "—"}</dd>
            </div>
          </dl>
          {rec.reasons?.length ? (
            <ul className="list-inside list-disc text-xs text-muted">
              {rec.reasons.map((r) => (
                <li key={r}>{r}</li>
              ))}
            </ul>
          ) : null}
          {result?.alternatives?.length ? (
            <div>
              <p className="mb-1 text-xs uppercase tracking-wide text-muted">Alternatives</p>
              <ul className="space-y-1 text-sm text-white/90" data-testid="recommend-alternatives">
                {result.alternatives.map((a) => (
                  <li key={a.dna_id || a.code} className="font-mono text-xs">
                    {a.code} · {a.dna_id} · score {a.score}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
          <p className="text-xs text-muted">
            Residuals: live media vendors and full DNA production_ready are not claimed. Use viral-hook
            path for host-executable demo when dna_id is wf_video_arch_a_viral_hook_v1.
          </p>
        </Card>
      ) : null}
    </div>
  );
}
