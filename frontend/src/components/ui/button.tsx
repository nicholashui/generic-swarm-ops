import type { ComponentPropsWithoutRef, ReactNode } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";

type ButtonProps = ComponentPropsWithoutRef<"button"> & { variant?: ButtonVariant; asChild?: boolean; href?: string; children: ReactNode };
const variants: Record<ButtonVariant, string> = {
  primary: "bg-[var(--accent)] text-[#04101d] hover:bg-[#90b7ff]",
  secondary: "bg-white/8 text-white hover:bg-white/12",
  ghost: "bg-transparent text-white hover:bg-white/8",
  danger: "bg-[var(--danger)] text-[#18060a] hover:bg-[#ff96a3]",
};
export function Button({ className, variant = "primary", asChild, href, children, ...props }: ButtonProps) {
  const classes = cn("inline-flex items-center justify-center gap-2 rounded-2xl px-4 py-2.5 text-sm font-semibold transition duration-150 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]", variants[variant], className);
  if (asChild && href) return <Link className={classes} href={href}>{children}</Link>;
  return <button className={classes} {...props}>{children}</button>;
}
