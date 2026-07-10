"use client";
import { useNotificationStore } from "@/stores/notification-store";
export function useToast() { const push = useNotificationStore((state) => state.push); return { success: (title: string, description: string) => push({ id: crypto.randomUUID(), title, description }) }; }
