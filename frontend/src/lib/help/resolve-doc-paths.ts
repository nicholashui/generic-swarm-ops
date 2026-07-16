/**
 * Route → markdown path resolution under public/docs.
 *
 * Candidates (in order):
 *   /docs<current-route>/<tab-id>.md
 *   /docs<route-with-params-stripped>/<tab-id>.md
 */

/** Dynamic segment tokens like [id], [...slug], [[...slug]] */
const DYNAMIC_SEGMENT = /^\[(?:\.\.\.)?[^\]]+\]$|^\[\[\.\.\.[^\]]+\]\]$/;

/**
 * Normalize a browser pathname:
 * - ensure leading slash
 * - strip trailing slash (except root)
 * - map /app prefix as-is (docs live under public/docs matching route)
 */
export function normalizeRoutePath(pathname: string): string {
  if (!pathname) return "/";
  let path = pathname.startsWith("/") ? pathname : `/${pathname}`;
  if (path.length > 1 && path.endsWith("/")) {
    path = path.slice(0, -1);
  }
  return path || "/";
}

/**
 * Build a path with dynamic-looking segments removed.
 * Heuristic: UUID, pure numeric ids, and Next-style bracket segments.
 */
export function stripParamSegments(pathname: string): string {
  const normalized = normalizeRoutePath(pathname);
  const parts = normalized.split("/").filter(Boolean);
  const kept = parts.filter((segment) => {
    if (DYNAMIC_SEGMENT.test(segment)) return false;
    // UUID
    if (/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(segment)) {
      return false;
    }
    // Long opaque ids (e.g. tok_, wf_ with version, run ids)
    if (/^[0-9a-f]{16,}$/i.test(segment)) return false;
    // Pure numbers
    if (/^\d+$/.test(segment)) return false;
    return true;
  });
  return kept.length ? `/${kept.join("/")}` : "/";
}

/**
 * Candidate markdown URLs for a tab on a given route (public URL paths).
 */
export function buildDocCandidates(pathname: string, tabId: string): string[] {
  const current = normalizeRoutePath(pathname);
  const stripped = stripParamSegments(pathname);
  const file = `${tabId}.md`;

  const primary = `/docs${current === "/" ? "" : current}/${file}`.replace(/\/{2,}/g, "/");
  const fallback = `/docs${stripped === "/" ? "" : stripped}/${file}`.replace(/\/{2,}/g, "/");

  if (primary === fallback) return [primary];
  return [primary, fallback];
}

/**
 * Resolve relative asset URLs against the markdown file path.
 * Leaves absolute and root-relative URLs unchanged.
 */
export function resolveMarkdownAssetUrl(src: string, markdownPath: string): string {
  if (!src) return src;
  if (/^(https?:|data:|blob:)/i.test(src)) return src;
  if (src.startsWith("/")) return src;

  const baseDir = markdownPath.includes("/")
    ? markdownPath.slice(0, markdownPath.lastIndexOf("/"))
    : "";
  const joined = `${baseDir}/${src}`.replace(/\/{2,}/g, "/");
  // Normalize ./ and ../
  const segments = joined.split("/");
  const out: string[] = [];
  for (const seg of segments) {
    if (!seg || seg === ".") continue;
    if (seg === "..") {
      if (out.length && out[out.length - 1] !== "") out.pop();
      continue;
    }
    out.push(seg);
  }
  return `/${out.join("/")}`.replace(/\/{2,}/g, "/");
}

/**
 * Pre-transform raw HTML <img> tags into markdown image syntax so relative
 * resolution stays consistent with standard markdown images.
 */
export function htmlImgTagsToMarkdown(markdown: string): string {
  return markdown.replace(
    /<img\b([^>]*)\/?>/gi,
    (_full, attrs: string) => {
      const srcMatch = attrs.match(/\bsrc\s*=\s*["']([^"']+)["']/i);
      const altMatch = attrs.match(/\balt\s*=\s*["']([^"']*)["']/i);
      const src = srcMatch?.[1] ?? "";
      const alt = altMatch?.[1] ?? "";
      if (!src) return "";
      return `![${alt}](${src})`;
    },
  );
}
