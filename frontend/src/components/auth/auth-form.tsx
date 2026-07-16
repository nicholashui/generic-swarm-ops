"use client";

import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { setFrontendSessionUser } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { AppError } from "@/lib/errors/app-error";

/** Strip accidental credential query params (legacy GET mistakes) without full reload. */
export function stripCredentialQueryFromLocation(): void {
  if (typeof window === "undefined") return;
  const url = new URL(window.location.href);
  const dirtyKeys = ["password", "passwd", "secret", "email", "token"];
  let dirty = false;
  for (const key of dirtyKeys) {
    if (url.searchParams.has(key)) {
      url.searchParams.delete(key);
      dirty = true;
    }
  }
  // keep safe `next` / `error` params only
  if (dirty) {
    window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
  }
}

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
  autoComplete?: string;
};

type FormValues = {
  name?: string;
  organization?: string;
  email?: string;
  password?: string;
  token?: string;
};

const loginSchema = z.object({
  email: z.string().trim().email("Enter a valid email address."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters."),
  organization: z.string().min(2, "Organization name is required."),
  email: z.string().trim().email("Enter a valid email address."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

const forgotSchema = z.object({
  email: z.string().trim().email("Enter a valid email address."),
});

const resetSchema = z.object({
  email: z.string().trim().email("Enter a valid email address."),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

const inviteSchema = z.object({
  token: z.string().min(8, "Invite token is required."),
  name: z.string().optional(),
  password: z.string().min(8, "Password must be at least 8 characters."),
});

const schemas: Record<AuthMode, z.ZodTypeAny> = {
  login: loginSchema,
  register: registerSchema,
  "forgot-password": forgotSchema,
  "reset-password": resetSchema,
  "accept-invite": inviteSchema,
};

const fieldMap: Record<AuthMode, AuthField[]> = {
  login: [
    {
      name: "email",
      label: "Email",
      type: "email",
      placeholder: "you@company.com",
      autoComplete: "username",
    },
    {
      name: "password",
      label: "Password",
      type: "password",
      placeholder: "Your password",
      autoComplete: "current-password",
    },
  ],
  register: [
    { name: "name", label: "Name", type: "text", placeholder: "Alex Morgan", autoComplete: "name" },
    {
      name: "organization",
      label: "Organization",
      type: "text",
      placeholder: "Northwind Operations",
      autoComplete: "organization",
    },
    {
      name: "email",
      label: "Email",
      type: "email",
      placeholder: "ops@example.com",
      autoComplete: "email",
    },
    {
      name: "password",
      label: "Password",
      type: "password",
      placeholder: "Minimum 8 characters",
      autoComplete: "new-password",
    },
  ],
  "forgot-password": [
    {
      name: "email",
      label: "Email",
      type: "email",
      placeholder: "ops@example.com",
      autoComplete: "email",
    },
  ],
  "reset-password": [
    {
      name: "email",
      label: "Email",
      type: "email",
      placeholder: "ops@example.com",
      autoComplete: "email",
    },
    {
      name: "password",
      label: "New password",
      type: "password",
      placeholder: "Choose a strong replacement password",
      autoComplete: "new-password",
    },
  ],
  "accept-invite": [
    {
      name: "token",
      label: "Invite token",
      type: "text",
      placeholder: "Paste invite token from your invitation",
      autoComplete: "off",
    },
    { name: "name", label: "Full name", type: "text", placeholder: "Alex Morgan", autoComplete: "name" },
    {
      name: "password",
      label: "Password",
      type: "password",
      placeholder: "Set a secure password for your account",
      autoComplete: "new-password",
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

/** Safe in-app redirect only (blocks open redirects). */
export function safePostLoginPath(nextParam: string | null | undefined): string {
  if (!nextParam) return "/app";
  const value = nextParam.trim();
  if (!value.startsWith("/") || value.startsWith("//") || value.includes("://")) {
    return "/app";
  }
  if (!value.startsWith("/app")) {
    return "/app";
  }
  return value;
}

function formatAuthError(err: unknown): string {
  if (err instanceof AppError) {
    return err.requestId ? `${err.message} (request_id: ${err.requestId})` : err.message;
  }
  if (err instanceof TypeError) {
    return "Network error. Check that the frontend and backend are both running.";
  }
  if (err instanceof Error) return err.message;
  return "Authentication failed";
}

async function loginViaBff(email: string, password: string) {
  // Explicit POST + JSON body only — never URLSearchParams / query string.
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    credentials: "same-origin",
    body: JSON.stringify({ email, password }),
    cache: "no-store",
  });

  const payload = (await response.json().catch(() => ({}))) as {
    ok?: boolean;
    user?: Record<string, unknown>;
    error?: { message?: string; code?: string };
  };

  if (!response.ok) {
    throw new AppError(
      payload.error?.message || response.statusText || "Login failed",
      response.status,
      undefined,
      payload.error?.code,
    );
  }

  return payload as { user: Record<string, unknown> };
}

export function AuthForm({
  mode,
  inviteToken = "",
  nextPath = null,
}: {
  mode: AuthMode;
  inviteToken?: string;
  /** From middleware `?next=` — must be a relative /app path. */
  nextPath?: string | null;
}) {
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof FormValues, string>>>({});
  const [busy, setBusy] = useState(false);
  const [info, setInfo] = useState<string | null>(null);

  const form = useForm<FormValues>({
    defaultValues:
      mode === "login"
        ? { email: "", password: "" }
        : mode === "accept-invite"
          ? { token: inviteToken }
          : {},
  });

  useEffect(() => {
    stripCredentialQueryFromLocation();
  }, []);

  async function onSubmit(values: FormValues) {
    setError(null);
    setInfo(null);
    setFieldErrors({});
    // Belt-and-suspenders: never leave secrets in the address bar.
    stripCredentialQueryFromLocation();

    const parsed = schemas[mode].safeParse(values);
    if (!parsed.success) {
      const next: Partial<Record<keyof FormValues, string>> = {};
      for (const issue of parsed.error.issues) {
        const key = issue.path[0];
        if (typeof key === "string" && !next[key as keyof FormValues]) {
          next[key as keyof FormValues] = issue.message;
        }
      }
      setFieldErrors(next);
      return;
    }

    setBusy(true);
    try {
      if (mode === "login") {
        if (env.demoMode) {
          setInfo("Demo mode is on — set NEXT_PUBLIC_DEMO_MODE=false for live login.");
          return;
        }
        const data = parsed.data as { email: string; password: string };
        const result = await loginViaBff(data.email, data.password);
        if (result.user) {
          setFrontendSessionUser(result.user);
        }
        window.location.assign(safePostLoginPath(nextPath));
        return;
      }

      if (mode === "accept-invite") {
        if (env.demoMode) {
          setInfo("Demo mode: invite accept is preview-only.");
          return;
        }
        const data = parsed.data as { token: string; password: string; name?: string };
        const token = (data.token || inviteToken || "").trim();
        if (!token) throw new Error("Invite token is required.");
        const response = await fetch("/api/auth/accept-invite", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          credentials: "same-origin",
          body: JSON.stringify({
            token,
            password: data.password,
            name: data.name?.trim() || undefined,
          }),
          cache: "no-store",
        });
        const result = (await response.json().catch(() => ({}))) as {
          ok?: boolean;
          user?: Record<string, unknown>;
          error?: { message?: string; code?: string };
        };
        if (!response.ok) {
          throw new AppError(
            result.error?.message || response.statusText || "Accept invite failed",
            response.status,
            undefined,
            result.error?.code,
          );
        }
        if (result.user && typeof result.user === "object") {
          setFrontendSessionUser(result.user);
        }
        // httpOnly access token is set by the BFF Set-Cookie headers.
        window.location.assign(safePostLoginPath(nextPath));
        return;
      }

      // Honest unavailable features (not fake success)
      if (mode === "register") {
        setInfo(
          "Self-service registration is not enabled. Ask an administrator for an invite, or sign in with an existing account.",
        );
        return;
      }
      if (mode === "forgot-password" || mode === "reset-password") {
        setInfo(
          "Password reset is not available through this console yet. Contact your administrator or use the seed admin account in local development.",
        );
        return;
      }
    } catch (err) {
      setError(formatAuthError(err));
    } finally {
      setBusy(false);
    }
  }

  const unavailable =
    mode === "register" || mode === "forgot-password" || mode === "reset-password";

  // Native fallback: POST form fields to BFF (never GET). JS path uses preventDefault + JSON POST.
  const formAction =
    mode === "login"
      ? "/api/auth/login"
      : mode === "accept-invite"
        ? "/api/auth/accept-invite"
        : undefined;

  return (
    <form
      className="space-y-4"
      data-testid={`auth-form-${mode}`}
      method="POST"
      action={formAction}
      autoComplete={mode === "login" ? "on" : "off"}
      noValidate
      onSubmit={(event) => {
        // Always cancel navigation/GET; credentials only leave as POST body (JSON via fetch).
        event.preventDefault();
        event.stopPropagation();
        void form.handleSubmit(onSubmit)(event);
      }}
    >
      {mode === "login" ? (
        <div className="rounded-xl border border-white/10 bg-black/20 px-3 py-2 text-xs text-muted">
          <p>
            Passwords are sent with <strong className="text-white">HTTP POST</strong> in the request
            body only (never as query parameters).
          </p>
        </div>
      ) : null}

      {unavailable ? (
        <div
          className="rounded-xl border border-[var(--warning)]/40 bg-[rgba(255,209,102,0.08)] px-3 py-2 text-xs text-[var(--warning)]"
          data-testid="auth-unavailable-banner"
        >
          This action is not live in the current product build. The form will not create accounts or
          change passwords.
        </div>
      ) : null}

      {fieldMap[mode].map((field) => {
        const message = fieldErrors[field.name];
        return (
          <div key={field.name} className="space-y-2">
            <label className="text-sm font-medium text-white" htmlFor={field.name}>
              {field.label}
            </label>
            <Input
              id={field.name}
              type={field.type}
              placeholder={field.placeholder}
              autoComplete={field.autoComplete}
              data-testid={`auth-${field.name}`}
              disabled={busy}
              {...form.register(field.name)}
            />
            {message ? (
              <p className="text-xs text-[var(--danger)]" role="alert">
                {message}
              </p>
            ) : null}
          </div>
        );
      })}

      <Button className="w-full" type="submit" disabled={busy} data-testid="auth-submit">
        {busy ? "Working…" : submitLabels[mode]}
      </Button>

      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="auth-error" role="alert">
          {error}
        </p>
      ) : null}

      {info ? (
        <p className="text-sm text-[var(--accent-2)]" data-testid="auth-info">
          {info}
        </p>
      ) : null}
    </form>
  );
}
