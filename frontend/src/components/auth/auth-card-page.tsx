import type { ReactNode } from "react";
import { ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export function AuthCardPage(props: {
  eyebrow: string;
  title: string;
  description: string;
  footer: ReactNode;
  children: ReactNode;
}) {
  return (
    <main className="app-grid flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-md">
        <Button asChild href="/" variant="ghost" className="mb-4">
          <>
            <ArrowLeft className="size-4" />
            Back
          </>
        </Button>
        <Card className="p-8">
          <p className="text-xs uppercase tracking-[0.28em] text-[var(--accent)]">
            {props.eyebrow}
          </p>
          <h1 className="mt-3 text-2xl font-semibold text-white">{props.title}</h1>
          <p className="mt-3 leading-7 text-muted">{props.description}</p>
          <div className="mt-8">{props.children}</div>
          <div className="mt-6 border-t border-white/10 pt-5 text-sm text-muted">{props.footer}</div>
        </Card>
      </div>
    </main>
  );
}
