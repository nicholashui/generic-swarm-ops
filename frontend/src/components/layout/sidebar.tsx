"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { hasPermission } from "@/lib/auth/permissions";
import { cn } from "@/lib/utils";
import type { SessionUser } from "@/types/domain";
import { NAVIGATION_GROUPS } from "@/types/navigation";

export function Sidebar({
  user,
  variant = "desktop",
}: {
  user: SessionUser;
  /** desktop: hidden below lg; mobile: always flex for drawer overlay */
  variant?: "desktop" | "mobile";
}) {
  const pathname = usePathname();
  return (
    <aside
      className={cn(
        "h-full min-h-0 w-[280px] shrink-0 flex-col overflow-y-auto overflow-x-hidden border-r border-white/10 bg-[rgba(3,8,15,0.72)] px-4 py-5 scrollbar-thin",
        variant === "desktop" ? "hidden lg:flex" : "flex",
      )}
    >
      <div className="rounded-[22px] border border-white/10 bg-white/4 px-4 py-4">
        <p className="text-xs uppercase tracking-[0.28em] text-[var(--accent)]">Generic Swarm Ops</p>
        <p className="mt-3 text-sm leading-7 text-muted">
          Enterprise operations surface for agents, workflows, approvals, knowledge, and audit
          visibility.
        </p>
      </div>
      <div className="mt-6 flex-1 space-y-6 overflow-y-auto pr-1 scrollbar-thin">
        {NAVIGATION_GROUPS.map((group) => {
          const visibleItems = group.items.filter((item) =>
            item.permissions.some((permission) => hasPermission(user.role, permission)),
          );
          if (!visibleItems.length) return null;
          return (
            <div key={group.title}>
              <p className="px-3 text-xs uppercase tracking-[0.24em] text-muted">{group.title}</p>
              <div className="mt-2 space-y-1">
                {visibleItems.map((item) => {
                  const active =
                    pathname === item.href || pathname.startsWith(`${item.href}/`);
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={cn(
                        "flex items-center gap-3 rounded-2xl px-3 py-3 text-sm transition",
                        active
                          ? "bg-white/10 text-white"
                          : "text-muted hover:bg-white/6 hover:text-white",
                      )}
                    >
                      <item.icon className="size-4" />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </aside>
  );
}
