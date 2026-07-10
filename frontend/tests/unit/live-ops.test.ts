import { describe, expect, it } from "vitest";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { LIVE_OPS_SURFACES } from "@/lib/api/live-ops-surfaces";
import { buildWorkflowRunPayload } from "@/lib/api/workflow-run-payload";

describe("buildWorkflowRunPayload", () => {
  it("supplies case_id for onboarding-style required schema", () => {
    const payload = buildWorkflowRunPayload(
      {
        id: "wf_customer_onboarding_v12",
        input_schema: {
          type: "object",
          required: ["case_id"],
          properties: {
            case_id: { type: "string" },
            customer_name: { type: "string" },
          },
        },
      },
      { triggered_from: "frontend_run_now" },
    );
    expect(payload.case_id).toBeTruthy();
    expect(String(payload.case_id).length).toBeGreaterThan(3);
    expect(payload.triggered_from).toBe("frontend_run_now");
  });

  it("does not overwrite provided required fields", () => {
    const payload = buildWorkflowRunPayload(
      {
        input_schema: { type: "object", required: ["case_id"], properties: { case_id: { type: "string" } } },
      },
      { case_id: "fixed_case", triggered_from: "test" },
    );
    expect(payload.case_id).toBe("fixed_case");
  });
});

describe("LIVE_OPS_SURFACES manifest", () => {
  it("every surface method is used by its client component", async () => {
    for (const surface of LIVE_OPS_SURFACES) {
      const abs = path.join(process.cwd(), surface.component);
      const src = await readFile(abs, "utf8");
      expect(src, `${surface.id} missing backendApi.${surface.method}`).toContain(
        `backendApi.${surface.method}`,
      );
      // Interactive: click handlers or form submit handlers
      expect(src, `${surface.id} should be interactive`).toMatch(/onClick|onSubmit|handleSubmit/);
    }
  });
});
