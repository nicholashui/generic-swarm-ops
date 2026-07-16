import { ArrowRight, ShieldCheck, Workflow, Wrench } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const features = [
  {
    title: "Operate with confidence",
    description: "Track agents, workflows, approvals, and audits from a single operational console.",
    icon: ShieldCheck,
  },
  {
    title: "Route work through governed flows",
    description: "Coordinate automation with approvals, status visibility, and role-aware actions.",
    icon: Workflow,
  },
  {
    title: "Manage the full AI toolchain",
    description: "Work across tools, knowledge, memory, and evaluations with consistent controls.",
    icon: Wrench,
  },
];

export default function Home() {
  return (
    <main className="app-grid min-h-screen px-6 py-10 md:px-10">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-7xl flex-col justify-between gap-10">
        <header className="flex flex-col gap-5 rounded-[28px] border border-white/10 bg-white/5 px-6 py-5 backdrop-blur md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.32em] text-[var(--accent)]">Generic Swarm Ops</p>
            <h1 className="mt-2 max-w-2xl text-3xl font-semibold tracking-tight text-white md:text-5xl">
              Governed AI operations for real business workflows, not demo dashboards.
            </h1>
          </div>
          <div className="flex gap-3">
            <Button asChild href="/login">
              Sign in to workspace
              <ArrowRight className="size-4" />
            </Button>
            <Button asChild href="/login" variant="secondary">
              Seed admin login
            </Button>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-[1.4fr_0.9fr]">
          <Card className="p-8">
            <p className="text-xs uppercase tracking-[0.28em] text-[var(--accent-2)]">Operational posture</p>
            <div className="mt-5 grid gap-5 md:grid-cols-3">
              <div>
                <p className="text-3xl font-semibold text-white">92</p>
                <p className="mt-2 text-muted">Frontend route surfaces are scaffolded around the hardened backend that already exists.</p>
              </div>
              <div>
                <p className="text-3xl font-semibold text-white">Live</p>
                <p className="mt-2 text-muted">Workflow run pages support SSE-oriented realtime UI patterns and request-aware error handling.</p>
              </div>
              <div>
                <p className="text-3xl font-semibold text-white">Governed</p>
                <p className="mt-2 text-muted">Approvals, audit visibility, masked secrets, and role-aware navigation are treated as first-class UX rules.</p>
              </div>
            </div>
          </Card>
          <Card className="flex flex-col justify-between gap-5 p-8">
            <div>
              <p className="text-xs uppercase tracking-[0.28em] text-[var(--accent)]">Execution note</p>
              <h2 className="mt-3 text-xl font-semibold text-white">Documented design fallback</h2>
              <p className="mt-3 text-muted">
                `frontend.md` requires OpenDesign MCP, but this execution uses a documented fallback because the `opendesign` server is not currently available in the workspace.
              </p>
            </div>
            <Button asChild href="/login" variant="ghost">
              Sign in to review the app shell
            </Button>
          </Card>
        </section>

        <section className="grid gap-5 md:grid-cols-3">
          {features.map(({ title, description, icon: Icon }) => (
            <Card key={title} className="p-6">
              <div className="flex size-11 items-center justify-center rounded-2xl bg-[rgba(121,168,255,0.16)] text-[var(--accent)]">
                <Icon className="size-5" />
              </div>
              <h2 className="mt-5 text-lg font-semibold text-white">{title}</h2>
              <p className="mt-3 leading-7 text-muted">{description}</p>
            </Card>
          ))}
        </section>
      </div>
    </main>
  );
}
