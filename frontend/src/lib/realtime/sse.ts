import { env } from "@/lib/config/env";
import type { WorkflowRunEvent } from "@/types/domain";

export function connectWorkflowRunStream(runId: string, handlers: { onEvent: (event: WorkflowRunEvent) => void; onStateChange?: (state: "connecting" | "open" | "reconnecting" | "closed") => void; seedEvents?: WorkflowRunEvent[] }) {
  if (typeof window === "undefined" || env.demoMode) {
    handlers.onStateChange?.("open");
    const timers = (handlers.seedEvents || []).map((event, index) => window.setTimeout(() => handlers.onEvent(event), 450 + index * 850));
    return { close: () => { timers.forEach((timer) => window.clearTimeout(timer)); handlers.onStateChange?.("closed"); } };
  }
  handlers.onStateChange?.("connecting");
  const stream = new EventSource(`${env.apiBaseUrl}/workflow-runs/${runId}/events`, { withCredentials: true });
  stream.onopen = () => handlers.onStateChange?.("open");
  stream.onerror = () => handlers.onStateChange?.("reconnecting");
  stream.onmessage = (message) => {
    try { handlers.onEvent(JSON.parse(message.data) as WorkflowRunEvent); } catch {}
  };
  return { close: () => { stream.close(); handlers.onStateChange?.("closed"); } };
}
