import { describe, expect, it } from "vitest";
import { hasPermission } from "@/lib/auth/permissions";
describe("permissions", () => {
  it("allows admins to read agents", () => { expect(hasPermission("admin", "agents:read")).toBe(true); });
  it("prevents viewers from updating workflows", () => { expect(hasPermission("viewer", "workflows:update")).toBe(false); });
});
