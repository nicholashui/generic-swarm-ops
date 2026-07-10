"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

type StepKey = "reflect" | "propose" | "evaluate" | "canary" | "full";

/**
 * Guided self-improvement: Reflect → Propose sandbox → Evaluate → Canary.
 */
export function ImproveRunButton({
  runId,
  workflowId,
}: {
  runId: string;
  workflowId?: string;
}) {
  const router = useRouter();
  const [busy, setBusy] = useState<StepKey | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [variantId, setVariantId] = useState<string | null>(null);
  const [steps, setSteps] = useState<string[]>([]);

  function pushStep(msg: string) {
    setSteps((s) => [...s, msg]);
  }

  async function resolveWorkflowId(fromResult?: Record<string, unknown>): Promise<string> {
    if (workflowId) return workflowId;
    if (typeof fromResult?.workflow_id === "string" && fromResult.workflow_id) return fromResult.workflow_id;
    if (typeof result?.workflow_id === "string" && result.workflow_id) return String(result.workflow_id);
    const reflection = (await backendApi.reflectRun(runId)) as Record<string, unknown>;
    return String(reflection.workflow_id || "");
  }

  async function onReflect() {
    setError(null);
    setBusy("reflect");
    try {
      if (env.demoMode) {
        setResult({ demo: true, action: "reflect", runId, lessons: ["Demo lesson: review gate latency"] });
        pushStep("demo: reflected");
        return;
      }
      const reflection = (await backendApi.reflectRun(runId)) as Record<string, unknown>;
      setResult({ action: "reflect", ...reflection });
      pushStep(`reflected · lessons=${Array.isArray(reflection.lessons) ? reflection.lessons.length : 0}`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function onPropose() {
    setError(null);
    setBusy("propose");
    try {
      if (env.demoMode) {
        setVariantId("var_demo");
        setResult({ demo: true, action: "auto-propose", runId, sandbox_only: true, id: "var_demo" });
        pushStep("demo: proposed var_demo");
        return;
      }
      const wf = await resolveWorkflowId();
      if (!wf) {
        setError("workflow_id unknown — open from a workflow-linked run");
        return;
      }
      const variant = (await backendApi.autoProposeImprovement({
        workflow_id: wf,
        run_id: runId,
      })) as Record<string, unknown>;
      const id = String(variant.id || "");
      setVariantId(id || null);
      setResult({ action: "auto-propose", variant });
      pushStep(`proposed ${id} (sandbox_only=${String(variant.sandbox_only)})`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function onEvaluate() {
    setError(null);
    setBusy("evaluate");
    try {
      const id = variantId || (typeof (result as { variant?: { id?: string } })?.variant?.id === "string"
        ? String((result as { variant?: { id?: string } }).variant?.id)
        : null);
      if (!id) {
        setError("Propose a sandbox variant first");
        return;
      }
      if (env.demoMode) {
        setResult({ demo: true, action: "evaluate", id, evaluation: { result: "passed" } });
        pushStep("demo: evaluated passed");
        return;
      }
      const evaluated = (await backendApi.evaluateVariant(id)) as Record<string, unknown>;
      setResult({ action: "evaluate", evaluated });
      const er = (evaluated.evaluation as { result?: string } | undefined)?.result;
      pushStep(`evaluated ${id} → ${er || evaluated.status}`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function onCanary() {
    setError(null);
    setBusy("canary");
    try {
      const id = variantId;
      if (!id) {
        setError("Propose + evaluate a variant first");
        return;
      }
      if (env.demoMode) {
        setResult({ demo: true, action: "canary", id, status: "approved_for_canary" });
        pushStep("demo: canary approved");
        return;
      }
      const canary = (await backendApi.promoteVariant(id, "canary")) as Record<string, unknown>;
      setResult({ action: "canary", canary });
      pushStep(`canary ${id} → ${String(canary.status)}`);
      router.push("/app/evolution");
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function onFullPipeline() {
    setError(null);
    setSteps([]);
    setBusy("full");
    try {
      if (env.demoMode) {
        setVariantId("var_demo");
        setResult({
          demo: true,
          action: "full_pipeline",
          steps: ["reflect", "propose", "evaluate", "canary"],
          status: "approved_for_canary",
        });
        setSteps(["demo: reflect", "demo: propose", "demo: evaluate passed", "demo: canary approved"]);
        return;
      }
      const reflection = (await backendApi.reflectRun(runId)) as Record<string, unknown>;
      pushStep(`reflected · lessons=${Array.isArray(reflection.lessons) ? reflection.lessons.length : 0}`);
      const wf = String(workflowId || reflection.workflow_id || "");
      if (!wf) throw new Error("workflow_id missing after reflect");
      const variant = (await backendApi.autoProposeImprovement({
        workflow_id: wf,
        run_id: runId,
      })) as Record<string, unknown>;
      const id = String(variant.id || "");
      setVariantId(id);
      pushStep(`proposed ${id}`);
      const evaluated = (await backendApi.evaluateVariant(id)) as Record<string, unknown>;
      const er = (evaluated.evaluation as { result?: string } | undefined)?.result;
      pushStep(`evaluated → ${er || evaluated.status}`);
      if (er !== "passed") {
        setResult({ action: "full_pipeline", reflection, variant, evaluated, stopped: "eval_failed" });
        setError("Sandbox evaluation failed — canary blocked (as designed)");
        return;
      }
      const canary = (await backendApi.promoteVariant(id, "canary")) as Record<string, unknown>;
      pushStep(`canary → ${String(canary.status)}`);
      setResult({ action: "full_pipeline", reflection, variant, evaluated, canary });
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="space-y-3" data-testid="improve-run">
      <div className="flex flex-wrap gap-2">
        <Button
          variant="secondary"
          disabled={busy !== null}
          onClick={() => void onReflect()}
          data-testid="improve-reflect"
        >
          <Sparkles className="size-4" />
          {busy === "reflect" ? "Reflecting…" : "1. Reflect"}
        </Button>
        <Button
          variant="secondary"
          disabled={busy !== null}
          onClick={() => void onPropose()}
          data-testid="improve-propose"
        >
          {busy === "propose" ? "Proposing…" : "2. Propose"}
        </Button>
        <Button
          variant="secondary"
          disabled={busy !== null || (!variantId && !env.demoMode)}
          onClick={() => void onEvaluate()}
          data-testid="improve-evaluate"
        >
          {busy === "evaluate" ? "Evaluating…" : "3. Evaluate"}
        </Button>
        <Button
          variant="secondary"
          disabled={busy !== null || (!variantId && !env.demoMode)}
          onClick={() => void onCanary()}
          data-testid="improve-canary"
        >
          {busy === "canary" ? "Canary…" : "4. Canary"}
        </Button>
        <Button disabled={busy !== null} onClick={() => void onFullPipeline()} data-testid="improve-full">
          {busy === "full" ? "Running pipeline…" : "Run full pipeline"}
        </Button>
        <Button
          variant="ghost"
          disabled={busy !== null}
          onClick={() => router.push("/app/evolution")}
          data-testid="improve-open-archive"
        >
          Open archive
        </Button>
      </div>
      {steps.length ? (
        <ol className="list-decimal space-y-1 pl-5 text-xs text-muted" data-testid="improve-steps">
          {steps.map((s) => (
            <li key={s}>{s}</li>
          ))}
        </ol>
      ) : null}
      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="improve-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre
          data-testid="improve-result"
          className="max-h-64 overflow-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]"
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}
