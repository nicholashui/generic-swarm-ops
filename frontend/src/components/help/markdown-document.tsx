"use client";

import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { Components } from "react-markdown";
import { htmlImgTagsToMarkdown, resolveMarkdownAssetUrl } from "@/lib/help/resolve-doc-paths";
import { useMarkdown } from "@/lib/help/use-markdown";
import { cn } from "@/lib/utils";

export type MarkdownDocumentProps = {
  /** One or more candidate public paths (tried in order). */
  candidates: string[];
  /** When false, no fetch (idle). Default true. */
  enabled?: boolean;
  className?: string;
  emptyMessage?: string;
};

function buildComponents(markdownPath: string | null): Components {
  return {
    img: ({ src, alt, ...rest }) => {
      const resolved =
        typeof src === "string" && markdownPath
          ? resolveMarkdownAssetUrl(src, markdownPath)
          : src;
      // eslint-disable-next-line @next/next/no-img-element
      return (
        <img
          {...rest}
          src={typeof resolved === "string" ? resolved : undefined}
          alt={alt || ""}
          className="my-3 max-w-full rounded-lg border border-white/10"
        />
      );
    },
    a: ({ href, children, ...rest }) => (
      <a
        {...rest}
        href={href}
        className="text-[var(--accent)] underline-offset-2 hover:underline"
        target={href?.startsWith("http") ? "_blank" : undefined}
        rel={href?.startsWith("http") ? "noreferrer" : undefined}
      >
        {children}
      </a>
    ),
    code: ({ className, children, ...rest }) => {
      const isBlock = Boolean(className);
      if (isBlock) {
        return (
          <code className={cn("font-[var(--font-mono)] text-xs text-[var(--accent-2)]", className)} {...rest}>
            {children}
          </code>
        );
      }
      return (
        <code
          className="rounded bg-white/10 px-1.5 py-0.5 font-[var(--font-mono)] text-[0.85em] text-[var(--accent-2)]"
          {...rest}
        >
          {children}
        </code>
      );
    },
    pre: ({ children, ...rest }) => (
      <pre
        className="my-3 overflow-x-auto rounded-xl border border-white/10 bg-black/40 p-3 font-[var(--font-mono)] text-xs"
        {...rest}
      >
        {children}
      </pre>
    ),
    table: ({ children, ...rest }) => (
      <div className="my-3 overflow-x-auto">
        <table className="w-full border-collapse text-left text-sm" {...rest}>
          {children}
        </table>
      </div>
    ),
    th: ({ children, ...rest }) => (
      <th className="border border-white/15 bg-white/5 px-3 py-2 font-semibold" {...rest}>
        {children}
      </th>
    ),
    td: ({ children, ...rest }) => (
      <td className="border border-white/10 px-3 py-2 align-top" {...rest}>
        {children}
      </td>
    ),
    blockquote: ({ children, ...rest }) => (
      <blockquote
        className="my-3 border-l-2 border-[var(--accent)]/50 pl-4 text-muted italic"
        {...rest}
      >
        {children}
      </blockquote>
    ),
    h1: ({ children, ...rest }) => (
      <h1 className="mb-3 mt-4 text-2xl font-semibold text-white" {...rest}>
        {children}
      </h1>
    ),
    h2: ({ children, ...rest }) => (
      <h2 className="mb-2 mt-5 text-xl font-semibold text-white" {...rest}>
        {children}
      </h2>
    ),
    h3: ({ children, ...rest }) => (
      <h3 className="mb-2 mt-4 text-lg font-semibold text-white" {...rest}>
        {children}
      </h3>
    ),
    p: ({ children, ...rest }) => (
      <p className="my-2 leading-7 text-[var(--foreground)]" {...rest}>
        {children}
      </p>
    ),
    ul: ({ children, ...rest }) => (
      <ul className="my-2 list-disc space-y-1 pl-5 text-[var(--foreground)]" {...rest}>
        {children}
      </ul>
    ),
    ol: ({ children, ...rest }) => (
      <ol className="my-2 list-decimal space-y-1 pl-5 text-[var(--foreground)]" {...rest}>
        {children}
      </ol>
    ),
    hr: (props) => <hr className="my-6 border-white/10" {...props} />,
  };
}

/**
 * Generic markdown renderer with loading / empty / error states.
 * Used by the right help drawer and the full-page document viewer.
 */
export function MarkdownDocument({
  candidates,
  enabled = true,
  className,
  emptyMessage = "No document for this screen yet.",
}: MarkdownDocumentProps) {
  const state = useMarkdown(candidates, enabled);
  const source = useMemo(() => {
    if (!state.markdown) return "";
    return htmlImgTagsToMarkdown(state.markdown);
  }, [state.markdown]);

  const components = useMemo(
    () => buildComponents(state.resolvedPath),
    [state.resolvedPath],
  );

  if (!enabled || state.status === "idle") {
    return null;
  }

  if (state.status === "loading") {
    return (
      <div className={cn("p-4 text-sm text-muted", className)} data-testid="help-md-loading">
        Loading document…
      </div>
    );
  }

  if (state.status === "error") {
    return (
      <div className={cn("space-y-2 p-4 text-sm", className)} data-testid="help-md-error" role="alert">
        <p className="font-medium text-[var(--danger)]">Could not load document</p>
        <p className="text-muted">{state.error}</p>
        {candidates[0] ? (
          <p className="font-[var(--font-mono)] text-xs text-muted">Tried: {candidates.join(" → ")}</p>
        ) : null}
      </div>
    );
  }

  // ready
  if (!state.markdown) {
    return (
      <div className={cn("p-4 text-sm text-muted", className)} data-testid="help-md-empty">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className={cn("help-markdown p-4 text-sm", className)} data-testid="help-md-ready">
      {state.resolvedPath ? (
        <p className="mb-3 font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-muted">
          {state.resolvedPath}
        </p>
      ) : null}
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {source}
      </ReactMarkdown>
    </div>
  );
}

/**
 * Full-page markdown viewer for a single explicit path under public/.
 */
export function FullPageMarkdownDocument({
  mdPath,
  className,
}: {
  mdPath: string;
  className?: string;
}) {
  const candidates = useMemo(() => {
    if (!mdPath) return [];
    const path = mdPath.startsWith("/") ? mdPath : `/${mdPath}`;
    return [path];
  }, [mdPath]);

  return (
    <article
      className={cn(
        "surface-card mx-auto max-w-3xl rounded-[24px] border border-white/10",
        className,
      )}
      data-testid="help-full-page-doc"
    >
      <MarkdownDocument candidates={candidates} enabled={Boolean(mdPath)} />
    </article>
  );
}
