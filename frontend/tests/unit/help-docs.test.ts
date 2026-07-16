import { describe, expect, it } from "vitest";
import {
  buildDocCandidates,
  htmlImgTagsToMarkdown,
  normalizeRoutePath,
  resolveMarkdownAssetUrl,
  stripParamSegments,
} from "@/lib/help/resolve-doc-paths";
import { isSoftMissingResponse } from "@/lib/help/use-markdown";
import { DEFAULT_HELP_TABS } from "@/lib/help/help-tabs";

describe("help route → doc path resolution", () => {
  it("normalizes trailing slashes", () => {
    expect(normalizeRoutePath("/app/workflows/")).toBe("/app/workflows");
    expect(normalizeRoutePath("/")).toBe("/");
  });

  it("strips dynamic id segments for fallback paths", () => {
    expect(stripParamSegments("/app/workflows/abc-def")).toBe("/app/workflows/abc-def");
    expect(stripParamSegments("/app/workflows/42")).toBe("/app/workflows");
    expect(
      stripParamSegments("/app/workflows/550e8400-e29b-41d4-a716-446655440000"),
    ).toBe("/app/workflows");
  });

  it("builds primary and fallback doc candidates", () => {
    const candidates = buildDocCandidates("/app/workflows/99", "spec");
    expect(candidates[0]).toBe("/docs/app/workflows/99/spec.md");
    expect(candidates[1]).toBe("/docs/app/workflows/spec.md");
  });

  it("uses single candidate when no param strip needed", () => {
    const candidates = buildDocCandidates("/app/workflows", "userguide");
    expect(candidates).toEqual(["/docs/app/workflows/userguide.md"]);
  });
});

describe("markdown asset resolution", () => {
  it("resolves relative images against markdown path", () => {
    expect(resolveMarkdownAssetUrl("./assets/flow.svg", "/docs/app/workflows/spec.md")).toBe(
      "/docs/app/workflows/assets/flow.svg",
    );
    expect(resolveMarkdownAssetUrl("../shared/a.png", "/docs/app/workflows/spec.md")).toBe(
      "/docs/app/shared/a.png",
    );
  });

  it("leaves absolute and root-relative URLs unchanged", () => {
    expect(resolveMarkdownAssetUrl("https://cdn.example/x.png", "/docs/a.md")).toBe(
      "https://cdn.example/x.png",
    );
    expect(resolveMarkdownAssetUrl("/static/logo.svg", "/docs/a.md")).toBe("/static/logo.svg");
  });

  it("converts raw HTML img tags to markdown images", () => {
    const input = `Hello <img src="./a.png" alt="diagram" /> world`;
    expect(htmlImgTagsToMarkdown(input)).toBe("Hello ![diagram](./a.png) world");
  });
});

describe("soft missing document detection", () => {
  it("treats 404 and HTML shells as soft misses", () => {
    expect(isSoftMissingResponse(404, "text/plain", "")).toBe(true);
    expect(isSoftMissingResponse(200, "text/html", "<!DOCTYPE html><html><body>app</body></html>")).toBe(
      true,
    );
    expect(isSoftMissingResponse(200, "text/markdown", "# Title\n\nBody")).toBe(false);
  });
});

describe("help tabs config", () => {
  it("provides generic default tabs without business domain names", () => {
    expect(DEFAULT_HELP_TABS.map((t) => t.id)).toEqual(["spec", "user_guide"]);
    for (const tab of DEFAULT_HELP_TABS) {
      expect(tab.mdPath).toBeNull();
    }
  });
});
