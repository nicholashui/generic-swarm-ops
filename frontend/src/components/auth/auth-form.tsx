"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, type Resolver } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { backendApi, setAccessToken, setFrontendSessionUser } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { AppError } from "@/lib/errors/app-error";

type AuthMode =
  | "login"
  | "register"
  | "forgot-password"
  | "reset-password"
  | "accept-invite";

type AuthField = {
  name: "name" | "organization" | "email" | "password" | "token";
  label: string;
  type: "text" | "email" | "password";
  placeholder: string;
};

type FormValues = Record<string, string>;

const schemas: Record<AuthMode, z.ZodType<FormValues>> = {
  login: z.object({
    email: z.string().email("Enter a valid email address."),
    password: z.string().min(8, "Password must be at least 8 characters."),
  }),
  register: z.object({
    name: z.string().min(2, "Name must be at least 2 characters."),
    organization: z.string().min(2, "Organization name is required."),
    email: z.string().email("Enter a valid email address."),
    password: z.string().min(8, "Password must be at least 8 characters."),
  }),
  "forgot-password": z.object({
    email: z.string().email("Enter a valid email address."),
  }),
  "reset-password": z.object({
    email: z.string().email("Enter a valid email address."),
    password: z.string().min(8, "Password must be at least 8 characters."),
  }),
  "accept-invite": z.object({
    token: z.string().min(8, "Invite token is required."),
    name: z.string().optional(),
    password: z.string().min(8, "Password must be at least 8 characters."),
  }),
};

const fieldMap: Record<AuthMode, AuthField[]> = {
  login: [
    { name: "email", label: "Email", type: "email", placeholder: "admin@example.com" },
    { name: "password", label: "Password", type: "password", placeholder: "Minimum 8 characters" },
  ],
  register: [
    { name: "name", label: "Name", type: "text", placeholder: "Alex Morgan" },
    {
      name: "organization",
      label: "Organization",
      type: "text",
      placeholder: "Northwind Operations",
    },
    { name: "email", label: "Email", type: "email", placeholder: "ops@example.com" },
    { name: "password", label: "Password", type: "password", placeholder: "Minimum 8 characters" },
  ],
  "forgot-password": [
    { name: "email", label: "Email", type: "email", placeholder: "ops@example.com" },
  ],
  "reset-password": [
    { name: "email", label: "Email", type: "email", placeholder: "ops@example.com" },
    {
      name: "password",
      label: "New password",
      type: "password",
      placeholder: "Choose a strong replacement password",
    },
  ],
  "accept-invite": [
    {
      name: "token",
      label: "Invite token",
      type: "text",
      placeholder: "Paste invite token from your invitation",
    },
    { name: "name", label: "Full name", type: "text", placeholder: "Alex Morgan" },
    {
      name: "password",
      label: "Password",
      type: "password",
      placeholder: "Set a secure password for your account",
    },
  ],
};

const submitLabels: Record<AuthMode, string> = {
  login: "Sign in",
  register: "Create account",
  "forgot-password": "Send reset email",
  "reset-password": "Reset password",
  "accept-invite": "Accept invite",
};

function formatAuthError(err: unknown): string {
  if (err instanceof AppError) {
    return err.requestId ? `${err.message} (request_id: ${err.requestId})` : err.message;
  }
  if (err instanceof Error) return err.message;
  return "Authentication failed";
}

export function AuthForm({
  mode,
  inviteToken = "",
}: {
  mode: AuthMode;
  /** Pre-filled invite token (e.g. from `?token=` on accept-invite page). */
  inviteToken?: string;
}) {
  const router = useRouter();
  const [submitted, setSubmitted] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const resolver = (zodResolver as (...args: unknown[]) => unknown)(
    schemas[mode],
  ) as Resolver<FormValues>;
  const form = useForm<FormValues>({
    resolver,
    defaultValues: mode === "accept-invite" ? { token: inviteToken } : {},
  });

  return (
    <form
      className="space-y-4"
      data-testid={`auth-form-${mode}`}
      onSubmit={form.handleSubmit(async (values) => {
        setError(null);
        setBusy(true);
        try {
          if (mode === "login" && !env.demoMode) {
            const result = await backendApi.login(values.email, values.password);
            setAccessToken(result.access_token);
            const user = result.user || {
              id: "user",
              organization_id: "org_default",
              email: values.email,
              name: values.email,
              role: "admin",
            };
            setFrontendSessionUser(user as Record<string, unknown>);
            setSubmitted(
              JSON.stringify(
                {
                  live: true,
                  user,
                  token_cookie: "gso_access_token",
                  has_token: Boolean(result.access_token),
                },
                null,
                2,
              ),
            );
            router.push("/app");
            router.refresh();
            return;
          }

          if (mode === "accept-invite") {
            const token = (values.token || inviteToken || "").trim();
            if (!token) {
              throw new Error("Invite token is required (open the link from your invitation).");
            }
            if (env.demoMode) {
              setSubmitted(
                JSON.stringify(
                  {
                    demo: true,
                    action: "accept-invite",
                    token,
                    name: values.name || null,
                  },
                  null,
                  2,
                ),
              );
              return;
            }
            const result = await backendApi.acceptInvitation({
              token,
              password: values.password,
              name: values.name?.trim() || undefined,
            });
            if (result.access_token) {
              setAccessToken(String(result.access_token));
            }
            if (result.user && typeof result.user === "object") {
              setFrontendSessionUser(result.user as Record<string, unknown>);
            }
            setSubmitted(
              JSON.stringify(
                {
                  live: true,
                  action: "accept-invite",
                  user: result.user || null,
                  has_token: Boolean(result.access_token),
                },
                null,
                2,
              ),
            );
            router.push("/app");
            router.refresh();
            return;
          }

          setSubmitted(JSON.stringify({ demoOrPreview: true, values }, null, 2));
        } catch (err) {
          setError(formatAuthError(err));
        } finally {
          setBusy(false);
        }
      })}
    >
      {fieldMap[mode].map((field) => {
        const message = form.formState.errors[field.name]?.message;
        return (
          <div key={field.name} className="space-y-2">
            <label className="text-sm font-medium text-white" htmlFor={field.name}>
              {field.label}
            </label>
            <Input
              id={field.name}
              type={field.type}
              placeholder={field.placeholder}
              data-testid={`auth-${field.name}`}
              {...form.register(field.name)}
            />
            {typeof message === "string" ? (
              <p className="text-xs text-[var(--danger)]">{message}</p>
            ) : null}
          </div>
        );
      })}

      <Button className="w-full" type="submit" disabled={busy} data-testid="auth-submit">
        {busy ? "Working…" : submitLabels[mode]}
      </Button>

      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="auth-error">
          {error}
        </p>
      ) : null}

      {submitted ? (
        <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
          <p className="font-medium text-white">
            {env.demoMode ? "Frontend preview submission" : "Live auth response"}
          </p>
          <pre className="mt-3 overflow-x-auto rounded-xl bg-black/30 p-3 font-[var(--font-mono)] text-xs text-[var(--accent-2)]">
            {submitted}
          </pre>
        </div>
      ) : null}
    </form>
  );
}
