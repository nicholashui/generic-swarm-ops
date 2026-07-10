import Link from "next/link";
import { AuthCardPage } from "@/components/auth/auth-card-page";
import { AuthForm } from "@/components/auth/auth-form";

export default function ForgotPasswordPage() {
  return (
    <AuthCardPage
      eyebrow="Recovery"
      title="Request a password reset"
      description="Start a secure recovery flow without exposing account existence or internal policy details."
      footer={
        <div className="flex items-center justify-between gap-3">
          <span>Need to go back?</span>
          <Link className="hover:text-white" href="/login">
            Return to sign in
          </Link>
        </div>
      }
    >
      <AuthForm mode="forgot-password" />
    </AuthCardPage>
  );
}
