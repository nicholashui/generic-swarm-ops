---
kind: frontend_style
name: Tailwind v4 + CSS Variables Design System
category: frontend_style
scope:
    - '**'
source_files:
    - frontend/src/app/globals.css
    - frontend/src/design/tokens.ts
    - frontend/src/design/theme.ts
    - frontend/src/design/status.ts
    - frontend/src/components/ui/button.tsx
    - frontend/src/components/ui/card.tsx
    - frontend/src/lib/utils.ts
    - frontend/postcss.config.mjs
---

The frontend styling system is built on Tailwind CSS v4 with a dark-first, CSS-variable-driven design token layer. It combines utility-first composition with a small set of hand-written base styles and semantic component primitives.

**Stack and tooling**
- Tailwind CSS v4 via `@tailwindcss/postcss` (no custom config file — configuration lives in CSS imports and JS tokens)
- PostCSS pipeline (`postcss.config.mjs`) registering only the Tailwind plugin
- `clsx` + a thin `cn()` wrapper in `src/lib/utils.ts` for conditional class merging
- No external UI kit; all visual primitives are implemented as internal React components under `src/components/ui/`

**Design tokens and theme**
- Semantic color tokens live in `src/design/tokens.ts` (`background`, `surface`, `accent`, `accentSecondary`, `success`, `warning`, `danger`, `info`, `muted`)
- Tokens are mirrored into CSS custom properties in `src/app/globals.css` (`--background`, `--foreground`, `--line`, `--accent`, `--accent-2`, `--danger`, `--warning`, `--success`, `--info`, `--muted`) so Tailwind utilities can reference them at runtime
- A minimal `appTheme` object in `src/design/theme.ts` brands the app and declares typography families (`IBM Plex Sans` / `IBM Plex Mono`)
- Status semantics are centralized in `src/design/status.ts`: a `statusStyles` map plus a `mapStatusTone()` helper that normalizes backend status strings to one of `{success, running, pending, danger, cancelled, draft, paused, neutral}` — consumed by badge/stateful UIs

**Base styles and layout primitives**
- `globals.css` sets the dark palette, radial-gradient background, selection color, a subtle `.app-grid` dot grid, and two surface classes (`.surface-card`, `.surface-card-strong`) with glass-like gradients and borders
- Reduced-motion media query disables animations for accessibility
- Global reset: `box-sizing: border-box`, full-height html/body, inherited link colors

**Component-level style conventions**
- Primitive components in `src/components/ui/` (e.g. `Button`, `Card`, `Badge`, `Input`, `Section`, `Skeleton`, `EmptyState`, `ErrorState`, `DataTable`, `LogViewer`, `MetricCard`, `SearchInput`, `StatusLabel`) compose Tailwind utilities through `cn(...)` rather than importing CSS modules
- Variants are expressed as string maps keyed by variant name (see `ButtonVariant` → `variants` record) and merged with `className` props
- All color usage goes through CSS variables (`var(--accent)`, `var(--danger)`, etc.) or Tailwind's `bg-[rgba(...)]` / `text-[var(--...)]` syntax — no hard-coded hex literals inside components
- Typography is applied via Tailwind font utilities referencing the IBM Plex families declared in `theme.ts`

**Responsive and cross-cutting concerns**
- Responsive behavior uses Tailwind's default breakpoints (no custom `tailwind.config.js`); spacing and sizing follow Tailwind's scale
- Accessibility: focus-visible outlines use `--accent`; reduced-motion is respected globally
- The design system is intentionally minimal — there is no separate theme provider, CSS-in-JS library, or CSS framework beyond Tailwind + vanilla CSS variables