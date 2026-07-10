"use client";
import { Menu } from "lucide-react";
import { useState } from "react";
import { Sidebar } from "@/components/layout/sidebar";
import type { SessionUser } from "@/types/domain";
export function MobileNav({ user }: { user: SessionUser }) { const [open, setOpen] = useState(false); return <><button className="inline-flex size-11 items-center justify-center rounded-2xl border border-white/10 bg-white/6 text-white lg:hidden" type="button" aria-label="Open navigation" onClick={() => setOpen(true)}><Menu className="size-5" /></button>{open ? <div className="fixed inset-0 z-40 bg-black/60 lg:hidden" onClick={() => setOpen(false)}><div className="h-full w-[300px]" onClick={(event) => event.stopPropagation()}><Sidebar user={user} /></div></div> : null}</>; }
