"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { backendApi, getAccessToken } from "@/lib/api/client";
import { env } from "@/lib/config/env";
import { formatMutationError } from "@/lib/forms/create-resource-schemas";

function readOrgIdFromSession(): string | null {
  if (typeof document === "undefined") return null;
  const match = document.cookie.match(/(?:^|; )frontend_session=([^;]*)/);
  if (!match) return null;
  try {
    const user = JSON.parse(decodeURIComponent(match[1])) as { organization_id?: string };
    return user.organization_id || null;
  } catch {
    return null;
  }
}

export function OrganizationSettingsForm() {
  const [orgId, setOrgId] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [slug, setSlug] = useState("");
  const [status, setStatus] = useState("active");
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        if (env.demoMode) {
          if (!cancelled) {
            setOrgId("org_demo");
            setName("Demo Organization");
            setSlug("demo-org");
            setStatus("active");
          }
          return;
        }
        let id = readOrgIdFromSession();
        if (!id) {
          const orgs = (await backendApi.listOrganizations()) as Array<Record<string, unknown>>;
          id = orgs[0]?.id ? String(orgs[0].id) : null;
        }
        if (!id) {
          throw new Error("No organization available for this session");
        }
        const org = (await backendApi.getOrganization(id)) as Record<string, unknown>;
        if (!cancelled) {
          setOrgId(id);
          setName(String(org.name || ""));
          setSlug(String(org.slug || ""));
          setStatus(String(org.status || "active"));
        }
      } catch (err) {
        if (!cancelled) setError(formatMutationError(err));
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  async function save() {
    setError(null);
    setResult(null);
    setBusy(true);
    try {
      if (env.demoMode) {
        setResult({ demo: true, saved: true, name, slug, status });
        return;
      }
      if (!orgId) throw new Error("Organization id missing");
      if (!getAccessToken() && typeof window !== "undefined") {
        // still attempt; cookie may be server-side only on some paths
      }
      const updated = (await backendApi.updateOrganization(orgId, {
        name: name.trim() || undefined,
        slug: slug.trim() || undefined,
        status: status.trim() || undefined,
      })) as Record<string, unknown>;
      setResult({ saved: true, organization: updated });
      setName(String(updated.name || name));
      setSlug(String(updated.slug || slug));
      setStatus(String(updated.status || status));
    } catch (err) {
      setError(formatMutationError(err));
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return (
      <Card className="p-6" data-testid="org-settings-loading">
        <p className="text-sm text-muted">Loading organization…</p>
      </Card>
    );
  }

  return (
    <div className="space-y-6" data-testid="org-settings-form">
      <Card className="space-y-4 p-6">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-muted">Identity</p>
          <p className="mt-1 text-sm text-muted">Brand and naming settings validated by the backend.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <Label htmlFor="org-name">Organization name</Label>
            <Input
              id="org-name"
              data-testid="org-name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Northwind Operations"
            />
          </div>
          <div>
            <Label htmlFor="org-slug">Slug</Label>
            <Input
              id="org-slug"
              data-testid="org-slug"
              value={slug}
              onChange={(e) => setSlug(e.target.value)}
              placeholder="northwind-ops"
            />
          </div>
          <div>
            <Label htmlFor="org-status">Status</Label>
            <Input
              id="org-status"
              data-testid="org-status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              placeholder="active"
            />
          </div>
          <div>
            <Label>Organization id</Label>
            <Input value={orgId || ""} readOnly className="opacity-70" data-testid="org-id" />
          </div>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button data-testid="org-save" disabled={busy || !orgId} onClick={() => void save()}>
            {busy ? "Saving…" : "Save organization"}
          </Button>
        </div>
      </Card>
      {error ? (
        <p className="text-sm text-[var(--danger)]" data-testid="org-settings-error">
          {error}
        </p>
      ) : null}
      {result ? (
        <pre
          data-testid="org-settings-result"
          className="overflow-x-auto rounded-xl bg-black/30 p-3 text-xs text-[var(--accent-2)]"
        >
          {JSON.stringify(result, null, 2)}
        </pre>
      ) : null}
    </div>
  );
}
