"use client";

import { useState } from "react";
import { LogOut } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { logoutViaBff } from "@/lib/api/client";
import type { SessionUser } from "@/types/domain";

export function UserMenu({ user }: { user: SessionUser }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSignOut() {
    setError(null);
    setBusy(true);
    try {
      await logoutViaBff();
      window.location.assign("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign out failed");
      setBusy(false);
    }
  }

  return (
    <div
      className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/6 px-3 py-2"
      data-testid="user-menu"
    >
      <div className="min-w-0">
        <p className="truncate text-sm font-semibold text-white">{user.name}</p>
        <div className="mt-1 flex flex-wrap items-center gap-2">
          <span className="truncate text-xs text-muted">{user.email}</span>
          <Badge className="bg-white/10 text-[var(--accent-2)]">{user.role}</Badge>
        </div>
        {error ? (
          <p className="mt-1 text-xs text-[var(--danger)]" role="alert">
            {error}
          </p>
        ) : null}
      </div>
      <Button
        type="button"
        variant="secondary"
        className="shrink-0 px-3 py-2 text-xs"
        disabled={busy}
        data-testid="sign-out"
        onClick={() => void onSignOut()}
      >
        <LogOut className="size-3.5" />
        {busy ? "Signing out…" : "Sign out"}
      </Button>
    </div>
  );
}
