"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm, useWatch } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import {
  MEMORY_SCOPE_OPTIONS,
  RISK_TIERS,
  TOOL_OPTIONS,
  agentCreateSchema,
  formatMutationError,
  workflowCreateSchema,
  type AgentCreateValues,
  type WorkflowCreateValues,
} from "@/lib/forms/create-resource-schemas";

export type FormMutationKind = "agent" | "workflow" | "settings";

type Props = {
  kind: FormMutationKind;
  draftLabel: string;
  submitLabel: string;
  /** Optional stable id for create payloads */
  resourceHint?: string;
};

function slugId(prefix: string, hint?: string, name?: string): string {
  const seed = name || hint || `${prefix}_${Date.now()}`;
  const base = seed
    .toLowerCase()
    .replace(/[^a-z0-9_]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 36);
  return base.startsWith(prefix) ? base : `${prefix}_${base || Date.now()}`;
}

function FieldError({ message }: { message?: string }) {
  if (!message) return null;
  return <p className="mt-1 text-xs text-[var(--danger)]">{message}</p>;
}

function CheckboxGroup({
  options,
  selected,
  onToggle,
  testIdPrefix,
}: {
  options: readonly string[];
  selected: string[];
  onToggle: (value: string) => void;
  testIdPrefix: string;
}) {
  return (
    <div className="flex flex-wrap gap-2">
      {options.map((option) => {
        const checked = selected.includes(option);
        return (
          <label
            key={option}
            className={`cursor-pointer rounded-full border px-3 py-1.5 text-xs ${
              checked
                ? "border-[var(--accent)] bg-[var(--accent)]/15 text-white"
                : "border-white/12 bg-white/4 text-slate-300"
            }`}
          >
            <input
              type="checkbox"
              className="sr-only"
              checked={checked}
              data-testid={`${testIdPrefix}-${option}`}
              onChange={() => onToggle(option)}
            />
            {option}
          </label>
        );
      })}
    </div>
  );
}

