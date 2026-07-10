import type { ReactNode } from "react";
export function EmptyState({ title, description, action }: { title: string; description: string; action?: ReactNode }) {
  return <div className="rounded-[24px] border border-dashed border-white/12 bg-white/4 px-6 py-12 text-center"><h3 className="text-lg font-semibold text-white">{title}</h3><p className="mx-auto mt-3 max-w-xl leading-7 text-muted">{description}</p>{action ? <div className="mt-6 flex justify-center">{action}</div> : null}</div>;
}
