"use client";

import { Search } from "lucide-react";
import { Breadcrumbs } from "@/components/layout/breadcrumbs";
import { CommandPalette } from "@/components/layout/command-palette";
import { MobileNav } from "@/components/layout/mobile-nav";
import { NotificationCenter } from "@/components/layout/notification-center";
import { OrganizationSwitcher } from "@/components/layout/organization-switcher";
import { UserMenu } from "@/components/layout/user-menu";
import { HelpHeaderActions } from "@/components/help/help-header-actions";
import type { SessionUser } from "@/types/domain";

export function AppHeader({ user }: { user: SessionUser }) {
  return (
    <>
      <header className="sticky top-0 z-20 border-b border-white/10 bg-[rgba(4,9,16,0.86)] px-4 py-4 backdrop-blur md:px-8">
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <MobileNav user={user} />
              <div className="hidden rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-muted md:flex md:min-w-[320px] md:items-center md:gap-3">
                <Search className="size-4 text-[var(--accent)]" />
                <span>Press Cmd/Ctrl + K for actions</span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <HelpHeaderActions />
              <OrganizationSwitcher />
              <NotificationCenter />
              <UserMenu user={user} />
            </div>
          </div>
          <Breadcrumbs />
        </div>
      </header>
      <CommandPalette />
    </>
  );
}
