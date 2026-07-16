"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  DEFAULT_HELP_TABS,
  HELP_DRAWER_DEFAULT_WIDTH,
  HELP_DRAWER_MIN_WIDTH,
  HELP_DRAWER_WIDTH_STORAGE_KEY,
  helpDrawerMaxForViewport,
  type HelpTabConfig,
} from "@/lib/help/help-tabs";

/** Content shown in the right panel when an agent SPEC is opened from the roster. */
export type AgentSpecFocus = {
  agentId: string;
  name: string;
  path?: string;
  source?: string;
  markdown?: string;
  loading: boolean;
  error?: string;
};

type WorkspaceHelpContextValue = {
  /** Mobile left nav drawer (optional shell behavior). */
  drawerOpen: boolean;
  setDrawerOpen: (open: boolean) => void;
  toggleDrawer: () => void;

  rightPanelOpen: boolean;
  setRightPanelOpen: (open: boolean) => void;
  toggleRightPanel: () => void;

  rightPanelWidth: number;
  setRightPanelWidth: (width: number) => void;
  rightPanelDragging: boolean;
  setRightPanelDragging: (dragging: boolean) => void;

  helpTabs: HelpTabConfig[];
  activeTabId: string;
  setActiveTabId: (id: string) => void;
  resetActiveTab: () => void;

  /** When set, right panel shows agent SPEC instead of route docs. */
  agentSpecFocus: AgentSpecFocus | null;
  setAgentSpecFocus: (focus: AgentSpecFocus | null) => void;
  /** Open panel and show loading/loaded agent SPEC. */
  openAgentSpecInPanel: (focus: AgentSpecFocus) => void;
  clearAgentSpecFocus: () => void;
};

const WorkspaceHelpContext = createContext<WorkspaceHelpContextValue | null>(null);

function clampWidth(width: number): number {
  const max = helpDrawerMaxForViewport();
  return Math.min(max, Math.max(HELP_DRAWER_MIN_WIDTH, Math.round(width)));
}

function readStoredWidth(): number {
  if (typeof window === "undefined") return HELP_DRAWER_DEFAULT_WIDTH;
  try {
    const raw = window.localStorage.getItem(HELP_DRAWER_WIDTH_STORAGE_KEY);
    if (!raw) return HELP_DRAWER_DEFAULT_WIDTH;
    const n = Number(raw);
    if (!Number.isFinite(n)) return HELP_DRAWER_DEFAULT_WIDTH;
    return clampWidth(n);
  } catch {
    return HELP_DRAWER_DEFAULT_WIDTH;
  }
}

export function WorkspaceHelpProvider({
  children,
  tabs = DEFAULT_HELP_TABS,
}: {
  children: ReactNode;
  tabs?: HelpTabConfig[];
}) {
  const helpTabs = tabs.length ? tabs : DEFAULT_HELP_TABS;
  const defaultTabId = helpTabs[0].id;

  const [drawerOpen, setDrawerOpen] = useState(false);
  const [rightPanelOpen, setRightPanelOpen] = useState(false);
  const [rightPanelWidth, setRightPanelWidthState] = useState(HELP_DRAWER_DEFAULT_WIDTH);
  const [rightPanelDragging, setRightPanelDragging] = useState(false);
  const [activeTabId, setActiveTabId] = useState(defaultTabId);
  const [agentSpecFocus, setAgentSpecFocus] = useState<AgentSpecFocus | null>(null);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setRightPanelWidthState(readStoredWidth());
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    try {
      window.localStorage.setItem(HELP_DRAWER_WIDTH_STORAGE_KEY, String(rightPanelWidth));
    } catch {
      // ignore quota / private mode
    }
  }, [rightPanelWidth, hydrated]);

  // Close mobile left drawer when viewport is desktop-sized; re-clamp width on resize.
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 1024px)");
    const onChange = () => {
      if (mq.matches) setDrawerOpen(false);
    };
    const onResize = () => {
      setRightPanelWidthState((w) => clampWidth(w));
    };
    onChange();
    mq.addEventListener("change", onChange);
    window.addEventListener("resize", onResize);
    return () => {
      mq.removeEventListener("change", onChange);
      window.removeEventListener("resize", onResize);
    };
  }, []);

  const setRightPanelWidth = useCallback((width: number) => {
    setRightPanelWidthState(clampWidth(width));
  }, []);

  const clearAgentSpecFocus = useCallback(() => setAgentSpecFocus(null), []);

  const openAgentSpecInPanel = useCallback((focus: AgentSpecFocus) => {
    setAgentSpecFocus(focus);
    setRightPanelOpen(true);
  }, []);

  const toggleDrawer = useCallback(() => setDrawerOpen((v) => !v), []);
  const toggleRightPanel = useCallback(() => {
    setRightPanelOpen((open) => {
      const next = !open;
      if (next) {
        setActiveTabId(defaultTabId);
        setAgentSpecFocus(null);
      }
      return next;
    });
  }, [defaultTabId]);

  const setRightPanelOpenSafe = useCallback(
    (open: boolean) => {
      setRightPanelOpen(open);
      if (open) {
        setActiveTabId(defaultTabId);
      } else {
        setAgentSpecFocus(null);
      }
    },
    [defaultTabId],
  );

  const setActiveTabIdAndClearAgent = useCallback((id: string) => {
    setActiveTabId(id);
    setAgentSpecFocus(null);
  }, []);

  const resetActiveTab = useCallback(() => {
    setActiveTabId(defaultTabId);
    setAgentSpecFocus(null);
  }, [defaultTabId]);

  const value = useMemo<WorkspaceHelpContextValue>(
    () => ({
      drawerOpen,
      setDrawerOpen,
      toggleDrawer,
      rightPanelOpen,
      setRightPanelOpen: setRightPanelOpenSafe,
      toggleRightPanel,
      rightPanelWidth,
      setRightPanelWidth,
      rightPanelDragging,
      setRightPanelDragging,
      helpTabs,
      activeTabId,
      setActiveTabId: setActiveTabIdAndClearAgent,
      resetActiveTab,
      agentSpecFocus,
      setAgentSpecFocus,
      openAgentSpecInPanel,
      clearAgentSpecFocus,
    }),
    [
      drawerOpen,
      toggleDrawer,
      rightPanelOpen,
      setRightPanelOpenSafe,
      toggleRightPanel,
      rightPanelWidth,
      setRightPanelWidth,
      rightPanelDragging,
      helpTabs,
      activeTabId,
      setActiveTabIdAndClearAgent,
      resetActiveTab,
      agentSpecFocus,
      openAgentSpecInPanel,
      clearAgentSpecFocus,
    ],
  );

  return (
    <WorkspaceHelpContext.Provider value={value}>{children}</WorkspaceHelpContext.Provider>
  );
}

export function useWorkspaceHelp(): WorkspaceHelpContextValue {
  const ctx = useContext(WorkspaceHelpContext);
  if (!ctx) {
    throw new Error("useWorkspaceHelp must be used within WorkspaceHelpProvider");
  }
  return ctx;
}

/** Optional hook that returns null outside provider (for isolated stories/tests). */
export function useWorkspaceHelpOptional(): WorkspaceHelpContextValue | null {
  return useContext(WorkspaceHelpContext);
}
