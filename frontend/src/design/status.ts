export const statusStyles = {
  success: "bg-[rgba(92,210,157,0.14)] text-[var(--success)] border-[rgba(92,210,157,0.32)]",
  warning: "bg-[rgba(255,209,102,0.14)] text-[var(--warning)] border-[rgba(255,209,102,0.32)]",
  danger: "bg-[rgba(255,127,143,0.14)] text-[var(--danger)] border-[rgba(255,127,143,0.32)]",
  info: "bg-[rgba(124,200,255,0.14)] text-[var(--info)] border-[rgba(124,200,255,0.32)]",
  neutral: "bg-white/6 text-white border-white/12",
  running: "bg-[rgba(124,200,255,0.14)] text-[var(--info)] border-[rgba(124,200,255,0.32)]",
  pending: "bg-[rgba(255,209,102,0.14)] text-[var(--warning)] border-[rgba(255,209,102,0.32)]",
  paused: "bg-white/8 text-muted border-white/12",
  cancelled: "bg-[rgba(255,127,143,0.14)] text-[var(--danger)] border-[rgba(255,127,143,0.32)]",
  draft: "bg-white/8 text-muted border-white/12",
  published: "bg-[rgba(92,210,157,0.14)] text-[var(--success)] border-[rgba(92,210,157,0.32)]",
} as const;

export type StatusTone = keyof typeof statusStyles;

export function mapStatusTone(status: string): StatusTone {
  const normalized = status.toLowerCase();
  if (["active", "approved", "succeeded", "healthy", "success", "published", "passed", "connected", "indexed"].includes(normalized)) return "success";
  if (["running", "indexing", "processing"].includes(normalized)) return "running";
  if (["pending", "queued", "waiting for approval", "waiting_for_approval", "warning"].includes(normalized)) return "pending";
  if (["failed", "error", "rejected"].includes(normalized)) return "danger";
  if (["cancelled", "archived", "revoked"].includes(normalized)) return "cancelled";
  if (["draft", "disabled", "inactive"].includes(normalized)) return "draft";
  if (["paused"].includes(normalized)) return "paused";
  return "neutral";
}
