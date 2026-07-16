/**
 * Auth contract tests — drive shipped modules for login/logout/cookies/redirects.
 */
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";
import {
  ACCESS_TOKEN_COOKIE,
  SESSION_COOKIE,
  parseSessionCookieValue,
  toSessionCookieUser,
} from "@/lib/auth/cookies";
import { safePostLoginPath } from "@/components/auth/auth-form";
import { clearClientSession, logoutViaBff } from "@/lib/api/client";

const root = join(__dirname, "../..");

function readSrc(rel: string): string {
  return readFileSync(join(root, rel), "utf8");
}

describe("auth cookie contract (shipped)", () => {
  it("middleware guards /app using the same cookie names as cookies.ts", () => {
    const mw = readSrc("middleware.ts");
    expect(mw).toContain("ACCESS_TOKEN_COOKIE");
    expect(mw).toContain("SESSION_COOKIE");
    expect(mw).toContain('pathname.startsWith("/app")');
    expect(ACCESS_TOKEN_COOKIE).toBe("gso_access_token");
    expect(SESSION_COOKIE).toBe("frontend_session");
  });

  it("login and accept-invite BFFs applyAuthCookies (httpOnly access token)", () => {
    const login = readSrc("src/app/api/auth/login/route.ts");
    const accept = readSrc("src/app/api/auth/accept-invite/route.ts");
    const logout = readSrc("src/app/api/auth/logout/route.ts");
    expect(login).toContain("applyAuthCookies");
    expect(accept).toContain("applyAuthCookies");
    expect(accept).toContain("users/invitations/accept");
    expect(logout).toContain("clearAuthCookies");
  });

  it("accept-invite form uses same-origin BFF not direct backendApi", () => {
    const form = readSrc("src/components/auth/auth-form.tsx");
    expect(form).toContain('fetch("/api/auth/accept-invite"');
    expect(form).not.toMatch(/acceptInvitation\(/);
  });

  it("login form posts same-origin BFF and supports next path helper", () => {
    const form = readSrc("src/components/auth/auth-form.tsx");
    expect(form).toContain('fetch("/api/auth/login"');
    expect(form).toContain("event.preventDefault()");
    expect(form).toMatch(/method=["']POST["']/i);
    expect(form).not.toMatch(/password:\s*["']admin-password["']/);
    expect(safePostLoginPath("/app/workflows")).toBe("/app/workflows");
    expect(safePostLoginPath("/app/evolution")).toBe("/app/evolution");
    expect(safePostLoginPath("https://evil.example")).toBe("/app");
    expect(safePostLoginPath("//evil.example")).toBe("/app");
    expect(safePostLoginPath("/login")).toBe("/app");
    expect(safePostLoginPath(null)).toBe("/app");
  });

  it("loadProductBundle redirects on 401/403 instead of crashing the tree", () => {
    const data = readSrc("src/lib/data/product-data.ts");
    expect(data).toContain('redirect("/login")');
    expect(data).toContain("err.status === 401 || err.status === 403");
  });

  it("parseSessionCookieValue accepts JSON session payloads", () => {
    const user = toSessionCookieUser({
      id: "user_admin",
      email: "admin@example.com",
      name: "Admin",
      role: "admin",
      organization_id: "org_default",
    });
    const raw = JSON.stringify(user);
    const parsed = parseSessionCookieValue(raw);
    expect(parsed?.email).toBe("admin@example.com");
    expect(parsed?.id).toBe("user_admin");
  });

  it("LessonUtilityPanel is loaded where used (static or dynamic import)", () => {
    const page = readSrc("src/app/app/[...slug]/page.tsx");
    expect(page).toContain("LessonUtilityPanel");
    expect(page).toMatch(
      /lesson-utility-panel/,
    );
  });

  it("UserMenu wires Sign out to logoutViaBff /api/auth/logout", () => {
    const userMenu = readSrc("src/components/layout/user-menu.tsx");
    const logoutBff = readSrc("src/app/api/auth/logout/route.ts");
    expect(userMenu).toMatch(/Sign out|sign-out/i);
    expect(userMenu).toContain("logoutViaBff");
    expect(userMenu).toContain('data-testid="sign-out"');
    expect(logoutBff).toContain("ACCESS_TOKEN_COOKIE");
    expect(logoutBff).toContain("auth/logout");
    expect(logoutBff).toContain("clearAuthCookies");
  });

  it("home page does not link unauthenticated users to bare /app", () => {
    const home = readSrc("src/app/page.tsx");
    expect(home).not.toMatch(/href=["']\/app["']/);
    expect(home).toContain('href="/login"');
  });

  it("browser API defaults to same-origin proxy", () => {
    const envSrc = readSrc("src/lib/config/env.ts");
    expect(envSrc).toContain('"/api/proxy"');
    expect(envSrc).toContain("browserApiBaseUrl");
    const proxy = readSrc("src/app/api/proxy/[...path]/route.ts");
    expect(proxy).toContain("ACCESS_TOKEN_COOKIE");
    expect(proxy).toContain("authorization");
  });
});

describe("logoutViaBff (shipped entry)", () => {
  it("POSTs /api/auth/logout and clears client session state", async () => {
    const calls: Array<{ url: string; init?: RequestInit }> = [];
    const originalFetch = globalThis.fetch;
    globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      calls.push({ url, init });
      return new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      });
    }) as typeof fetch;

    try {
      clearClientSession();
      await logoutViaBff();
      expect(calls.length).toBe(1);
      expect(calls[0].url).toContain("/api/auth/logout");
      expect(calls[0].init?.method).toBe("POST");
    } finally {
      globalThis.fetch = originalFetch;
    }
  });
});
