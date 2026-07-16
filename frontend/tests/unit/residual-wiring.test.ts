import { describe, expect, it } from "vitest";
import { readFile } from "node:fs/promises";
import path from "node:path";

async function readSrc(rel: string) {
  return readFile(path.join(process.cwd(), rel), "utf8");
}

describe("residual FE wiring (T-05-05, T-11-06, T-16-02, T-16-03)", () => {
  it("accept-invite uses same-origin BFF that sets httpOnly session cookies", async () => {
    const form = await readSrc("src/components/auth/auth-form.tsx");
    const bff = await readSrc("src/app/api/auth/accept-invite/route.ts");
    expect(form).toContain('fetch("/api/auth/accept-invite"');
    expect(form).toContain("accept-invite");
    expect(bff).toContain("users/invitations/accept");
    expect(bff).toContain("applyAuthCookies");
  });

  it("run console exposes pause/resume/expire lifecycle actions", async () => {
    const client = await readSrc("src/lib/api/client.ts");
    const consoleSrc = await readSrc("src/components/domain/workflow-run-console.tsx");
    expect(client).toContain("pauseWorkflowRun");
    expect(client).toContain("resumeWorkflowRun");
    expect(client).toContain("expireWorkflowRun");
    expect(consoleSrc).toContain("backendApi.pauseWorkflowRun");
    expect(consoleSrc).toContain("backendApi.resumeWorkflowRun");
    expect(consoleSrc).toContain("backendApi.expireWorkflowRun");
    expect(consoleSrc).toContain('data-testid="run-pause"');
    expect(consoleSrc).toContain('data-testid="run-resume"');
    expect(consoleSrc).toContain('data-testid="run-expire"');
  });

  it("user admin panel invites and disables via backend APIs", async () => {
    const client = await readSrc("src/lib/api/client.ts");
    const panel = await readSrc("src/components/domain/user-admin-panel.tsx");
    expect(client).toContain("createInvitation");
    expect(client).toContain("updateUser");
    expect(panel).toContain("backendApi.createInvitation");
    expect(panel).toContain("backendApi.updateUser");
    expect(panel).toContain("invite-user-submit");
  });

  it("organization settings form patches organizations", async () => {
    const client = await readSrc("src/lib/api/client.ts");
    const form = await readSrc("src/components/domain/organization-settings-form.tsx");
    expect(client).toContain("updateOrganization");
    expect(client).toMatch(/PATCH/);
    expect(form).toContain("backendApi.updateOrganization");
    expect(form).toContain('data-testid="org-save"');
  });
});
