"use client";

import { useEffect, useRef, useState } from "react";

export type MarkdownStatus = "idle" | "loading" | "ready" | "error";

export type MarkdownState = {
  status: MarkdownStatus;
  markdown: string | null;
  resolvedPath: string | null;
  error: string | null;
};

type InternalMarkdownState = MarkdownState & {
  requestKey: string | null;
};

const IDLE_MARKDOWN_STATE: MarkdownState = {
  status: "idle",
  markdown: null,
  resolvedPath: null,
  error: null,
};

const LOADING_MARKDOWN_STATE: MarkdownState = {
  status: "loading",
  markdown: null,
  resolvedPath: null,
  error: null,
};

const cache = new Map<string, string>();

/** Exported for tests — clear in-memory cache. */
export function clearMarkdownCache(): void {
  cache.clear();
}

function looksLikeHtmlDocument(text: string): boolean {
  const sample = text.slice(0, 256).trim().toLowerCase();
  return (
    sample.startsWith("<!doctype html") ||
    sample.startsWith("<html") ||
    (sample.includes("<head") && sample.includes("<body"))
  );
}

/**
 * Soft miss: file not present or dev server returned HTML SPA shell.
 */
export function isSoftMissingResponse(
  status: number,
  contentType: string | null,
  body: string,
): boolean {
  if (status === 404) return true;
  if (status === 200 && looksLikeHtmlDocument(body)) return true;
  if (
    contentType &&
    /text\/html/i.test(contentType) &&
    looksLikeHtmlDocument(body)
  )
    return true;
  return false;
}

async function fetchMarkdownCandidate(
  path: string,
): Promise<
  { ok: true; text: string } | { ok: false; soft: boolean; message: string }
> {
  if (cache.has(path)) {
    return { ok: true, text: cache.get(path)! };
  }
  try {
    const response = await fetch(path, {
      method: "GET",
      credentials: "same-origin",
      headers: {
        Accept: "text/markdown, text/plain, text/*;q=0.9, */*;q=0.1",
      },
      cache: "no-store",
    });
    const contentType = response.headers.get("content-type");
    const text = await response.text();
    if (!response.ok) {
      if (isSoftMissingResponse(response.status, contentType, text)) {
        return { ok: false, soft: true, message: `Not found: ${path}` };
      }
      return {
        ok: false,
        soft: false,
        message: `HTTP ${response.status} for ${path}`,
      };
    }
    if (isSoftMissingResponse(200, contentType, text)) {
      return { ok: false, soft: true, message: `HTML fallback for ${path}` };
    }
    cache.set(path, text);
    return { ok: true, text };
  } catch (err) {
    return {
      ok: false,
      soft: false,
      message: err instanceof Error ? err.message : "Network error",
    };
  }
}

/**
 * Load the first available markdown path from candidates.
 * When `enabled` is false, stays idle and does not fetch.
 */
export function useMarkdown(
  candidates: string[],
  enabled: boolean,
): MarkdownState {
  const [state, setState] = useState<InternalMarkdownState>({
    ...IDLE_MARKDOWN_STATE,
    requestKey: null,
  });
  const requestId = useRef(0);
  const key = candidates.join("|");

  const shouldLoad = enabled && candidates.length > 0;

  useEffect(() => {
    const id = ++requestId.current;
    if (!shouldLoad) {
      const resetTask = window.setTimeout(() => {
        if (id !== requestId.current) return;
        setState({ ...IDLE_MARKDOWN_STATE, requestKey: null });
      }, 0);
      return () => {
        window.clearTimeout(resetTask);
        if (requestId.current === id) requestId.current += 1;
      };
    }

    const loadTask = window.setTimeout(() => {
      if (id !== requestId.current) return;
      setState({
        ...LOADING_MARKDOWN_STATE,
        requestKey: key,
      });

      void (async () => {
        let lastHardError: string | null = null;
        for (const path of candidates) {
          const result = await fetchMarkdownCandidate(path);
          if (id !== requestId.current) return;
          if (result.ok) {
            setState({
              status: "ready",
              markdown: result.text,
              resolvedPath: path,
              error: null,
              requestKey: key,
            });
            return;
          }
          if (!result.soft) {
            lastHardError = result.message;
            // keep trying soft misses; hard error only if all fail or last is hard
          }
        }
        if (id !== requestId.current) return;
        if (lastHardError) {
          setState({
            status: "error",
            markdown: null,
            resolvedPath: null,
            error: lastHardError,
            requestKey: key,
          });
        } else {
          // All soft misses → empty document (not a crash)
          setState({
            status: "ready",
            markdown: null,
            resolvedPath: null,
            error: null,
            requestKey: key,
          });
        }
      })();
    }, 0);

    return () => {
      window.clearTimeout(loadTask);
      if (requestId.current === id) requestId.current += 1;
    };
  }, [key, shouldLoad]); // eslint-disable-line react-hooks/exhaustive-deps -- candidates joined as key

  if (!shouldLoad) return IDLE_MARKDOWN_STATE;
  if (state.requestKey !== key) return LOADING_MARKDOWN_STATE;
  return state;
}
