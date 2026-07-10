import Link from "next/link";
import { AuthCardPage } from "@/components/auth/auth-card-page";
import { AuthForm } from "@/components/auth/auth-form";

export default function ResetPasswordPage() {
  return (
    <AuthCardPage
      eyebrow="Recovery"
      title="Complete password reset"
      description="Replace a compromised credential and return to the governed operations workspace with a secure session."
      footer={
        <div className="flex items-center justify-between gap-3">
          <span>Reset link expired?</span>
          <Link className="hover:text-white" href="/forgot-password">
            Request another email
          </Link>
        </div>
      }
    >
      <AuthForm mode="reset-password" />
    </AuthCardPage>
  );
}
