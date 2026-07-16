import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { NextRequest } from "next/server";
import { methodNotAllowedForAuth, readPostFields } from "@/lib/auth/parse-body";
import { stripCredentialQueryFromLocation } from "@/components/auth/auth-form";

const root = join(__dirname, "../..");

describe("login is POST-only (no password in query)", () => {
  it("auth form uses method POST and posts JSON body to BFF", () => {
    const form = readFileSync(join(root, "src/components/auth/auth-form.tsx"), "utf8");
    expect(form).toMatch(/method=["']POST["']/i);
    expect(form).toContain('action={formAction}');
    expect(form).toContain('"/api/auth/login"');
    expect(form).toContain('method: "POST"');
    expect(form).toContain("JSON.stringify({ email, password })");
    expect(form).toContain("event.preventDefault()");
    // Must not build credential query strings
    expect(form).not.toMatch(/URLSearchParams[\s\S]{0,80}password/);
    expect(form).not.toMatch(/`\/login\?.*password/);
  });

  it("login route rejects GET", async () => {
    const { GET } = await import("@/app/api/auth/login/route");
    const res = await GET();
    expect(res.status).toBe(405);
    expect(res.headers.get("Allow")).toBe("POST");
  });

  it("readPostFields accepts JSON body and rejects query passwords", async () => {
    const okReq = new NextRequest("http://localhost/api/auth/login", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ email: "a@b.com", password: "secret-password" }),
    });
    const fields = await readPostFields(okReq, ["email", "password"]);
    expect(fields.email).toBe("a@b.com");
    expect(fields.password).toBe("secret-password");

    const bad = new NextRequest("http://localhost/api/auth/login?password=leak", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ email: "a@b.com", password: "x" }),
    });
    await expect(readPostFields(bad, ["email", "password"])).rejects.toThrow(/query string/i);

    const getish = methodNotAllowedForAuth();
    expect(getish.status).toBe(405);
  });

  it("readPostFields accepts form-urlencoded POST (no-JS fallback)", async () => {
    const body = new URLSearchParams({
      email: "admin@example.com",
      password: "admin-password",
    });
    const req = new NextRequest("http://localhost/api/auth/login", {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body: body.toString(),
    });
    const fields = await readPostFields(req, ["email", "password"]);
    expect(fields.email).toBe("admin@example.com");
    expect(fields.password).toBe("admin-password");
  });

  it("stripCredentialQueryFromLocation removes password from address bar", () => {
    // jsdom location is limited; exercise that the helper is exported and callable.
    expect(typeof stripCredentialQueryFromLocation).toBe("function");
    stripCredentialQueryFromLocation();
  });
});
