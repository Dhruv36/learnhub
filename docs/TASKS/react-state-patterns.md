# react / state-patterns.html — State Architecture Patterns

Pager: `← context.html` · `external-state.html →`

Cover:

- The five-way classification that drives every decision — **server cache, client UI, form, URL,
  derived** — and why treating server data as client state is the root of most React state complexity.
- **Derived state must be computed during render, not stored in an effect.** Show the
  two-sources-of-truth bug concretely.
- Lifting to the lowest common ancestor, and the cost when that ancestor is high up.
- Colocation as the default, and when to break it.
- The URL as state (filters, tabs, pagination) — shareable, back-button-correct, refresh-survivable.
- Controlled vs uncontrolled as a general pattern beyond forms, plus the hybrid
  `defaultValue` + `onChange` API most libraries expose.
- Normalising nested data, and why an array of nested objects makes updates quadratic and error-prone.
- The state-colocation refactor of a slow app.
- When prop drilling is genuinely fine (two or three levels) and when it signals a composition problem.
- A worked decision tree for placing any new piece of state.
