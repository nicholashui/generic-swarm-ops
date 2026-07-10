import Link from "next/link";
import { AuthCardPage } from "@/components/auth/auth-card-page";
import { AuthForm } from "@/components/auth/auth-form";

export default function LoginPage() {
  return (
    <AuthCardPage
      eyebrow="Authentication"
      title="Sign in to the operations workspace"
      description="Access governed workflows, approvals, knowledge, and audit visibility from a single enterprise console."
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
      <AuthForm mode="login" />
    </AuthCardPage>
  );
}
