import type { ReactNode } from "react";
import { AppHeader } from "@/components/layout/app-header";
import { Sidebar } from "@/components/layout/sidebar";
import type { SessionUser } from "@/types/domain";
export function AppShell({ user, children }: { user: SessionUser; children: ReactNode }) { return <div className="min-h-screen lg:flex"><Sidebar user={user} /><div className="flex min-h-screen flex-1 flex-col"><AppHeader user={user} /><main className="flex-1 px-4 py-6 md:px-8 md:py-8">{children}</main></div></div>; }
