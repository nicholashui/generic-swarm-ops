import type { ReactNode } from "react";
import { Card } from "@/components/ui/card";

type Column<T> = { key: keyof T | string; label: string; render?: (row: T) => ReactNode };
export function DataTable<T extends { id: string | number }>({ rows, columns, caption }: { rows: T[]; columns: Column<T>[]; caption?: string }) {
  return <Card className="overflow-hidden p-0"><div className="overflow-x-auto"><table className="min-w-full border-collapse">{caption ? <caption className="sr-only">{caption}</caption> : null}<thead><tr className="border-b border-white/10 bg-white/4 text-left">{columns.map((column) => <th key={String(column.key)} className="px-5 py-3 text-xs font-semibold uppercase tracking-[0.2em] text-muted">{column.label}</th>)}</tr></thead><tbody>{rows.map((row) => <tr key={row.id} className="border-b border-white/6 last:border-b-0 hover:bg-white/4">{columns.map((column) => <td key={String(column.key)} className="px-5 py-4 align-top text-sm text-white">{column.render ? column.render(row) : String(row[column.key as keyof T] ?? "")}</td>)}</tr>)}</tbody></table></div></Card>;
}
