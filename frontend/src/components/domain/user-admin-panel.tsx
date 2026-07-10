"use client";

import { useMemo, useState } from "react";
import { Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { DataTable } from "@/components/ui/data-table";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { StatusBadge } from "@/components/ui/status-badge";
import { backendApi } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

export type UserAdminRow = {
  id: string;
  name: string;
  role: string;
  status: string;
  lastActive: string;
  email?: string;
};

const ROLES = ["viewer", "operator", "reviewer", "developer", "admin"] as const;

export function UserAdminPanel({ initialRows }: { initialRows: UserAdminRow[] }) {
  const [rows, setRows] = useState(initialRows);
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [role, setRole] = useState<string>("viewer");
  const [busy, setBusy] = useState<"invite" | string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);
  const [inviteOpen, setInviteOpen] = useState(false);

  const metrics = useMemo(() => {
    const invited = rows.filter((r) => /invit/i.test(r.status)).length;
    const active = rows.filter((r) => /active/i.test(r.status)).length;
    return { invited, active, total: rows.length };
  }, [rows]);

  async function refreshUsers() {
    if (env.demoMode) return;
    const list = (await backendApi.listUsers()) as Array<Record<string, unknown>>;
    setRows(
      list.map((row) => ({
        id: String(row.id || ""),
        name: String(row.name || row.email || ""),
        role: String(row.role || "viewer"),
        status: String(row.status || "Active"),
        lastActive: String(row.updated_at || row.created_at || "recent"),
        email: row.email ? String(row.email) : undefined,
      })),
    );
  }

  async function inviteUser() {
    setError(null);
    setResult(null);
    setBusy("invite");
    try {
      if (env.demoMode) {
        const demoId = `user_demo_${Date.now()}`;
        setRows((current) => [
          {
            id: demoId,
            name: name || email.split("@")[0] || "Invited user",
            role,
            status: "Invited",
            lastActive: "just now",
            email,
          },
          ...current,
        ]);
        setResult({ demo: true, action: "invite", email, role });
        setInviteOpen(false);
        setEmail("");
        setName("");
        return;
      }
      const invitation = (await backendApi.createInvitation({
        email: email.trim(),
        name: name.trim() || undefined,
        role,
      })) as Record<string, unknown>;
      setResult({
        action: "invite",
        invitation_id: invitation.id,
        email: invitation.email,
        role: invitation.role,
        // token shown once for ops/dev (backend returns it for local accept flow)
        token: invitation.token,
        accept_hint: invitation.token
          ? `/accept-invite?token=${encodeURIComponent(String(invitation.token))}`
          : undefined,
      });
      await refreshUsers();
      setInviteOpen(false);
      setEmail("");
      setName("");
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  async function setUserStatus(userId: string, status: "active" | "disabled") {
    setError(null);
    setResult(null);
    setBusy(userId);
    try {
      if (env.demoMode) {
        setRows((current) =>
          current.map((row) => (row.id === userId ? { ...row, status: status === "disabled" ? "Disabled" : "Active" } : row)),
        );
        setResult({ demo: true, action: "status", userId, status });
        return;
      }
      const updated = (await backendApi.updateUser(userId, { status })) as Record<string, unknown>;
      setResult({ action: "status", user: updated });
      await refreshUsers();
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(null);
    }
  }

  return (
    <div className="space-y-6" data-testid="user-admin-panel">
      <div className="grid gap-4 md:grid-cols-4">
        <Card className="p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-muted">Users</p>
          <p className="mt-2 text-2xl font-semibold text-white">{metrics.total}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-muted">Active</p>
          <p className="mt-2 text-2xl font-semibold text-white">{metrics.active}</p>
        </Card>
        <Card className="p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-muted">Invited</p>
          <p className="mt-2 text-2xl font-semibold text-white">{metrics.invited}</p>
        </Card>
        <Card className="flex items-center justify-center p-4">
          <Button
            variant="secondary"
            data-testid="invite-user-open"
            onClick={() => setInviteOpen((v) => !v)}
          >
            <Plus className="size-4" />
            Invite user
          </Button>
        </Card>
      </div>

      {inviteOpen ? (
        <Card className="space-y-4 p-5" data-testid="invite-user-form">
          <p className="text-sm font-medium text-white">Send invitation</p>
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <Label htmlFor="invite-email">Email</Label>
              <Input
                id="invite-email"
                data-testid="invite-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="ops@example.com"
              />
            </div>
            <div>
              <Label htmlFor="invite-name">Name (optional)</Label>
              <Input
                id="invite-name"
                data-testid="invite-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Alex Morgan"
              />
            </div>
            <div>
              <Label htmlFor="invite-role">Role</Label>
              <select
                id="invite-role"
                data-testid="invite-role"
                className="mt-1 w-full rounded-xl border border-white/12 bg-white/5 px-3 py-2 text-sm text-white"
                value={role}
                onChange={(e) => setRole(e.target.value)}
              >
                {ROLES.map((r) => (
                  <option key={r} value={r} className="bg-slate-900">
                    {r}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button
              data-testid="invite-user-submit"
              disabled={busy !== null || !email.trim()}
              onClick={() => void inviteUser()}
            >
              {busy === "invite" ? "Inviting…" : "Send invite"}
            </Button>
            <Button variant="secondary" disabled={busy !== null} onClick={() => setInviteOpen(false)}>
              Cancel
            </Button>
          </div>
        </Card>
      ) : null}

      <DataTable
        caption="Users"
        rows={rows}
        columns={[
          { key: "name", label: "User" },
          { key: "role", label: "Role" },
          {
            key: "status",
            label: "Status",
            render: (row) => <StatusBadge status={String(row.status).toLowerCase()} />,
          },
          { key: "lastActive", label: "Last active" },
          {
            key: "id",
            label: "Actions",
            render: (row) => {
              const disabled = /disabled/i.test(row.status);
              return (
                <div className="flex flex-wrap gap-2">
                  {disabled ? (
                    <Button
                      variant="secondary"
                      data-testid={`user-enable-${row.id}`}
                      disabled={busy !== null}
                      onClick={() => void setUserStatus(row.id, "active")}
                    >
                      {busy === row.id ? "…" : "Enable"}
                    </Button>
                  ) : (
                    <Button
                      variant="danger"
                      data-testid={`user-disable-${row.id}`}
                      disabled={busy !== null}
                      onClick={() => void setUserStatus(row.id, "disabled")}
                    >
                      {busy === row.id ? "…" : "Disable"}
                    </Button>
                  )}
                </div>
              );
            },
          },
        ]}
      />

      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="user-admin-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre
          data-testid="user-admin-result"
          className="overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]"
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}
