import { Suspense } from "react";
import Link from "next/link";
import { AuthCardPage } from "@/components/auth/auth-card-page";
import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <AuthCardPage
      eyebrow="Sign in"
      title="Operations console"
      description="Sign in with your organization account to access governed workflows, approvals, and audit visibility."
      footer={
        <div className="flex items-center justify-between gap-3">
          <Link className="hover:text-white" href="/forgot-password">
            Forgot password?
          </Link>
          <Link className="hover:text-white" href="/register">
            Create account
          </Link>
        </div>
      }
    >
      <Suspense fallback={<p className="text-sm text-muted">Loading sign-in…</p>}>
        <LoginForm />
      </Suspense>
    </AuthCardPage>
  );
}
