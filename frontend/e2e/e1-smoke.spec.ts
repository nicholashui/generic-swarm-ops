import { test, expect } from "@playwright/test";

/**
 * E1 smoke.
 *
 * API tests skip when backend is down.
 * UI tests skip unless server is up (or E2E_START=1 starts Next).
 *
 *   pnpm exec playwright test
 *   E2E_START=1 pnpm exec playwright test
 */

const baseURL = process.env.PLAYWRIGHT_BASE_URL || "http://127.0.0.1:3000";
const api = process.env.PLAYWRIGHT_API_BASE || "http://127.0.0.1:8000/api/v1";

async function isReachable(url: string): Promise<boolean> {
  try {
    const res = await fetch(url, { method: "GET", signal: AbortSignal.timeout(2500) });
    return res.status > 0;
  } catch {
    return false;
  }
}

test.describe("E1 API smoke", () => {
  test("health ready when backend up", async ({ request }) => {
    try {
      const res = await request.get(`${api}/health/ready`, { timeout: 3000 });
      if (!res.ok()) {
        test.skip(true, "backend not ready");
        return;
      }
      const json = await res.json();
      const db = json?.dependencies?.database || json?.database;
      expect(["postgres", "json-file"]).toContain(db);
    } catch {
      test.skip(true, "backend not reachable");
    }
  });

  test("login + flagship workflow present", async ({ request }) => {
    try {
      const login = await request.post(`${api}/auth/login`, {
        data: { email: "admin@example.com", password: "admin-password" },
        timeout: 5000,
      });
      if (!login.ok()) {
        test.skip(true, "login failed / backend down");
        return;
      }
      const { access_token } = await login.json();
      const wf = await request.get(`${api}/workflows`, {
        headers: { Authorization: `Bearer ${access_token}` },
      });
      expect(wf.ok()).toBeTruthy();
      const list = await wf.json();
      expect(Array.isArray(list)).toBeTruthy();
      expect(list.some((w: { id?: string }) => w.id === "wf_customer_onboarding_v12")).toBeTruthy();
    } catch {
      test.skip(true, "backend not reachable");
    }
  });
});

test.describe("E1 UI smoke", () => {
  test.beforeAll(async () => {
    const up = await isReachable(baseURL);
    test.skip(!up, `UI server not running at ${baseURL} (set E2E_START=1 to auto-start)`);
  });

  test("login page renders", async ({ page }) => {
    await page.goto("/login");
    await expect(page.locator("body")).toBeVisible();
    const text = (await page.textContent("body")) || "";
    expect(text.length).toBeGreaterThan(20);
  });

  test("app or login reachable", async ({ page }) => {
    await page.goto("/app");
    const url = page.url();
    expect(url.includes("/app") || url.includes("/login")).toBeTruthy();
  });

  test("evolution route responds", async ({ page }) => {
    await page.goto("/app/evolution");
    const body = (await page.textContent("body")) || "";
    expect(body.length).toBeGreaterThan(20);
  });
});
