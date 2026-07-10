"use client";
import { useEffect } from "react";
import { useCommandPaletteStore } from "@/stores/command-palette-store";
export function useCommandPalette() { const open = useCommandPaletteStore((state) => state.open); const setOpen = useCommandPaletteStore((state) => state.setOpen); const toggle = useCommandPaletteStore((state) => state.toggle); useEffect(() => { const onKeyDown = (event: KeyboardEvent) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); toggle(); } if (event.key === "Escape") setOpen(false); }; window.addEventListener("keydown", onKeyDown); return () => window.removeEventListener("keydown", onKeyDown); }, [setOpen, toggle]); return { open, setOpen, toggle }; }
