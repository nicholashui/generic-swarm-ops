"use client";
import { useEffect, useMemo, useState } from "react";
import { connectWorkflowRunStream } from "@/lib/realtime/sse";
import type { WorkflowRunEvent } from "@/types/domain";
export function useRealtimeRun(runId: string, initialEvents: WorkflowRunEvent[]) { const [events, setEvents] = useState(initialEvents); const [connectionState, setConnectionState] = useState<"connecting" | "open" | "reconnecting" | "closed">("connecting"); useEffect(() => { const seen = new Set(initialEvents.map((event) => event.id)); const connection = connectWorkflowRunStream(runId, { seedEvents: initialEvents, onEvent: (event) => { if (seen.has(event.id)) return; seen.add(event.id); setEvents((current) => [...current, event]); }, onStateChange: setConnectionState }); return () => connection.close(); }, [initialEvents, runId]); return { connectionState, events: useMemo(() => [...events].sort((a, b) => a.timestamp.localeCompare(b.timestamp)), [events]) }; }
