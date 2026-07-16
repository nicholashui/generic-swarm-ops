"use client";

import { usePathname, useRouter } from "next/navigation";
import { BookOpen, PanelRight } from "lucide-react";
import { useWorkspaceHelp } from "@/components/help/workspace-help-context";
import { HELP_FULL_PAGE_BASE } from "@/lib/help/help-tabs";
import { buildDocCandidates } from "@/lib/help/resolve-doc-paths";
import { cn } from "@/lib/utils";

/**
 * Header actions:
 * 1) Full-page document navigation
 * 2) Right help drawer toggle
 */
export function HelpHeaderActions({
  fullPageBase = HELP_FULL_PAGE_BASE,
  className,
}: {
  fullPageBase?: string;
  className?: string;
}) {
  const pathname = usePathname() || "/";
  const router = useRouter();
  const { rightPanelOpen, toggleRightPanel, helpTabs } = useWorkspaceHelp();

  function openFullPageDoc() {
    const tabId = helpTabs[0]?.id || "spec";
    const [primary] = buildDocCandidates(pathname, tabId);
    const url = `${fullPageBase}?md=${encodeURIComponent(primary)}`;
    router.push(url);
  }

  return (
    <div className={cn("flex items-center gap-1", className)} data-testid="help-header-actions">
      <button
        type="button"
        className="inline-flex size-10 items-center justify-center rounded-2xl border border-white/10 bg-white/6 text-white transition hover:bg-white/10"
        aria-label="Open full-page documentation"
        title="Open documentation"
        data-testid="help-open-full-doc"
        onClick={openFullPageDoc}
      >
        <BookOpen className="size-4" />
      </button>
      <button
        type="button"
        className={cn(
          "inline-flex size-10 items-center justify-center rounded-2xl border border-white/10 transition",
          rightPanelOpen
            ? "border-[var(--accent)]/50 bg-[rgba(121,168,255,0.16)] text-[var(--accent)]"
            : "bg-white/6 text-white hover:bg-white/10",
        )}
        aria-label={rightPanelOpen ? "Close help panel" : "Open help panel"}
        aria-pressed={rightPanelOpen}
        title="Toggle help panel"
        data-testid="help-toggle-drawer"
        onClick={toggleRightPanel}
      >
        <PanelRight className="size-4" />
      </button>
    </div>
  );
}
