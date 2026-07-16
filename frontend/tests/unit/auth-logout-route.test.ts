/**
 * Exercises the shipped logout BFF route entry (POST handler).
 */
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ACCESS_TOKEN_COOKIE, SESSION_COOKIE } from "@/lib/auth/cookies";

const cookieGet = vi.fn();
const backendFetch = vi.fn();

vi.mock("next/headers", () => ({
  cookies: async () => ({
    get: (name: string) => cookieGet(name),
  }),
}));

describe("POST /api/auth/logout (shipped route)", () => {
  beforeEach(() => {
    cookieGet.mockReset();
    backendFetch.mockReset();
    globalThis.fetch = backendFetch as unknown as typeof fetch;
  });

  it("clears gso_access_token and frontend_session with maxAge 0 and revokes backend token", async () => {
    cookieGet.mockImplementation((name: string) =>
      name === ACCESS_TOKEN_COOKIE ? { value: "tok_live_session" } : undefined,
    );
    backendFetch.mockResolvedValue(
      new Response(JSON.stringify({ message: "logged_out" }), { status: 200 }),
    );

    const { POST } = await import("@/app/api/auth/logout/route");
    const response = await POST(new Request("http://127.0.0.1:3000/api/auth/logout", { method: "POST" }));
    expect(response.status).toBe(200);

    const cookies = response.cookies.getAll();
    const byName = Object.fromEntries(cookies.map((c) => [c.name, c]));
    expect(byName[ACCESS_TOKEN_COOKIE]?.value).toBe("");
    expect(byName[ACCESS_TOKEN_COOKIE]?.maxAge).toBe(0);
    expect(byName[ACCESS_TOKEN_COOKIE]?.httpOnly).toBe(true);
    expect(byName[SESSION_COOKIE]?.value).toBe("");
    expect(byName[SESSION_COOKIE]?.maxAge).toBe(0);

    expect(backendFetch).toHaveBeenCalled();
    const [url, init] = backendFetch.mock.calls[0] as [string, RequestInit];
    expect(String(url)).toContain("/auth/logout");
    expect((init.headers as Record<string, string>).Authorization).toBe(
      "Bearer tok_live_session",
    );
  });
});
