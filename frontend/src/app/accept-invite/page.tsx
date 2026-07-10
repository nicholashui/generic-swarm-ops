import Link from "next/link";
import { Suspense } from "react";
import { AuthCardPage } from "@/components/auth/auth-card-page";
import { AcceptInviteForm } from "@/components/auth/accept-invite-form";

export default function AcceptInvitePage() {
  return (
    <AuthCardPage
      eyebrow="Invitation"
      title="Join your organization workspace"
      description="Accept the invite, set your profile credentials, and enter the shared automation environment with the correct role."
      footer={
        <div className="flex items-center justify-between gap-3">
          <span>Invite already accepted?</span>
          <Link className="hover:text-white" href="/login">
            Continue to sign in
          </Link>
        </div>
      }
    >
      <Suspense fallback={<p className="text-sm text-muted">Loading invite form…</p>}>
        <AcceptInviteForm />
      </Suspense>
    </AuthCardPage>
  );
}
