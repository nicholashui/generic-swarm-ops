"use client";

import type { ReactNode } from "react";
import { AppHeader } from "@/components/layout/app-header";
import { Sidebar } from "@/components/layout/sidebar";
import { RightHelpPanel } from "@/components/help/right-help-panel";
import { WorkspaceHelpProvider, useWorkspaceHelp } from "@/components/help/workspace-help-context";
import type { SessionUser } from "@/types/domain";
import { cn } from "@/lib/utils";

function AppShellLayout({ user, children }: { user: SessionUser; children: ReactNode }) {
  const { rightPanelOpen, rightPanelDragging, drawerOpen, setDrawerOpen } = useWorkspaceHelp();

  return (
    // Fixed viewport height so main + help panel scroll independently (not document scroll).
    <div className="flex h-dvh max-h-dvh overflow-hidden lg:flex" data-testid="app-shell">
      <Sidebar user={user} />

      {/* Mobile left drawer owned by workspace shell */}
      {drawerOpen ? (
        <div
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          data-testid="help-mobile-nav-overlay"
          onClick={() => setDrawerOpen(false)}
        >
          <div className="h-full w-[300px]" onClick={(event) => event.stopPropagation()}>
            <div className="flex h-full flex-col overflow-hidden bg-[rgba(3,8,15,0.96)]">
              <Sidebar user={user} variant="mobile" />
            </div>
          </div>
        </div>
      ) : null}

      <div className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
        <AppHeader user={user} />
        <div
          className={cn(
            "flex min-h-0 flex-1 overflow-hidden",
            !rightPanelDragging && "transition-[padding] duration-150",
          )}
          data-testid="app-shell-body"
        >
          <main
            className={cn(
              "min-h-0 min-w-0 flex-1 overflow-y-auto overflow-x-hidden px-4 py-6 md:px-8 md:py-8",
              rightPanelOpen && "lg:pr-2",
            )}
            data-testid="app-shell-main"
          >
            {children}
          </main>
          <RightHelpPanel />
        </div>
      </div>
    </div>
  );
}

export function AppShell({ user, children }: { user: SessionUser; children: ReactNode }) {
  return (
    <WorkspaceHelpProvider>
      <AppShellLayout user={user}>{children}</AppShellLayout>
    </WorkspaceHelpProvider>
  );
}
