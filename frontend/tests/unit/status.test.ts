import { describe, expect, it } from "vitest";
import { formatStatusLabel } from "@/lib/formatting/status";
describe("status formatting", () => {
  it("formats snake case labels", () => { expect(formatStatusLabel("waiting_for_approval")).toBe("Waiting For Approval"); });
});
