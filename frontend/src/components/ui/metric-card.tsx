import { ArrowUpRight } from "lucide-react";
import { Card } from "@/components/ui/card";
export function MetricCard({ label, value, delta }: { label: string; value: string; delta: string }) {
  return <Card className="p-5"><div className="flex items-start justify-between"><div><p className="text-xs uppercase tracking-[0.24em] text-muted">{label}</p><p className="mt-4 text-3xl font-semibold text-white">{value}</p></div><div className="flex size-10 items-center justify-center rounded-2xl bg-white/6 text-[var(--accent)]"><ArrowUpRight className="size-4" /></div></div><p className="mt-5 text-sm text-muted">{delta}</p></Card>;
}
