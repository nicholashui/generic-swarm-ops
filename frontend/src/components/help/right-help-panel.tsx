"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { ArrowLeft, GripVertical, X } from "lucide-react";
import { MarkdownDocument } from "@/components/help/markdown-document";
import { useWorkspaceHelp } from "@/components/help/workspace-help-context";
import {
  HELP_DRAWER_MIN_WIDTH,
  helpDrawerMaxForViewport,
} from "@/lib/help/help-tabs";
import { buildDocCandidates } from "@/lib/help/resolve-doc-paths";
import { cn } from "@/lib/utils";

const KEYBOARD_STEP = 16;
const KEYBOARD_STEP_LARGE = 48;

/**
 * Right-side tabbed help drawer with a visible, draggable left-edge resize handle.
 * Also shows agent SPEC.md when opened from the roster (agentSpecFocus).
 */
export function RightHelpPanel() {
  const pathname = usePathname() || "/";
  const {
    rightPanelOpen,
    setRightPanelOpen,
    rightPanelWidth,
    setRightPanelWidth,
    rightPanelDragging,
    setRightPanelDragging,
    helpTabs,
    activeTabId,
    setActiveTabId,
    agentSpecFocus,
    clearAgentSpecFocus,
  } = useWorkspaceHelp();

  const [viewportMax, setViewportMax] = useState(() => helpDrawerMaxForViewport());
  const dragRef = useRef<{ startX: number; startWidth: number } | null>(null);

  useEffect(() => {
    const onResize = () => setViewportMax(helpDrawerMaxForViewport());
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  const activeTab = helpTabs.find((t) => t.id === activeTabId) ?? helpTabs[0];

  const candidates = useMemo(() => {
    if (!activeTab) return [];
    if (activeTab.mdPath) return [activeTab.mdPath];
    return buildDocCandidates(pathname, activeTab.id);
  }, [activeTab, pathname]);

  const endDrag = useCallback(() => {
    dragRef.current = null;
    setRightPanelDragging(false);
    document.body.style.cursor = "";
    document.body.style.userSelect = "";
  }, [setRightPanelDragging]);

  const onPointerDown = useCallback(
    (event: React.PointerEvent<HTMLDivElement>) => {
      event.preventDefault();
      event.stopPropagation();
      dragRef.current = { startX: event.clientX, startWidth: rightPanelWidth };
      setRightPanelDragging(true);
      document.body.style.cursor = "col-resize";
      document.body.style.userSelect = "none";
      try {
        event.currentTarget.setPointerCapture(event.pointerId);
      } catch {
        // ignore if capture unsupported
      }
    },
    [rightPanelWidth, setRightPanelDragging],
  );

  // Drag listeners on window so resize continues even if pointer leaves the thin handle.
  useEffect(() => {
    if (!rightPanelDragging) return;

    const onMove = (event: PointerEvent) => {
      const drag = dragRef.current;
      if (!drag) return;
      // Drag left → wider panel; drag right → narrower
      const delta = drag.startX - event.clientX;
      setRightPanelWidth(drag.startWidth + delta);
    };
    const onUp = () => endDrag();

    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
    window.addEventListener("pointercancel", onUp);
    window.addEventListener("blur", onUp);
    return () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
      window.removeEventListener("blur", onUp);
    };
  }, [rightPanelDragging, setRightPanelWidth, endDrag]);

  const onKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLDivElement>) => {
      const step = event.shiftKey ? KEYBOARD_STEP_LARGE : KEYBOARD_STEP;
      const max = helpDrawerMaxForViewport();
      switch (event.key) {
        case "ArrowLeft":
          event.preventDefault();
          setRightPanelWidth(rightPanelWidth + step);
          break;
        case "ArrowRight":
          event.preventDefault();
          setRightPanelWidth(rightPanelWidth - step);
          break;
        case "Home":
          event.preventDefault();
          setRightPanelWidth(max);
          break;
        case "End":
          event.preventDefault();
          setRightPanelWidth(HELP_DRAWER_MIN_WIDTH);
          break;
        default:
          break;
      }
    },
    [rightPanelWidth, setRightPanelWidth],
  );

  if (!rightPanelOpen) return null;

  const showingAgent = Boolean(agentSpecFocus);

  return (
    <aside
      className={cn(
        "relative flex h-full min-h-0 shrink-0 flex-col overflow-hidden border-l border-white/10 bg-[rgba(4,10,18,0.96)]",
        !rightPanelDragging && "transition-[width] duration-150 ease-out",
      )}
      style={{ width: rightPanelWidth, minWidth: HELP_DRAWER_MIN_WIDTH, maxWidth: viewportMax }}
      data-testid="help-right-panel"
      aria-label={showingAgent ? "Agent specification panel" : "Help documentation panel"}
    >
      {/* Visible resize grip on the left edge */}
      <div
        role="separator"
        aria-orientation="vertical"
        aria-valuemin={HELP_DRAWER_MIN_WIDTH}
        aria-valuemax={viewportMax}
        aria-valuenow={rightPanelWidth}
        aria-label="Resize help panel. Drag left to widen, right to narrow. Arrow keys also work."
        tabIndex={0}
        data-testid="help-resize-handle"
        className={cn(
          "group absolute inset-y-0 left-0 z-20 flex w-3 -translate-x-1/2 cursor-col-resize items-center justify-center",
          "touch-none select-none outline-none",
          rightPanelDragging ? "bg-[var(--accent)]/30" : "hover:bg-[var(--accent)]/20 focus-visible:bg-[var(--accent)]/25",
        )}
        onPointerDown={onPointerDown}
        onKeyDown={onKeyDown}
        title="Drag to resize panel"
      >
        <span
          className={cn(
            "flex h-12 w-1.5 items-center justify-center rounded-full border border-white/15 bg-white/10",
            "group-hover:border-[var(--accent)]/50 group-hover:bg-[var(--accent)]/40",
            rightPanelDragging && "border-[var(--accent)] bg-[var(--accent)]",
          )}
        >
          <GripVertical className="size-3 text-white/70" aria-hidden />
        </span>
      </div>

      {rightPanelDragging ? (
        <div
          className="pointer-events-none absolute bottom-3 left-1/2 z-30 -translate-x-1/2 rounded-full border border-white/15 bg-black/80 px-3 py-1 font-[var(--font-mono)] text-xs text-white"
          data-testid="help-resize-width-badge"
        >
          {rightPanelWidth}px
        </div>
      ) : null}

      <header className="flex items-start justify-between gap-2 border-b border-white/10 px-4 py-3 pl-5">
        <div className="min-w-0">
          {showingAgent && agentSpecFocus ? (
            <>
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Agent SPEC</p>
              <p className="mt-0.5 truncate text-sm font-medium text-white">{agentSpecFocus.name}</p>
              <p className="mt-0.5 font-[var(--font-mono)] text-[10px] text-muted">
                {agentSpecFocus.agentId}
              </p>
              {agentSpecFocus.path ? (
                <p className="mt-0.5 truncate font-[var(--font-mono)] text-[10px] text-muted">
                  {agentSpecFocus.path}
                </p>
              ) : null}
            </>
          ) : (
            <>
              <p className="text-xs uppercase tracking-[0.24em] text-[var(--accent)]">Help</p>
              <p className="mt-0.5 text-sm font-medium text-white">Screen documentation</p>
              <p className="mt-0.5 text-[10px] text-muted">Drag left edge to resize</p>
            </>
          )}
        </div>
        <div className="flex shrink-0 items-center gap-1">
          {showingAgent ? (
            <button
              type="button"
              className="inline-flex size-9 items-center justify-center rounded-xl border border-white/10 bg-white/6 text-white hover:bg-white/10"
              aria-label="Back to screen documentation"
              data-testid="help-agent-spec-back"
              title="Back to screen docs"
              onClick={clearAgentSpecFocus}
            >
              <ArrowLeft className="size-4" />
            </button>
          ) : null}
          <button
            type="button"
            className="inline-flex size-9 items-center justify-center rounded-xl border border-white/10 bg-white/6 text-white hover:bg-white/10"
            aria-label="Close help panel"
            data-testid="help-drawer-close"
            onClick={() => setRightPanelOpen(false)}
          >
            <X className="size-4" />
          </button>
        </div>
      </header>

      {!showingAgent ? (
        <div
          className="flex gap-1 overflow-x-auto border-b border-white/10 px-2 py-2"
          role="tablist"
          aria-label="Document types"
        >
          {helpTabs.map((tab) => {
            const selected = tab.id === activeTabId;
            return (
              <button
                key={tab.id}
                type="button"
                role="tab"
                aria-selected={selected}
                data-testid={`help-tab-${tab.id}`}
                className={cn(
                  "rounded-xl px-3 py-1.5 text-xs font-medium transition",
                  selected
                    ? "bg-white/12 text-white"
                    : "text-muted hover:bg-white/6 hover:text-white",
                )}
                onClick={() => setActiveTabId(tab.id)}
              >
                {tab.label}
              </button>
            );
          })}
        </div>
      ) : null}

      <div
        className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden overscroll-contain scrollbar-thin"
        role="tabpanel"
        data-testid="help-panel-scroll"
      >
        {showingAgent && agentSpecFocus ? (
          <div className="p-4" data-testid="help-agent-spec-body">
            {agentSpecFocus.loading ? (
              <p className="text-sm text-muted">Loading SPEC.md…</p>
            ) : null}
            {agentSpecFocus.error ? (
              <p className="text-sm text-[var(--danger)]" role="alert">
                {agentSpecFocus.error}
              </p>
            ) : null}
            {agentSpecFocus.markdown ? (
              <div className="text-sm leading-7 text-[var(--foreground)]">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({ children }) => (
                      <h1 className="mb-3 text-xl font-semibold text-white">{children}</h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="mb-2 mt-4 text-lg font-semibold text-white">{children}</h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="mb-2 mt-3 text-base font-semibold text-white">{children}</h3>
                    ),
                    p: ({ children }) => <p className="my-2">{children}</p>,
                    ul: ({ children }) => (
                      <ul className="my-2 list-disc space-y-1 pl-5">{children}</ul>
                    ),
                    ol: ({ children }) => (
                      <ol className="my-2 list-decimal space-y-1 pl-5">{children}</ol>
                    ),
                    a: ({ href, children }) => (
                      <a
                        href={href}
                        className="text-[var(--accent)] underline-offset-2 hover:underline"
                        target={href?.startsWith("http") ? "_blank" : undefined}
                        rel={href?.startsWith("http") ? "noreferrer" : undefined}
                      >
                        {children}
                      </a>
                    ),
                    code: ({ className, children, ...rest }) =>
                      className ? (
                        <code
                          className="block overflow-x-auto rounded-lg bg-black/40 p-3 font-[var(--font-mono)] text-xs text-[var(--accent-2)]"
                          {...rest}
                        >
                          {children}
                        </code>
                      ) : (
                        <code
                          className="rounded bg-white/10 px-1 font-[var(--font-mono)] text-[0.85em] text-[var(--accent-2)]"
                          {...rest}
                        >
                          {children}
                        </code>
                      ),
                  }}
                >
                  {agentSpecFocus.markdown}
                </ReactMarkdown>
              </div>
            ) : null}
          </div>
        ) : (
          <MarkdownDocument
            key={`${pathname}:${activeTabId}`}
            candidates={candidates}
            enabled={rightPanelOpen && !showingAgent}
          />
        )}
      </div>
    </aside>
  );
}
