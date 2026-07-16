/**
 * Configurable document types for the help drawer / full-page viewer.
 * Keep free of product-domain hardcoding — only generic doc type ids.
 */

export type HelpTabConfig = {
  /** Stable tab key and markdown filename stem (e.g. "spec" → spec.md). */
  id: string;
  /** UI label. */
  label: string;
  /**
   * Optional precomputed path. When null, resolved from the current route at runtime.
   */
  mdPath: string | null;
};

export type HelpTab = HelpTabConfig;

/** Default document types available on every screen. */
export const DEFAULT_HELP_TABS: HelpTabConfig[] = [
  { id: "spec", label: "Spec", mdPath: null },
  { id: "user_guide", label: "User guide", mdPath: null },
];

export const HELP_FULL_PAGE_BASE = "/app/docs";

export const HELP_DRAWER_WIDTH_STORAGE_KEY = "gso.help.rightPanelWidth";
export const HELP_DRAWER_MIN_WIDTH = 280;
/** Absolute ceiling; runtime also clamps vs viewport so main area stays usable. */
export const HELP_DRAWER_MAX_WIDTH = 1400;
export const HELP_DRAWER_DEFAULT_WIDTH = 440;

/** Effective max for current viewport — allow a wide help/SPEC panel (up to ~75% vw). */
export function helpDrawerMaxForViewport(viewportWidth?: number): number {
  const vw = viewportWidth ?? (typeof window !== "undefined" ? window.innerWidth : 1280);
  // Leave at least ~280px for main content when possible.
  const leaveMain = 280;
  const byFraction = Math.floor(vw * 0.75);
  const byMain = Math.max(HELP_DRAWER_MIN_WIDTH, vw - leaveMain);
  return Math.min(HELP_DRAWER_MAX_WIDTH, Math.max(HELP_DRAWER_MIN_WIDTH, Math.min(byFraction, byMain)));
}
