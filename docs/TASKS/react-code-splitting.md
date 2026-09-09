# react / code-splitting.html — Code Splitting & Suspense

Pager: `← memoization.html` · `concurrent.html →`

Cover:

- Why bundle size dominates first-load performance — **parse and execute cost on a mid-range phone,
  not just download** — with real numbers for a 1MB bundle on a slow device.
- `React.lazy` and dynamic `import()` mechanics, and why the import must be statically analysable for
  the bundler to emit a chunk.
- `Suspense` as the boundary that catches a pending lazy component, and the placement trade-off —
  too coarse means a blank page, too fine means a spinner mosaic.
- **Route-based splitting as the highest-value split**, plus component-level splitting for heavy
  widgets (an editor, a chart library, a map).
- The loading-state jank problem, and `useTransition` keeping the old UI visible instead of flashing
  a fallback.
- How Suspense works underneath (a thrown promise / the newer `use()` mechanism) and why Suspense for
  data waited on server components.
- Analysing a bundle with source-map-explorer or the Vite/webpack analyzers, and what to look for —
  a date library, an icon set imported whole, a dependency duplicated at two versions.
- Tree-shaking and what defeats it: side effects, CommonJS, barrel files re-exporting everything.
- A checklist of what to split versus what to just delete.
