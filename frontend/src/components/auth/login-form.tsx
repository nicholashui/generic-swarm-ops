"use client";

import { useSearchParams } from "next/navigation";
import { AuthForm } from "@/components/auth/auth-form";

/** Client wrapper so login can read middleware `?next=` without forcing the page static. */
export function LoginForm() {
  const searchParams = useSearchParams();
  const nextPath = searchParams.get("next");
  return <AuthForm mode="login" nextPath={nextPath} />;
}
