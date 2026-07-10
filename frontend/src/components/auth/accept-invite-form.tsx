"use client";

import { useSearchParams } from "next/navigation";
import { AuthForm } from "@/components/auth/auth-form";

/** Client wrapper so only accept-invite reads search params (Suspense-safe). */
export function AcceptInviteForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";
  return <AuthForm mode="accept-invite" inviteToken={token} />;
}
