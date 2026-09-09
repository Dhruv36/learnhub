# react / testing.html — Testing React

Pager: `← error-boundaries.html` · `architecture.html →`

Cover:

- The guiding principle — **test what the user experiences, not the implementation** — and the
  concrete consequence that asserting on state or internals produces tests that fail on refactors and
  pass on real bugs.
- React Testing Library's query priority (`getByRole` first, then label, then text, `getByTestId` last
  as an escape hatch) and why that order **is an accessibility check in disguise**.
- `getBy` vs `queryBy` vs `findBy` and exactly when each is correct — throwing, returning null, awaiting.
- `userEvent` over `fireEvent`, and why it matters: it fires the full pointer/focus/keydown/input
  sequence a real user generates, catching bugs `fireEvent.change` misses.
- `waitFor` and `findBy` for async, and why an arbitrary `setTimeout` in a test is always wrong.
- Mocking the network at the boundary with MSW rather than mocking `fetch` or your data hooks, and
  why that survives a data-layer change.
- Testing hooks with `renderHook`.
- What NOT to test — implementation details, third-party libraries, generated markup.
- The pyramid for a React app: many component tests, some integration across a route, few E2E.
- Snapshot tests and their failure mode — large snapshots nobody reads, rubber-stamped updates.
- Accessibility assertions with `jest-axe`.
- A worked example converting a brittle implementation-coupled test into a behavioural one.