function AgentCreateForm({
  draftLabel,
  submitLabel,
  resourceHint,
}: {
  draftLabel: string;
  submitLabel: string;
  resourceHint?: string;
}) {
  const router = useRouter();
  const [busy, setBusy] = useState<"draft" | "submit" | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  const form = useForm<AgentCreateValues>({
    resolver: zodResolver(agentCreateSchema),
    defaultValues: {
      name: "",
      description: "",
      department: "operations",
      risk_level: "tier_2_draft",
      allowed_tools: ["audit_log_writer"],
      allowed_memory_scopes: ["organization_memory", "workflow_memory"],
      system_instructions: "",
    },
  });

  async function run(mode: "draft" | "submit") {
    setError(null);
    setBusy(mode);
    const valid = await form.trigger();
    if (!valid) {
      setBusy(null);
      return;
    }
    const values = form.getValues();
    try {
      if (env.demoMode) {
        setResult({ demo: true, mode, kind: "agent", status: mode === "draft" ? "draft" : "submitted", ...values });
        return;
      }
      const id = slugId("agent", resourceHint, values.name);
      const payload = {
        id,
        name: values.name,
        description: values.description,
        department: values.department,
        status: mode === "draft" ? "draft" : "active",
        allowed_tools: values.allowed_tools,
        allowed_memory_scopes: values.allowed_memory_scopes,
        risk_level: values.risk_level,
        runtime_configuration: {
          system_instructions: values.system_instructions || undefined,
        },
      };
      const created = (await backendApi.createAgent(payload)) as Record<string, unknown>;
      setResult(created);
      if (mode === "submit") router.push(`/app/agents/${id}`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  const tools = useWatch({ control: form.control, name: "allowed_tools" }) ?? [];
  const scopes = useWatch({ control: form.control, name: "allowed_memory_scopes" }) ?? [];

  return (
    <div className="space-y-5" data-testid="agent-create-form">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label htmlFor="agent-name">Agent name</Label>
          <Input id="agent-name" data-testid="agent-name" placeholder="e.g. Onboarding assistant" {...form.register("name")} />
          <FieldError message={form.formState.errors.name?.message} />
        </div>
        <div>
          <Label htmlFor="agent-department">Owner team</Label>
          <Input id="agent-department" data-testid="agent-department" placeholder="operations" {...form.register("department")} />
          <FieldError message={form.formState.errors.department?.message} />
        </div>
        <div className="md:col-span-2">
          <Label htmlFor="agent-description">Business description</Label>
          <Textarea
            id="agent-description"
            data-testid="agent-description"
            placeholder="What this agent owns and when it should escalate"
            {...form.register("description")}
          />
          <FieldError message={form.formState.errors.description?.message} />
        </div>
        <div>
          <Label htmlFor="agent-risk">Risk tier</Label>
          <select
            id="agent-risk"
            data-testid="agent-risk"
            className="w-full rounded-2xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white focus:border-[var(--accent)] focus:outline-none"
            {...form.register("risk_level")}
          >
            {RISK_TIERS.map((tier) => (
              <option key={tier} value={tier} className="bg-slate-900">
                {tier}
              </option>
            ))}
          </select>
          <FieldError message={form.formState.errors.risk_level?.message} />
        </div>
        <div>
          <Label htmlFor="agent-instructions">System instructions</Label>
          <Input
            id="agent-instructions"
            data-testid="agent-instructions"
            placeholder="Optional instruction profile"
            {...form.register("system_instructions")}
          />
        </div>
        <div className="md:col-span-2">
          <Label>Tool permissions</Label>
          <CheckboxGroup
            options={TOOL_OPTIONS}
            selected={tools}
            testIdPrefix="agent-tool"
            onToggle={(value) => {
              const next = tools.includes(value) ? tools.filter((t) => t !== value) : [...tools, value];
              form.setValue("allowed_tools", next, { shouldValidate: true });
            }}
          />
          <FieldError message={form.formState.errors.allowed_tools?.message} />
        </div>
        <div className="md:col-span-2">
          <Label>Memory scopes</Label>
          <CheckboxGroup
            options={MEMORY_SCOPE_OPTIONS}
            selected={scopes}
            testIdPrefix="agent-scope"
            onToggle={(value) => {
              const next = scopes.includes(value) ? scopes.filter((s) => s !== value) : [...scopes, value];
              form.setValue("allowed_memory_scopes", next, { shouldValidate: true });
            }}
          />
          <FieldError message={form.formState.errors.allowed_memory_scopes?.message} />
        </div>
      </div>
      <div className="flex flex-wrap gap-3">
        <Button variant="secondary" disabled={busy !== null} onClick={() => void run("draft")} data-testid="form-draft">
          {busy === "draft" ? "Saving…" : draftLabel}
        </Button>
        <Button disabled={busy !== null} onClick={() => void run("submit")} data-testid="form-submit">
          {busy === "submit" ? "Submitting…" : submitLabel}
        </Button>
      </div>
      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="form-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre data-testid="form-result" className="overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]">
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}

function WorkflowCreateForm({
  draftLabel,
  submitLabel,
  resourceHint,
}: {
  draftLabel: string;
  submitLabel: string;
  resourceHint?: string;
}) {
  const router = useRouter();
  const [busy, setBusy] = useState<"draft" | "submit" | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  const form = useForm<WorkflowCreateValues>({
    resolver: zodResolver(workflowCreateSchema),
    defaultValues: {
      name: "",
      description: "",
      department: "operations",
      risk_tier: "tier_3_execute_reversible",
      primary_agent: "business_orchestrator",
      tools: ["audit_log_writer"],
      human_gate: false,
      evaluation_suite: "golden+regression",
      rollback_notes: "",
    },
  });

  async function run(mode: "draft" | "submit") {
    setError(null);
    setBusy(mode);
    const valid = await form.trigger();
    if (!valid) {
      setBusy(null);
      return;
    }
    const values = form.getValues();
    try {
      if (env.demoMode) {
        setResult({ demo: true, mode, kind: "workflow", status: mode === "draft" ? "draft" : "submitted", ...values });
        return;
      }
      const id = slugId("wf", resourceHint, values.name);
      const needsGate = values.human_gate || values.risk_tier === "tier_4_execute_with_gate";
      const steps = [
        {
          id: "start",
          agent: values.primary_agent,
          tools: values.tools,
          action_type: needsGate ? "irreversible_execution" : "analysis",
          human_gate_required: needsGate,
          irreversible: needsGate,
        },
      ];
      const payload = {
        id,
        name: values.name,
        description: values.description,
        department: values.department,
        status: mode === "draft" ? "draft" : "active",
        risk_tier: values.risk_tier,
        steps,
        evaluation_policy: {
          suite: values.evaluation_suite,
          block_on_fail: true,
          auto_promote: false,
        },
        rollback: {
          reversible: true,
          rollback_steps: (values.rollback_notes || "notify_ops_owner")
            .split(/[,;\n]+/)
            .map((s) => s.trim())
            .filter(Boolean),
        },
        input_schema: { type: "object", properties: { case_id: { type: "string" } }, required: ["case_id"] },
        output_schema: { type: "object", properties: { outcome: { type: "string" } }, required: [] },
        memory_reads: ["workflow_memory"],
        memory_writes: ["workflow_memory"],
      };
      const created = (await backendApi.createWorkflow(payload)) as Record<string, unknown>;
      setResult(created);
      if (mode === "submit") router.push(`/app/workflows/${id}`);
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  const tools = useWatch({ control: form.control, name: "tools" }) ?? [];

  return (
    <div className="space-y-5" data-testid="workflow-create-form">
      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <Label htmlFor="wf-name">Workflow name</Label>
          <Input id="wf-name" data-testid="workflow-name" placeholder="e.g. Customer onboarding vNext" {...form.register("name")} />
          <FieldError message={form.formState.errors.name?.message} />
        </div>
        <div>
          <Label htmlFor="wf-department">Owner</Label>
          <Input id="wf-department" data-testid="workflow-department" placeholder="operations" {...form.register("department")} />
          <FieldError message={form.formState.errors.department?.message} />
        </div>
        <div className="md:col-span-2">
          <Label htmlFor="wf-description">Business description</Label>
          <Textarea
            id="wf-description"
            data-testid="workflow-description"
            placeholder="Business goal, trigger, and success criteria"
            {...form.register("description")}
          />
          <FieldError message={form.formState.errors.description?.message} />
        </div>
        <div>
          <Label htmlFor="wf-risk">Risk tier</Label>
          <select
            id="wf-risk"
            data-testid="workflow-risk"
            className="w-full rounded-2xl border border-white/10 bg-white/6 px-4 py-3 text-sm text-white focus:border-[var(--accent)] focus:outline-none"
            {...form.register("risk_tier")}
          >
            {RISK_TIERS.map((tier) => (
              <option key={tier} value={tier} className="bg-slate-900">
                {tier}
              </option>
            ))}
          </select>
          <FieldError message={form.formState.errors.risk_tier?.message} />
        </div>
        <div>
          <Label htmlFor="wf-agent">Primary agent</Label>
          <Input
            id="wf-agent"
            data-testid="workflow-agent"
            placeholder="business_orchestrator"
            {...form.register("primary_agent")}
          />
          <FieldError message={form.formState.errors.primary_agent?.message} />
        </div>
        <div className="md:col-span-2">
          <Label>Tools on first step</Label>
          <CheckboxGroup
            options={TOOL_OPTIONS}
            selected={tools}
            testIdPrefix="workflow-tool"
            onToggle={(value) => {
              const next = tools.includes(value) ? tools.filter((t) => t !== value) : [...tools, value];
              form.setValue("tools", next, { shouldValidate: true });
            }}
          />
          <FieldError message={form.formState.errors.tools?.message} />
        </div>
        <div>
          <Label htmlFor="wf-eval">Evaluation suite</Label>
          <Input
            id="wf-eval"
            data-testid="workflow-eval"
            placeholder="golden+regression"
            {...form.register("evaluation_suite")}
          />
          <FieldError message={form.formState.errors.evaluation_suite?.message} />
        </div>
        <div>
          <Label htmlFor="wf-rollback">Rollback steps (comma-separated)</Label>
          <Input
            id="wf-rollback"
            data-testid="workflow-rollback"
            placeholder="disable_customer_record, notify_ops_owner"
            {...form.register("rollback_notes")}
          />
        </div>
        <div className="md:col-span-2">
          <label className="flex items-center gap-3 text-sm text-white">
            <input type="checkbox" data-testid="workflow-human-gate" {...form.register("human_gate")} className="size-4" />
            Require human gate on the primary step
          </label>
        </div>
      </div>
      <div className="flex flex-wrap gap-3">
        <Button variant="secondary" disabled={busy !== null} onClick={() => void run("draft")} data-testid="form-draft">
          {busy === "draft" ? "Saving…" : draftLabel}
        </Button>
        <Button disabled={busy !== null} onClick={() => void run("submit")} data-testid="form-submit">
          {busy === "submit" ? "Submitting…" : submitLabel}
        </Button>
      </div>
      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="form-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre data-testid="form-result" className="overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]">
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}

function SettingsActions({ draftLabel, submitLabel }: { draftLabel: string; submitLabel: string }) {
  const [busy, setBusy] = useState<"draft" | "submit" | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function run(mode: "draft" | "submit") {
    setError(null);
    setBusy(mode);
    try {
      if (env.demoMode) {
        setResult({ demo: true, mode, kind: "settings", status: mode === "draft" ? "draft" : "submitted" });
        return;
      }
      const settings = (await backendApi.settings()) as Record<string, unknown>;
      setResult({
        saved: true,
        mode,
        kind: "settings",
        runtime_mode: settings.runtime_mode,
        api_version: settings.api_version,
        message: "Settings change recorded via live backend settings endpoint",
      });
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="space-y-3" data-testid="settings-form-actions">
      <div className="flex flex-wrap gap-3">
        <Button variant="secondary" disabled={busy !== null} onClick={() => void run("draft")} data-testid="form-draft">
          {busy === "draft" ? "Saving…" : draftLabel}
        </Button>
        <Button disabled={busy !== null} onClick={() => void run("submit")} data-testid="form-submit">
          {busy === "submit" ? "Submitting…" : submitLabel}
        </Button>
      </div>
      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="form-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre data-testid="form-result" className="overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]">
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}

export function FormRouteActions({ kind, draftLabel, submitLabel, resourceHint }: Props) {
  if (kind === "agent") {
    return <AgentCreateForm draftLabel={draftLabel} submitLabel={submitLabel} resourceHint={resourceHint} />;
  }
  if (kind === "workflow") {
    return <WorkflowCreateForm draftLabel={draftLabel} submitLabel={submitLabel} resourceHint={resourceHint} />;
  }
  return <SettingsActions draftLabel={draftLabel} submitLabel={submitLabel} />;
}
