# react / architecture.html — Architecture for Large Apps

Pager: `← testing.html` · `server-components.html →`

`composition.html` is already rebuilt — complement it rather than repeating it.

Cover:

- Folder structure by **feature rather than file type**, with the concrete pain of `components/`,
  `hooks/`, `utils/` at 300 files, and what a feature folder contains.
- The module-boundary rule — a feature exposes a public `index.ts` and nothing imports its internals —
  and enforcing it with **ESLint import rules rather than a wiki page**.
- The layering that survives: UI primitives, feature modules, shared components, data/API layer — and
  why dependencies must point one way.
- **A shared component only earns its place at three real consumers**, and the premature-design-system trap.
- TypeScript at scale — props types as the contract, discriminated unions for variants, where `any` leaks.
- State architecture at scale, referencing the server-cache / client / URL split.
- Barrel files and the bundle and circular-import problems they cause.
- Monorepos and when they are actually worth it.
- Lint rules and code review as the mechanism that actually holds architecture in place.
- Migrating an existing large app — the strangler pattern, feature by feature, **never a rewrite**.
- Documentation that stays true: colocated READMEs, Storybook for the component library, ADRs.
- Honest guidance on when all of this is over-engineering for a five-person team.
