"use client";
import { Bell } from "lucide-react";
import { useNotificationStore } from "@/stores/notification-store";
export function NotificationCenter() { const notifications = useNotificationStore((state) => state.notifications); return <button className="relative inline-flex size-11 items-center justify-center rounded-2xl border border-white/10 bg-white/6 text-white" type="button" aria-label="Notifications"><Bell className="size-4" />{notifications.length ? <span className="absolute right-2 top-2 inline-flex size-2 rounded-full bg-[var(--warning)]" /> : null}</button>; }
