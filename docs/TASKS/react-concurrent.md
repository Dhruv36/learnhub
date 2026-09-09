# react / concurrent.html — Concurrent Features

Pager: `← code-splitting.html` · `composition.html →`

Cover:

- The problem — before React 18 rendering was a single uninterruptible synchronous pass, so a large
  render blocked the main thread and input queued behind it.
- **Concurrent rendering means React can pause, abandon and restart a render**, which is why render
  functions must be pure and why StrictMode double-invokes them in development.
- `useTransition` / `startTransition` marking an update interruptible — use the typing-into-a-filter-
  over-10k-rows example and say what the user actually perceives. `isPending` for feedback.
- `useDeferredValue` and how it differs: **deferring a VALUE you do not control versus marking an
  UPDATE you trigger.** Include a comparison table.
- Automatic batching in React 18 — updates in promises, timeouts and native handlers now batch too,
  which was a real behaviour change on upgrade — and `flushSync` as the deliberate escape hatch.
- `useId` for SSR-stable ids, and why `Math.random()` breaks hydration.
- Streaming SSR with `renderToPipeableStream` and selective hydration, so a slow data section no
  longer blocks the whole page becoming interactive.
- Tearing — what it is, why concurrent rendering makes it possible, and why external stores must use
  `useSyncExternalStore`.
- Honest guidance: most apps need none of this explicitly, since the wins arrive through the framework.
