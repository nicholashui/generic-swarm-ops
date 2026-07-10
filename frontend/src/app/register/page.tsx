import Link from "next/link";
import { AuthCardPage } from "@/components/auth/auth-card-page";
import { AuthForm } from "@/components/auth/auth-form";
import { EmptyState } from "@/components/ui/empty-state";
import { env } from "@/lib/config/env";

export default function RegisterPage() {
  return (
    <AuthCardPage
      eyebrow="Registration"
      title="Create an organization account"
      description="Provision a new workspace for agent governance, workflow orchestration, and observability."
      footer={
        <div className="flex items-center justify-between gap-3">
          <span>Already have access?</span>
          <Link className="hover:text-white" href="/login">
            Return to sign in
          </Link>
        </div>
      }
    >
      {env.enableRegistration ? (
        <AuthForm mode="register" />
      ) : (
        <EmptyState
          title="Invite-only access"
          description="Public self-registration is disabled in this environment. Ask an administrator to send an invite."
        />
      )}
    </AuthCardPage>
  );
}
