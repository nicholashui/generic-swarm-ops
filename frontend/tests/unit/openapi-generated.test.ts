import { describe, expect, it } from "vitest";
import { readFileSync, existsSync } from "node:fs";
import path from "node:path";

describe("OpenAPI generation artifacts", () => {
  it("openapi.json exists and includes agent/workflow paths", () => {
    const openapiPath = path.join(process.cwd(), "openapi.json");
    expect(existsSync(openapiPath)).toBe(true);
    const doc = JSON.parse(readFileSync(openapiPath, "utf8")) as {
      paths?: Record<string, unknown>;
    };
    expect(doc.paths?.["/api/v1/agents"]).toBeTruthy();
    expect(doc.paths?.["/api/v1/workflows"]).toBeTruthy();
  });

  it("generated openapi.d.ts exports paths type", () => {
    const dts = path.join(process.cwd(), "src/lib/api/generated/openapi.d.ts");
    expect(existsSync(dts)).toBe(true);
    const src = readFileSync(dts, "utf8");
    expect(src).toContain("export interface paths");
    expect(src).toContain("/api/v1/agents");
  });
});
