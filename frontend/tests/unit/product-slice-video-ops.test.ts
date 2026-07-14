import { afterEach, describe, expect, it, vi } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const root = join(__dirname, "../../..");

describe("product slice: recommend + special skills wiring", () => {
  afterEach(() => {
    vi.resetModules();
    vi.unstubAllEnvs();
  });

  it("client exposes real API paths for archetypes, recommend, special-skills", () => {
    const clientPath = join(root, "frontend/src/lib/api/client.ts");
    const src = readFileSync(clientPath, "utf8");
    expect(src).toContain('request("/domains/video/archetypes")');
    expect(src).toContain('request("/domains/video/recommend-workflow"');
    expect(src).toContain('request("/domains/video/special-skills")');
    expect(src).toContain("recommendVideoWorkflow");
    expect(src).toContain("videoSpecialSkills");
    expect(src).toContain("videoArchetypes");
  });

  it("domains page mounts RecommendWorkflowPanel and SpecialSkillsPanel", () => {
    const page = join(root, "frontend/src/app/app/[...slug]/page.tsx");
    const src = readFileSync(page, "utf8");
    expect(src).toContain("RecommendWorkflowPanel");
    expect(src).toContain("SpecialSkillsPanel");
    expect(src).toContain("VideoN3RosterPanel");
    expect(src).toMatch(/section === ["']domains["']/);
  });

  it("sidebar navigation exposes Domains via appPaths.domains", () => {
    const navPath = join(root, "frontend/src/types/navigation.ts");
    const pathsPath = join(root, "frontend/src/lib/routes/paths.ts");
    const sidebarPath = join(root, "frontend/src/components/layout/sidebar.tsx");
    const nav = readFileSync(navPath, "utf8");
    const paths = readFileSync(pathsPath, "utf8");
    const sidebar = readFileSync(sidebarPath, "utf8");
    expect(paths).toContain('domains: "/app/domains"');
    expect(nav).toContain("appPaths");
    expect(nav).toContain("appPaths.domains");
    expect(nav).toMatch(/label:\s*["']Domains["']/);
    expect(nav).toContain("href: appPaths.domains");
    // Sidebar only maps NAVIGATION_GROUPS → Domains must be in that list to be reachable
    expect(sidebar).toContain("NAVIGATION_GROUPS");
    expect(sidebar).toContain("item.href");
  });

  it("demoMode is opt-in so default product path hits live APIs", async () => {
    vi.stubEnv("NEXT_PUBLIC_DEMO_MODE", "");
    const { env: unsetEnv } = await import("@/lib/config/env");
    expect(unsetEnv.demoMode).toBe(false);

    vi.resetModules();
    vi.stubEnv("NEXT_PUBLIC_DEMO_MODE", "false");
    const { env: falseEnv } = await import("@/lib/config/env");
    expect(falseEnv.demoMode).toBe(false);

    vi.resetModules();
    vi.stubEnv("NEXT_PUBLIC_DEMO_MODE", "true");
    const { env: trueEnv } = await import("@/lib/config/env");
    expect(trueEnv.demoMode).toBe(true);

    const envSrc = readFileSync(join(root, "frontend/src/lib/config/env.ts"), "utf8");
    expect(envSrc).toContain('NEXT_PUBLIC_DEMO_MODE === "true"');
    expect(envSrc).not.toContain('NEXT_PUBLIC_DEMO_MODE !== "false"');
  });

  it("panel components call backendApi and are not static-only tables", () => {
    const rec = readFileSync(
      join(root, "frontend/src/components/domain/recommend-workflow-panel.tsx"),
      "utf8",
    );
    const skills = readFileSync(
      join(root, "frontend/src/components/domain/special-skills-panel.tsx"),
      "utf8",
    );
    expect(rec).toContain("backendApi.recommendVideoWorkflow");
    expect(rec).toContain("data-testid=\"recommend-workflow-panel\"");
    expect(skills).toContain("backendApi.videoSpecialSkills");
    expect(skills).toContain("data-testid=\"special-skills-panel\"");
    // DEMO_* only behind demoMode — real path is the API when demo is off
    expect(rec).toMatch(/if\s*\(\s*env\.demoMode\s*\)/);
    expect(skills).toMatch(/if\s*\(\s*env\.demoMode\s*\)/);
    expect(rec).not.toMatch(/return DEMO_RESULT;\s*\n\s*}\s*\n\s*const durationSec/);
    // residuals non-claim copy present
    expect(rec.toLowerCase()).toMatch(/live media|production_ready|not claimed/);
    expect(skills.toLowerCase()).toMatch(/catalog|not live media/);
  });

  it("recommendVideoWorkflow client POSTs the real recommend-workflow path", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      expect(url).toContain("/domains/video/recommend-workflow");
      expect(init?.method).toBe("POST");
      expect(String(init?.body || "")).toContain("viral TikTok");
      return {
        ok: true,
        headers: new Headers(),
        json: async () => ({
          recommendation: {
            code: "A",
            dna_id: "wf_video_arch_a_viral_hook_v1",
            process_id: "video.arch.a.viral_hook",
            name: "Viral Hook Clip / Meme",
          },
          alternatives: [],
          confidence: 0.8,
        }),
      } as Response;
    });
    vi.stubGlobal("fetch", fetchMock);
    const { backendApi, setAccessToken } = await import("@/lib/api/client");
    setAccessToken("tok_rec");
    const out = await backendApi.recommendVideoWorkflow({
      brief: "15s viral TikTok hook about coffee",
      duration_sec: 15,
      top_k: 3,
    });
    expect((out as { recommendation?: { dna_id?: string } }).recommendation?.dna_id).toBe(
      "wf_video_arch_a_viral_hook_v1",
    );
    expect(fetchMock).toHaveBeenCalled();
  });

  it("videoSpecialSkills client GETs the real special-skills path", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      expect(url).toContain("/domains/video/special-skills");
      return {
        ok: true,
        headers: new Headers(),
        json: async () => ({
          count: 17,
          skills: Array.from({ length: 17 }, (_, i) => ({
            skill_id: `skill_${i}`,
            status: "mvp_integrated",
          })),
          registry_path: "business/video/special_skills/REGISTRY.json",
        }),
      } as Response;
    });
    vi.stubGlobal("fetch", fetchMock);
    const { backendApi, setAccessToken } = await import("@/lib/api/client");
    setAccessToken("tok_sk");
    const out = (await backendApi.videoSpecialSkills()) as { count: number; skills: unknown[] };
    expect(out.count).toBe(17);
    expect(out.skills).toHaveLength(17);
    expect(fetchMock).toHaveBeenCalled();
  });

  it("pack registry on disk still has 17 skills for API to serve", () => {
    const regPath = join(root, "business/video/special_skills/REGISTRY.json");
    expect(existsSync(regPath)).toBe(true);
    const reg = JSON.parse(readFileSync(regPath, "utf8"));
    expect(reg.skill_count).toBe(17);
    expect(Array.isArray(reg.skills)).toBe(true);
    expect(reg.skills.length).toBe(17);
  });
});
