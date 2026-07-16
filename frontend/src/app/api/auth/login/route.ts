import { NextResponse } from "next/server";
import { toSessionCookieUser } from "@/lib/auth/cookies";
import { methodNotAllowedForAuth, readPostFields } from "@/lib/auth/parse-body";
import { applyAuthCookies, resolveCookieSecure } from "@/lib/auth/session-cookies";
import { backendApiBaseUrl } from "@/lib/config/env";

/**
 * Same-origin login BFF — POST only.
 * Credentials must be in the request body (JSON or form), never in the URL.
 * Sets httpOnly access token + session cookie.
 */
export async function GET() {
  return methodNotAllowedForAuth();
}

export async function POST(request: Request) {
  let fields: Record<string, string>;
  try {
    fields = await readPostFields(request, ["email", "password"]);
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

  const email = String(fields.email || "").trim();
  const password = String(fields.password || "");
  if (!email || !password) {
    return NextResponse.json(
      { error: { message: "Email and password are required", code: "validation_error" } },
      { status: 400 },
    );
  }

  const apiBase = backendApiBaseUrl();
  const wantsHtml =
    (request.headers.get("accept") || "").includes("text/html") ||
    !(request.headers.get("content-type") || "").includes("application/json");

  let upstream: Response;
  try {
    upstream = await fetch(`${apiBase}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ email, password }),
      cache: "no-store",
    });
  } catch (err) {
    const detail = err instanceof Error ? err.message : "unknown";
    return NextResponse.json(
      {
        error: {
          message: `Cannot reach backend at ${apiBase} (${detail}). Start uvicorn on port 8000.`,
          code: "backend_unreachable",
        },
      },
      { status: 502 },
    );
  }

  const payload = (await upstream.json().catch(() => ({}))) as {
    access_token?: string;
    refresh_token?: string;
    user?: Record<string, unknown>;
    error?: { message?: string; code?: string };
    detail?: string;
  };

  if (!upstream.ok) {
    const message =
      payload.error?.message ||
      (typeof payload.detail === "string" ? payload.detail : null) ||
      upstream.statusText ||
      "Login failed";
    if (wantsHtml) {
      // Native form POST without JS — bounce back to login with generic error (no password echo).
      return NextResponse.redirect(new URL("/login?error=auth", request.url), 303);
    }
    return NextResponse.json(
      {
        error: {
          message,
          code: payload.error?.code || "login_failed",
        },
      },
      { status: upstream.status },
    );
  }

  const accessToken = payload.access_token;
  if (!accessToken) {
    return NextResponse.json(
      { error: { message: "Backend login response missing access_token", code: "invalid_response" } },
      { status: 502 },
    );
  }

  const sessionUser = toSessionCookieUser(payload.user || {}, email);
  const secure = resolveCookieSecure(request.url);

  if (wantsHtml) {
    const response = NextResponse.redirect(new URL("/app", request.url), 303);
    applyAuthCookies(response, accessToken, sessionUser, { secure });
    return response;
  }

  const response = NextResponse.json({
    ok: true,
    user: sessionUser,
  });
  applyAuthCookies(response, accessToken, sessionUser, { secure });
  return response;
}
