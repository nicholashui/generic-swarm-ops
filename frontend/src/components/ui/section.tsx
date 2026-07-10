import type { ReactNode } from "react";
export function Section({ eyebrow, title, description, actions, children }: { eyebrow?: string; title: string; description?: string; actions?: ReactNode; children: ReactNode }) {
  return <section className="space-y-5"><div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between"><div>{eyebrow ? <p className="text-xs uppercase tracking-[0.28em] text-[var(--accent)]">{eyebrow}</p> : null}<h1 className="mt-2 text-2xl font-semibold tracking-tight text-white md:text-3xl">{title}</h1>{description ? <p className="mt-2 max-w-3xl leading-7 text-muted">{description}</p> : null}</div>{actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}</div>{children}</section>;
}
