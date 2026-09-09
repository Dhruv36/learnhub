# react / router.html — Routing & URL State

Pager: `← external-state.html` · `performance.html →`

Cover:

- Client-side routing mechanics (History API, intercepted link clicks, no full page load) and **what
  you must re-implement that the browser gave you for free** — scroll restoration, focus management,
  the back button, announcing navigation to screen readers.
- React Router v6/v7 route configuration, nested routes and `Outlet`, layout routes.
- **The URL as the most under-used state container** — filters, sort, pagination and open panels
  belong there because they are shareable, refresh-survivable and back-button-correct.
- `useSearchParams` and the trap that **it is a snapshot**, so successive updates in one handler lose
  each other unless you use the functional form.
- Loaders and actions as the data-router model, and how they eliminate the fetch-in-effect waterfall
  by starting requests at navigation time.
- `defer` / streaming and per-route Suspense boundaries.
- Protected routes done correctly — redirect state so the user returns where they were, and why an
  effect-based redirect flashes content.
- Route-based code splitting as the highest-value split.
- A comparison of React Router, TanStack Router (type-safe params) and Next.js file-based routing.
