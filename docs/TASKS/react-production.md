# react / production.html — Production Patterns

Pager: `← nextjs.html` · `quiz.html →`

Cover:

- What a production build changes — minification, dead-code elimination, `NODE_ENV` stripping
  development warnings, source maps and whether to ship them.
- Environment configuration and the fact that **anything in a client bundle is public** — the
  recurring incident of an API secret shipped via a build-time variable.
- Performance budgets and the Core Web Vitals that matter — LCP, **INP (which replaced FID)**, CLS —
  with real thresholds and the React-specific cause of each.
- Real-user monitoring versus lab metrics, and why lab numbers mislead.
- Error tracking: source maps uploaded, release tagging, sampling.
- The accessibility floor a production app must meet — focus management on route change, announcing
  navigation, keyboard traps in modals, and the fact that **a `<div onClick>` is invisible to a
  screen reader**.
- Internationalisation and the bundle cost of naive approaches.
- Security — XSS via `dangerouslySetInnerHTML`, why JWTs in `localStorage` are a bad default, CSP,
  dependency risk.
- Caching and cache-busting via content hashes, plus **the stale-index.html problem** that serves an
  old shell referencing deleted chunks.
- Feature flags and progressive rollout.
- A concrete pre-launch checklist covering build, monitoring, accessibility, security and rollback.
