# react / external-state.html — External Stores (Redux, Zustand)

Pager: `← state-patterns.html` · `router.html →`

Cover:

- The problem stores solve that context does not — **selective subscription**, so a component
  re-renders only when the slice it reads changes.
- `useSyncExternalStore` as the primitive React provides, and **tearing** as the reason it exists.
- Redux Toolkit as actually written today (`createSlice`, Immer drafts, RTK Query) versus the
  boilerplate reputation from 2016.
- The Redux principles that remain valuable independent of the library — single source of truth,
  pure reducers, serialisable actions, time-travel debugging.
- Zustand's model and why its API is so much smaller.
- A fair comparison across Redux Toolkit, Zustand, Jotai/Recoil (atomic), MobX (proxy) and plain
  context — the axis being subscription granularity and devtools.
- Selectors, and **why returning a new object from a selector causes an infinite re-render loop**
  (with the `useShallow` / equality-fn fix).
- Middleware and persistence.
- The honest verdict: most apps need a server-cache library plus local state, and reach for a client
  store later than they think.
