import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import path from "node:path";

describe("Improve → evaluate → canary UI wiring", () => {
  it("ImproveRunButton exposes full guided pipeline actions", () => {
    const src = readFileSync(
      path.join(process.cwd(), "src/components/domain/improve-run-button.tsx"),
      "utf8",
    );
    expect(src).toContain("backendApi.reflectRun");
    expect(src).toContain("backendApi.autoProposeImprovement");
    expect(src).toContain("backendApi.evaluateVariant");
    expect(src).toContain('promoteVariant(id, "canary")');
    expect(src).toContain("improve-full");
    expect(src).toContain("onFullPipeline");
  });

  it("Evolution archive supports eval then canary", () => {
    const src = readFileSync(
      path.join(process.cwd(), "src/components/domain/evolution-archive-panel.tsx"),
      "utf8",
    );
    expect(src).toContain("evaluateThenCanary");
    expect(src).toContain("archive-eval-canary");
    expect(src).toContain("backendApi.evolutionArchive");
  });

  it("page mounts ImproveRunButton on workflow run detail", () => {
    const src = readFileSync(path.join(process.cwd(), "src/app/app/[...slug]/page.tsx"), "utf8");
    expect(src).toContain("ImproveRunButton");
    expect(src).toContain("EvolutionArchivePanel");
    expect(src).toContain('section === "evolution"');
  });
});
