"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
export function Breadcrumbs() { const pathname = usePathname(); const parts = pathname.split('/').filter(Boolean); return <nav aria-label="Breadcrumb" className="flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.18em] text-muted">{parts.map((part, index) => <div key={`${part}-${index}`} className="flex items-center gap-2">{index > 0 ? <span>/</span> : null}<Link href={`/${parts.slice(0, index + 1).join('/')}`} className="hover:text-white">{part.replace(/-/g, ' ')}</Link></div>)}</nav>; }
