import { Badge } from "@/components/ui/badge";
import { mapStatusTone, statusStyles } from "@/design/status";
import { formatStatusLabel } from "@/lib/formatting/status";
import { cn } from "@/lib/utils";
export function StatusBadge({ status }: { status: string }) { const tone = mapStatusTone(status); return <Badge className={cn(statusStyles[tone])}>{formatStatusLabel(status)}</Badge>; }
