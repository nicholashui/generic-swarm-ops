"use client";

import { Menu } from "lucide-react";
import { useWorkspaceHelpOptional } from "@/components/help/workspace-help-context";
import type { SessionUser } from "@/types/domain";

/**
 * Mobile nav trigger. When inside WorkspaceHelpProvider, uses shell-owned drawer state.
 * Falls back to no-op outside the provider (should not happen in app shell).
 */
export function MobileNav({ user: _user }: { user: SessionUser }) {
  const help = useWorkspaceHelpOptional();

  return (
    <button
      className="inline-flex size-11 items-center justify-center rounded-2xl border border-white/10 bg-white/6 text-white lg:hidden"
      type="button"
      aria-label="Open navigation"
      data-testid="mobile-nav-open"
      onClick={() => help?.setDrawerOpen(true)}
    >
      <Menu className="size-5" />
    </button>
  );
}
