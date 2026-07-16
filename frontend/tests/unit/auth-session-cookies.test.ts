/**
 * Drives shipped session-cookie helpers used by login / accept-invite / logout BFFs.
 */
import { describe, expect, it } from "vitest";
import { NextResponse } from "next/server";
import { ACCESS_TOKEN_COOKIE, SESSION_COOKIE } from "@/lib/auth/cookies";
import {
  applyAuthCookies,
  clearAuthCookies,
  resolveCookieSecure,
} from "@/lib/auth/session-cookies";

function cookieMap(
  response: NextResponse,
): Record<string, { value: string; maxAge?: number; httpOnly?: boolean; secure?: boolean }> {
  const out: Record<
    string,
    { value: string; maxAge?: number; httpOnly?: boolean; secure?: boolean }
  > = {};
  for (const c of response.cookies.getAll()) {
    out[c.name] = {
      value: c.value,
      maxAge: c.maxAge,
      httpOnly: c.httpOnly,
      secure: c.secure,
    };
  }
  return out;
}

describe("session-cookies helpers (shipped BFF path)", () => {
  it("resolveCookieSecure is false on local HTTP (so cookies stick under next start)", () => {
    expect(resolveCookieSecure("http://127.0.0.1:3000/api/auth/login")).toBe(false);
    expect(resolveCookieSecure("http://localhost:3000/login")).toBe(false);
    expect(resolveCookieSecure("https://ops.example.com/api/auth/login")).toBe(true);
  });

  it("applyAuthCookies sets httpOnly access token and session without Secure on HTTP", () => {
    const res = NextResponse.json({ ok: true });
    applyAuthCookies(
      res,
      "tok_test_abc",
      {
        id: "user_1",
        organization_id: "org_default",
        email: "a@example.com",
        name: "A",
        role: "admin",
      },
      { secure: false },
    );
    const cookies = cookieMap(res);
    expect(cookies[ACCESS_TOKEN_COOKIE]?.value).toBe("tok_test_abc");
    expect(cookies[ACCESS_TOKEN_COOKIE]?.httpOnly).toBe(true);
    expect(cookies[ACCESS_TOKEN_COOKIE]?.secure).toBe(false);
    expect(cookies[ACCESS_TOKEN_COOKIE]?.maxAge).toBeGreaterThan(0);
    expect(cookies[SESSION_COOKIE]?.value).toContain("a@example.com");
    expect(cookies[SESSION_COOKIE]?.httpOnly).toBe(false);
    expect(cookies[SESSION_COOKIE]?.secure).toBe(false);
  });

  it("clearAuthCookies expires both cookies (logout BFF)", () => {
    const res = NextResponse.json({ ok: true });
    applyAuthCookies(res, "tok_to_clear", {
      id: "user_1",
      organization_id: "org_default",
      email: "a@example.com",
      name: "A",
      role: "admin",
    });
    clearAuthCookies(res);
    const cookies = cookieMap(res);
    expect(cookies[ACCESS_TOKEN_COOKIE]?.value).toBe("");
    expect(cookies[ACCESS_TOKEN_COOKIE]?.maxAge).toBe(0);
    expect(cookies[ACCESS_TOKEN_COOKIE]?.httpOnly).toBe(true);
    expect(cookies[SESSION_COOKIE]?.value).toBe("");
    expect(cookies[SESSION_COOKIE]?.maxAge).toBe(0);
  });
});
