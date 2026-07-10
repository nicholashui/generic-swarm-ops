import { Badge } from "@/components/ui/badge";
import type { SessionUser } from "@/types/domain";
export function UserMenu({ user }: { user: SessionUser }) { return <div className="rounded-2xl border border-white/10 bg-white/6 px-3 py-2"><p className="text-sm font-semibold text-white">{user.name}</p><div className="mt-1 flex items-center gap-2"><span className="text-xs text-muted">{user.email}</span><Badge className="bg-white/10 text-[var(--accent-2)]">{user.role}</Badge></div></div>; }
