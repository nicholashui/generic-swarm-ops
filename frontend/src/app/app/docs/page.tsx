import Link from "next/link";
import { FullPageMarkdownDocument } from "@/components/help/markdown-document";
import { Section } from "@/components/ui/section";

type SearchParams = Promise<Record<string, string | string[] | undefined>>;

/**
 * Full-page document viewer.
 * Query: ?md=/docs/<route>/<type>.md
 */
export default async function HelpDocsPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;
  const raw = params.md;
  const mdPath = Array.isArray(raw) ? raw[0] : raw;

  return (
    <Section
      eyebrow="Documentation"
      title="Document viewer"
      description="Full-page markdown from the static docs area. Paths resolve under public/docs."
      actions={
        <Link
          href="/app"
          className="rounded-2xl border border-white/10 bg-white/6 px-4 py-2 text-sm text-white hover:bg-white/10"
        >
          Back to workspace
        </Link>
      }
    >
      {mdPath ? (
        <FullPageMarkdownDocument mdPath={mdPath} />
      ) : (
        <div
          className="surface-card rounded-[24px] border border-white/10 p-6 text-sm text-muted"
          data-testid="help-full-page-missing-param"
        >
          Provide a markdown path via the <code className="text-[var(--accent-2)]">md</code> query
          parameter, for example{" "}
          <code className="text-[var(--accent-2)]">/app/docs?md=/docs/app/workflows/spec.md</code>.
        </div>
      )}
    </Section>
  );
}
