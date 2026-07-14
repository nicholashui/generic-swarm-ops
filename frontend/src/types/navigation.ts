import type { LucideIcon } from "lucide-react";
import {
  Activity,
  Bot,
  BrainCircuit,
  Database,
  FileKey2,
  LayoutDashboard,
  Layers,
  Shield,
  ShieldAlert,
  Sparkles,
  Users,
  Waypoints,
  Wrench,
} from "lucide-react";
import { appPaths } from "@/lib/routes/paths";
import type { Permission } from "./permissions";

export type NavigationItem = { label: string; href: string; icon: LucideIcon; permissions: Permission[] };
export type NavigationGroup = { title: string; items: NavigationItem[] };

export const NAVIGATION_GROUPS: NavigationGroup[] = [
  { title: "Main", items: [
    { label: "Dashboard", href: appPaths.dashboard, icon: LayoutDashboard, permissions: ["workflows:read"] },
    { label: "Agents", href: appPaths.agents, icon: Bot, permissions: ["agents:read"] },
    { label: "Domains", href: appPaths.domains, icon: Layers, permissions: ["workflows:read"] },
    { label: "Tools", href: appPaths.tools, icon: Wrench, permissions: ["tools:read"] },
    { label: "Workflows", href: appPaths.workflows, icon: Waypoints, permissions: ["workflows:read"] },
    { label: "Approvals", href: appPaths.approvals, icon: ShieldAlert, permissions: ["approvals:read"] },
  ]},
  { title: "Data", items: [
    { label: "Knowledge", href: "/app/knowledge", icon: Database, permissions: ["knowledge:read"] },
    { label: "Memory", href: "/app/memory", icon: BrainCircuit, permissions: ["memory:read"] },
  ]},
  { title: "Quality", items: [
    { label: "Evaluations", href: "/app/evaluations", icon: Activity, permissions: ["evaluations:read"] },
    { label: "Processes", href: "/app/processes", icon: Activity, permissions: ["processes:read"] },
    { label: "Evolution", href: "/app/evolution", icon: Sparkles, permissions: ["workflows:read"] },
  ]},
  { title: "Security", items: [
    { label: "Audit Logs", href: "/app/audit-logs", icon: Shield, permissions: ["audit:read"] },
    { label: "API Keys", href: "/app/settings/api-keys", icon: FileKey2, permissions: ["settings:read"] },
  ]},
  { title: "Admin", items: [
    { label: "Users", href: "/app/settings/users", icon: Users, permissions: ["users:read"] },
    { label: "Settings", href: "/app/settings", icon: Wrench, permissions: ["settings:read"] },
  ]},
];
