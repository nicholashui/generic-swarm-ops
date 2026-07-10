import { DataTable } from "@/components/ui/data-table";
import { StatusBadge } from "@/components/ui/status-badge";
import type { ApiKeyRecord } from "@/types/domain";
export function ApiKeyTable({ rows }: { rows: ApiKeyRecord[] }) { return <DataTable caption="API keys" rows={rows} columns={[{ key: "name", label: "Key name" }, { key: "maskedValue", label: "Masked value" }, { key: "createdAt", label: "Created" }, { key: "lastUsed", label: "Last used" }, { key: "status", label: "Status", render: (row) => <StatusBadge status={row.status} /> }]} />; }
