import { NextResponse } from "next/server";
import { toSessionCookieUser } from "@/lib/auth/cookies";
import { methodNotAllowedForAuth, readPostFields } from "@/lib/auth/parse-body";
import { applyAuthCookies, resolveCookieSecure } from "@/lib/auth/session-cookies";
import { backendApiBaseUrl } from "@/lib/config/env";

/**
 * Same-origin accept-invite BFF — POST body only (never GET query secrets).
 */
export async function GET() {
  return methodNotAllowedForAuth();
}

export async function POST(request: Request) {
  let fields: Record<string, string>;
  try {
    fields = await readPostFields(request, ["token", "password", "name"]);
  } catch (err) {
    return NextResponse.json(
      {
        error: {
          message: err instanceof Error ? err.message : "Invalid body",
          code: "bad_request",
        },
      },
      { status: 400 },
    );
  }

  const token = String(fields.token || "").trim();
  const password = String(fields.password || "");
  const name = fields.name?.trim();
  if (!token || !password) {
    return NextResponse.json(
      { error: { message: "Invite token and password are required", code: "validation_error" } },
      { status: 400 },
    );
  }

  const apiBase = backendApiBaseUrl();
  let upstream: Response;
  try {
    upstream = await fetch(`${apiBase}/users/invitations/accept`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ token, password, name: name || undefined }),
      cache: "no-store",
    });
  } catch (err) {
    const detail = err instanceof Error ? err.message : "unknown";
    return NextResponse.json(
      {
        error: {
          message: `Cannot reach backend at ${apiBase} (${detail})`,
          code: "backend_unreachable",
        },
      },
      { status: 502 },
    );
  }

  const payload = (await upstream.json().catch(() => ({}))) as {
    access_token?: string;
    user?: Record<string, unknown>;
    error?: { message?: string; code?: string };
    detail?: string;
  };

  if (!upstream.ok) {
    const message =
      payload.error?.message ||
      (typeof payload.detail === "string" ? payload.detail : null) ||
      upstream.statusText ||
      "Accept invite failed";
    return NextResponse.json(
      { error: { message, code: payload.error?.code || "accept_invite_failed" } },
      { status: upstream.status },
    );
  }

  const accessToken = payload.access_token;
  if (!accessToken) {
    return NextResponse.json(
      {
        error: {
          message: "Accept invite succeeded but no access_token was returned",
          code: "invalid_response",
        },
      },
      { status: 502 },
    );
  }

  const sessionUser = toSessionCookieUser(payload.user || {}, String(payload.user?.email || ""));
  const response = NextResponse.json({ ok: true, user: sessionUser });
  applyAuthCookies(response, accessToken, sessionUser, {
    secure: resolveCookieSecure(request.url),
  });
  return response;
}
