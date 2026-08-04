# LearnHub — Project Status

**Live:** https://dhruv36.github.io/learnhub/ · **Repo:** github.com/Dhruv36/learnhub (GitHub Pages, main branch → auto-deploy on push)

A GeeksforGeeks/W3Schools-style learning site: plain HTML/CSS/JS, no build step. Goal: deep, curated, mid/senior-interview-ready content the engineering community can use as a single reference. Every track = ~20 lessons (Basics → Ultra-Advanced) + **10 quizzes × 20 questions = 200 Qs** with per-answer explanations.

---

## Track completion

| # | Track | Lessons | Quiz Qs | Status |
|---|-------|---------|---------|--------|
| 1 | HTML | 14 | 200 | ✅ DONE |
| 2 | CSS | 14 | 200 | ✅ DONE |
| 3 | JavaScript | 16 | 200 | ✅ DONE |
| 4 | React | 12 | 200 | ✅ DONE |
| 5 | Node.js | 12 | 200 | ✅ DONE |
| 6 | Python | 12 | 200 | ✅ v3 done · 🔄 v4 1/12 |
| 7 | Java | 12 | 200 | ✅ DONE |
| 8 | SQL | 12 | 200 | ✅ DONE |
| 9 | MongoDB | 12 | 200 | ✅ DONE |
| 10 | Redis | 11 | 200 | ✅ DONE |
| 11 | Docker | 12 | 200 | ✅ DONE |
| 12 | Kubernetes | 12 | 200 | ✅ DONE |
| 13 | AWS | 12 | 200 | ✅ DONE |
| 14 | CI/CD | 12 | 200 | ✅ DONE |
| 15 | Angular | 12 | 200 | ✅ DONE |
| 16 | .NET (C#) | 23 (v4) | 200 | ✅ DONE |
| 17 | ASP.NET Core | 12 | 200 | ✅ DONE |
| 18 | LeetCode Patterns | 21 lessons (Foundations ×3 + Core ×8 + Trees&Graphs ×4 + Advanced ×6) | 200 | ✅ DONE |
| 19 | System Design | 36 lessons (Fundamentals ×11 + Deep Dives ×6 + Case Studies ×12 + Senior/Staff ×7) | 200 | ✅ DONE (v4) |

**v3 build-out done: 19 full tracks (3,800 quiz questions), all committed & pushed.**

---

## 🚧 CURRENT PHASE: Mastery v4 rebuild (started 2026-07-12)

**User feedback:** v3 lessons (~9–13KB each) are too shallow — "can't even master a single topic" at beginner, mid, OR senior level. Directive: make learners masters of each topic.

**Decisions (user-confirmed via AskUserQuestion):**
1. **Expand curriculum** — split combined topics into focused lessons at 3–5× depth (not deepen-in-place). E.g., JS "Closures & this" → 4 separate lessons. Tracks grow from ~12–16 to ~30+ lessons.
2. ~~**Work in site order, tracks 1→19**~~ — **SUPERSEDED 2026-07-30 by the damage-order queue below.** Site order polished 8 tracks while the highest-value ones sat at v3. Still true: complete each track fully before moving on.

### v4 mastery lesson format (supersedes v3 skeleton for lesson depth; same HTML shell/header/sidebar/pager)
Target **~500–700 lines (~35–50KB)** per lesson. Structure:
1. `<h1>` + level badge + intro: what you'll master + prerequisites line (link previous lessons)
2. **Gradual concept build**: plain-language explanation → mental model → syntax → several worked, commented examples (never one example where three teach more)
3. **Step-by-step build section**: construct something real, incrementally, showing output at each step
4. **Deep-dive sections**: edge cases, browser/runtime behavior, spec gotchas, internals (the senior layer)
5. **Common Mistakes** table (grown, 6+ rows)
6. **Interview Questions**: 6+ `<details class="solution">`, explicitly graded — 2 beginner, 2 mid, 2 senior
7. **🏋️ Graded exercises WITH solutions**: 6–10, easy→hard, each with a `<details class="solution">` solution + explanation (this is new vs v3 — v3 had unsolved practice prompts)
8. Key Takeaways + pager

### v4 progress
| # | Track | v4 status |
|---|-------|-----------|
| 1 | HTML | ✅ **DONE** — all 32 mastery-depth lessons shipped (Foundations ×8, Forms Mastery ×6, Semantics & Structure ×3, Media & Embedding ×4, Accessibility ×3, SEO ×2, Performance ×2, Production ×4). Old combined pages (links-images.html, lists-tables.html) kept as redirect stubs to their split successors. Quiz bank NOT yet re-tuned to v4's expanded topic list — old 200 Qs still valid but could use a refresh pass later. |
| 2 | CSS | ✅ **DONE** — all 28 mastery-depth lessons shipped (Foundations ×7, Layout ×6, Motion & Interaction ×3, Modern CSS ×5, Architecture ×3, Production ×4). Old combined pages (colors-units-typography.html, transitions-animations.html, cross-browser-a11y.html) kept as redirect stubs. Link-audited clean (0 broken internal hrefs). Quiz bank not yet re-tuned. |
| 3 | JavaScript | ✅ **DONE (v4+ expanded, 2026-07-18)** — **38 lessons** at mastery depth (Language Core ×9, Objects & Data ×7, Async ×5, Browser & Web Platform ×5, Modules & Tooling ×2, Production ×10). **+5 new: Functional Patterns (Language Core), Dates/Time & Intl (Objects & Data), WebSockets & Real-Time (Browser), Testing JavaScript + Design Patterns in JavaScript (Production)**. Old combined pages kept as legacy stubs. Link-audited clean; quiz banks retuned to the new topics (sets 2/3/4/8/10) — validate 10/200/0. |
| 4 | React | ✅ **DONE** — all 28 mastery-depth lessons shipped (Foundations ×7, Effects & Lifecycle ×5, State Management ×5, Performance ×4, Patterns & Quality ×4, Full-Stack React ×3 incl. Server Components, Next.js, Production Patterns). Old combined pages (props-state, forms-events, context-state) kept as redirect stubs. Heavy cross-linking to JS track + between lessons (later lessons cite earlier by number). Link-audited clean; quiz banks validate 10/200/0 (not yet re-tuned to v4 topics). |
| — | Spring Boot | ✅ **DONE (v4+ expanded, 2026-07-18)** — **23 lessons** at full HTML-track depth (300–360 lines): Core Container ×5, Web Layer ×5, Data Layer ×3, Cross-Cutting ×3, Production ×4, **+ Event-Driven & Reactive ×3 (API Design & Versioning, Messaging & Kafka, Reactive/WebFlux)**. Every lesson: "what you'll master" intro → Parts 1–6 → deep-dive senior `.note` → Common Mistakes → 6 tiered interview Qs → 6 graded exercises → Key Takeaways → pager. Link-audited clean; quiz 10/200/0 (set 10 retuned to cover the new topics). All pushed & live. |
| — | Java | ✅ **DONE (v4+ expanded, 2026-07-18)** — **45 lessons** at full depth. Original 40 across Foundations/OOP/Core Libraries/Modern Java/Concurrency/JVM&Perf/Professional, **+5 new: Annotations & Reflection, Regular Expressions (Core Libraries); The Module System/JPMS (Modern Java); Concurrency Patterns & Pitfalls capstone (Concurrency); Benchmarking & JMH (JVM & Performance)**. Link-audited clean; quiz 10/200/0 (sets 5 & 7 retuned for the new topics; benchmarking already in set 8). All pushed & live. |
| 15 | Angular | ✅ **DONE (v4, 2026-07-19)** — **23 lessons** at mastery depth across 8 sections: Foundations ×4 (index=Components & Standalone, data-binding=Templates, directives=Control Flow, pipes), Components & Reactivity ×4 (component-communication, lifecycle, signals, change-detection), Services & DI ×2 (services-di, di-advanced), RxJS ×2 (rxjs, rxjs-patterns), Forms ×3 (template-forms, forms=Reactive, form-validation incl. CVA), Routing & HTTP ×3 (routing, guards-lazy, http), State ×2 (state-management, ngrx), Production ×3 (testing, performance, enterprise=SSR/i18n/security/monorepo). 12 rewritten in place + 11 new files. Modern Angular throughout: standalone, signals, @if/@for, functional guards/interceptors, zoneless, httpResource. Link-audited clean; quiz retuned (9 swaps: linkedSignal/resource, multi-providers, inject-context, catchError placement, takeUntilDestroyed, lifecycle, CVA, track identity) — 10/200/0. |
| 16 | .NET (C#) | ✅ **DONE (v4, 2026-07-27)** — **23 lessons** at mastery depth across 6 sections: Foundations ×5 (index=How It Runs, types, control-flow, strings, methods), Object-Oriented C# ×5 (oop, inheritance, records-structs, generics, pattern-matching), Core Libraries ×4 (collections-generics, linq, delegates-events, exceptions-nullability), Async & Concurrency ×3 (async-await, **async-patterns** new, **threading** new), Runtime & Performance ×2 (memory, performance-aot), Professional ×4 (di-hosting, efcore, testing, **modern-csharp** new capstone). 12 rewritten in place + 11 new files. Modern throughout: primary constructors, collection expressions, required/init, TimeProvider, Channels, ExecuteUpdate/Delete, source generators, NativeAOT. Link-audited clean (0 broken); pager chain verified against nav order end to end; quiz banks retuned (14 swaps) — 10/200/0. |
| 19 | System Design | ✅ **DONE (v4, 2026-07-30)** — **all 36 lessons rebuilt**, 30–61KB each (1.8 MB total), every one with 12 `<details>` (6 tiered interview Qs + 6 graded exercises), Common Mistakes table and Key Takeaways. **Whole track passes `python validate.py tutorials/system-design` with 0 errors.** §1 Fundamentals 11/11 · §2 Deep Dives 6/6 · §3 Case Studies 12/12 · §4 Senior/Staff 7/7. Uses the **tradeoff-driven SD format**; case studies use the **case-study format** (both below). Quiz bank still the v3 200-Q set — retune to the v4 curriculum when convenient. |
| 5 | Node.js | ✅ **DONE (v4, 2026-07-31)** — **25 lessons** at v4 depth (27KB median), commit `fe2219f`. Was "deep but narrow" at 10 lessons; expanded rather than deepened, as planned. |
| 17 | ASP.NET Core | ✅ **DONE (v4, 2026-08-04)** — **all 23 lessons** at v4 depth, 30–52KB each, every one `det=12 ex=6`. **Whole track passes `python validate.py tutorials/aspnet` with 0 errors.** §1 Foundations 5/5 (index, minimal-apis, routing, model-binding, configuration) · §2 The Pipeline 4/4 (middleware, di-config, filters, validation-errors) · §3 Building APIs 4/4 (controllers-mvc, api-design, versioning, openapi) · §4 Data 3/3 (efcore-data, efcore-advanced, caching) · §5 Security &amp; Realtime 4/4 (authn-authz, authorization, security, signalr) · §6 Production 4/4 (caching-background=Background Services, testing, clean-architecture, production-readiness). **Re-scoped v3 files:** `di-config` is DI-only (config split out), `validation-errors` is error-handling-only (validation moved to model-binding), `caching-background` is Background Services only (caching split out), `efcore-data` is modelling/querying only (change tracking split out). `routing-binding.html` became a redirect stub → routing + model-binding. Quiz bank still the v3 200-Q set — retune when convenient. |
| 6 | Python | ✅ **DONE (v4, 2026-08-04)** — **all 12 lessons** at v4 depth, 35–58KB each, every one `det=12 ex=6`. **Whole track passes `python validate.py tutorials/python` with 0 errors.** Order: index (Syntax/Types/Variables) → control-flow → data-structures → strings-io → oop → comprehensions-generators → decorators-context → modules-packaging → typing → concurrency → testing → fastapi. Uses the **language-track v4 format** (6 Parts → Common Mistakes → 6 tiered Qs → 6 graded exercises → Takeaways), *not* the SD tradeoff format. Rebuilt in place — the v3 content was thin but correct, so this was expansion rather than reconstruction, and no redirect stubs were needed. Quiz bank still the v3 200-Q set — retune when convenient. |
| 5, 7–18 | all others | ⏳ pending (still at v3 depth) — see damage-order queue below |

#### Python v4 — per-lesson status (all ✅, 0 validation errors)
| # | Lesson | v3 | v4 | Focus |
|---|--------|----|----|--------|
| 1 | index.html (Syntax, Types & Variables) | 8KB | **35KB** | name/object model · core types · strong+dynamic typing · idioms · deep dives: mutable default argument, copying |
| 2 | control-flow.html (Control Flow & Functions) | 8KB | **38KB** | truthiness · loops · 5 parameter kinds · LEGB/closures/late-binding · pattern matching · exceptions as control flow |
| 3 | data-structures.html | 8KB | **42KB** | complexity per operation · dicts/sets/hashability · tuples & immutability · collections · sorting · choosing by access pattern |
| 4 | strings-io.html | 7KB | **42KB** | immutability & O(n²) concat · format mini-language · str vs bytes & encoding · `with`/modes/streaming · pathlib · atomic writes |
| 5 | oop.html (OOP & Dataclasses) | 9KB | **48KB** | attribute lookup & shared class attrs · dunder protocols · dataclass slots/frozen · MRO & super() · properties/descriptors · composition |
| 6 | comprehensions-generators.html | 8KB | **47KB** | comprehension forms · iterator protocol & exhaustion · generators as frames · lazy pipelines · itertools · send/throw/close |
| 7 | decorators-context.html | 9KB | **50KB** | wraps & the 5 omissions · 3-layer factories · lru_cache method leak · `__exit__` returning True · @contextmanager · ExitStack |
| 8 | modules-packaging.html | 8KB | **47KB** | import once & side effects · sys.path shadowing · circular imports (4 fixes) · venv + lockfile chain · src layout · build/publish |
| 9 | typing.html (Type Hints) | 8KB | **49KB** | erasure · narrowing & assert_never · Protocol · generics & invariance · Literal/TypedDict/NewType · mypy vs Pydantic · rollout plan |
| 10 | concurrency.html (GIL, Threads, Async) | 9KB | **53KB** | what the GIL locks · decision table w/ numbers · asyncio & blocking calls · `+=` is not atomic · pickling boundary · cancellation/timeouts |
| 11 | testing.html (pytest) | 8KB | **55KB** | assertion introspection · parametrise boundaries · fixtures & scope · transaction-rollback DB · patch-where-used & autospec · flakiness |
| 12 | fastapi.html (Production APIs) | 9KB | **58KB** | types as contract · request/response model split · DI & overrides · async def vs def · BOLA/authz · errors/config/observability · deploy |

### ⚠️ Order changed 2026-07-30 (user: "junior, mid and senior can't refer to this — content not up to the mark")

Strict site order 1→19 polished 8 tracks while the highest-value ones stayed at v3. Audit of actual page sizes showed the site is really **two sites**: 8 v4 tracks at 22–32KB/lesson with 12 `<details>` blocks, and 12 v3 tracks at 5–13KB with 3. Worst offender was System Design — 34 lessons at 5KB median with **zero** exercises, zero graded interview Qs, zero Common Mistakes, despite being the most senior-referenced track on the site.

**New queue, by damage (user-confirmed):**
1. ~~**System Design** (36)~~ ✅ **COMPLETE 2026-07-30** — 36/36 at 30–61KB, 0 validation errors
2. ~~**Node.js**~~ ✅ **COMPLETE 2026-07-31** — 10 → 25 lessons @ 27KB median
3. ~~**ASP.NET Core**~~ ✅ **COMPLETE 2026-08-04** — 23/23 lessons, 0 validation errors
4. ~~**Python**~~ ✅ **COMPLETE 2026-08-04** — 12/12 lessons, 0 validation errors
5. 🔄 **SQL** (12 @ 7–9KB) ← **CURRENT** — highest junior/mid traffic
6. 🆕 **Database Concepts & Architecture** — NEW track (see below)
7. 🆕 **Vector Databases & RAG** — NEW track (see below)
8. **LeetCode** (22 @ 12KB) — note: `index.html` has **0** `<details>`, needs graded sets + batch-2 patterns
9. **Infra six** — Docker, Kubernetes, AWS, CI/CD, MongoDB, Redis (9–12KB, all 3 `<details>`)

**Remaining: ~130 lessons across 5 tracks** (SQL 9 + DB Concepts ~14 + Vector/RAG ~14 + LeetCode 21 + infra six ~70 under the approved expansion, ~40 if deepened in place).

### 🆕 Two new Database-section tracks (user-requested 2026-08-04)

Both are **new tracks built directly at v4 depth** (no v3 to rebuild), added to the `Databases` section of the root `index.html` alongside SQL / MongoDB / Redis. Sequenced **after SQL, before LeetCode** (user-confirmed).

**A. Database Concepts & Architecture** (`tutorials/database-concepts/`)
Scope confirmed by user: **"based on design perspective and storage engine internals"** — i.e. data-modelling/physical-design decisions *plus* how the engine actually works underneath. Deliberately **excludes** distribution topics (CAP, replication, consensus, sharding) — those already exist in System Design and must not be duplicated. Draft curriculum:
1. *Storage Foundations* — Pages/Heap Files & Row Layout · B+Trees · LSM-Trees & Write-Optimised Storage · Buffer Pool & Page Cache
2. *Durability & Concurrency* — WAL, Checkpoints & Crash Recovery · MVCC & Snapshot Isolation · Locking, Latches & Deadlocks
3. *Query Processing* — Parser/Rewriter/Planner · Cost Models & Statistics · Join & Aggregation Algorithms
4. *Design Perspective* — Physical Schema Design for the Engine · OLTP vs OLAP & Row vs Columnar · Engine Landscape (Postgres/MySQL/SQLite/DuckDB) · Choosing a Database

**B. Vector Databases & RAG** (`tutorials/vector-databases/`)
Scope confirmed: **vector stores + RAG patterns** (the full practical track, incl. evaluation and production ops). Draft curriculum:
1. *Foundations* — Embeddings & Vector Space · Similarity Metrics & Normalisation · The Curse of Dimensionality
2. *Indexing & Search* — Exact kNN vs ANN · HNSW Deep Dive · IVF, PQ & Quantisation · Tuning Recall vs Latency
3. *The Landscape* — pgvector & SQL-Native · Dedicated Stores (Pinecone/Qdrant/Weaviate/Milvus) · Metadata Filtering & Hybrid Search (BM25 + vector)
4. *RAG in Production* — Chunking & Ingestion · Retrieval Pipeline & Reranking · Evaluating Retrieval · Scaling, Cost & Ops

Both need: `nav.js`, `quiz.html` + `quiz-bank-1.js`/`quiz-bank-2.js` (10 sets × 20 Qs), a card in root `index.html` → `#databases`, and every lesson at `det=12 ex=6`.

### ⚠ Open decision: infra six scope
User approved full curriculum expansion (12 → ~20 lessons each, ~70 lessons total) on 2026-08-03. After writing 16 ASP.NET lessons at this depth, the build recommendation is to **deepen in place at 12 lessons each (~40 lessons)** instead: Docker, Redis and CI/CD do not have 20 lessons of genuinely distinct material the way Java or System Design did, and padding would show. Raised with the user; not yet re-decided. Default to the approved expansion unless told otherwise.

### Session note 2026-08-03
16 ASP.NET lessons written in one session. Sustained rate is ~1 lesson per 15–20 min at 32–47KB each, so the remaining ~112 lessons span multiple sessions. Every lesson is committed at each checkpoint — resume from this file plus `git log --oneline`. The v4 lesson format is stable and proven across 5 sections; no format changes pending. Quiz banks across *every* v4 track (HTML, CSS, JS, React, Angular, .NET, System Design) are still the v3 200-Q sets — not broken, but drifted from the expanded curricula. Retune pass deferred until lessons are done.

### Tradeoff-driven SD lesson format (System Design only — supersedes the language-track recipe for this track)
Language tracks hit depth via tiered interview Qs + graded coding exercises. System Design needs a different shape — same shell/sidebar/pager and same 12-`<details>` volume, but:
1. "What you'll master" intro + prerequisites line
2. **Mental model** before mechanics — and where a popular framing is *wrong*, say so explicitly (CAP's pick-2-of-3, "balanced keys = balanced load")
3. **Worked arithmetic, not asserted claims** — show the modulo remap table, show the QPS→servers chain, and state a **design consequence after every number**
4. `mistake-pair` divs for ❌ unbacked vs ✅ derived reasoning
5. **Deep dives on the mechanism** (how reconciliation actually works, how data moves at join time), plus **alternatives with when-NOT-to-use** — the strongest senior signal
6. Common Mistakes table, 7–8 rows
7. 6 tiered interview Qs (2 🟢 beginner / 2 🟡 mid / 2 🔴 senior) — senior answers are multi-paragraph and name the trade-off being accepted
8. 6 graded exercises easy→hard; solutions show the *reasoning chain*, and the hard ones often end by **renegotiating the requirement** (approximate rank beats exact rank; cap retention; question the spec)
9. Key Takeaways (8–10 bullets) + pager

### Case-study format (§3 Design X lessons — supersedes the above for those 12)
Same shell and same volume (12 `<details>` = 6 tiered Qs + 6 graded exercises, 24KB+), but structured as an interview walkthrough rather than concept teaching:
1. "What you'll master" + prerequisites, and **what this problem is really testing** (every case study has a signature skill — TinyURL = encoding + read-heavy caching; rate limiter = algorithm choice + distributed counting; chat = fan-out + delivery guarantees)
2. **Requirements clarification** — functional, non-functional, and explicitly *out* of scope. Model the questions a candidate should ask.
3. **Estimation** with a design consequence after each number (reuse the estimation-lesson method)
4. **High-level design** — the diagram and the request flow
5. **The core design decision** — a tradeoff table of 2–4 real options, then a justified pick. This is the section that carries the lesson.
6. **Deep dive on the hard part** (weight this heavily — it's what separates senior candidates)
7. **Bottlenecks & scaling** — what breaks first at 10×, and the fix
8. Common Mistakes → 6 tiered interview Qs → 6 graded exercises → Key Takeaways → pager

### ✅ validate.py — required check on every lesson, every track

**Run from repo root: `python validate.py tutorials/<track> [file.html ...]`**
- Arg 1 is the **directory**; extra args are filenames **relative to it** (`validate.py tutorials/python index.html`). Omit filenames to check the whole track.
- Checks: HTML tag nesting, **unescaped `<` inside `<pre>`**, required asset refs, v4 structure counts (`det=12 ex=6`), and resolves every internal link.
- Expect `[ ok ] name  NNkB  det=12 ex=6 tbl=N` and `0 errors`. Exits 1 on any error.
- On Windows, prefix with `PYTHONIOENCODING=utf-8` or the emoji/em-dashes crash the console writer (cp1252) — a *reporting* failure, not a file problem.

**This is not optional ceremony — it caught 6 real bugs in System Design** that source review missed, including an unescaped `<` that silently swallowed a document from line 200 to `</main>`, and an `<a>` tag nested inside a `<pre>`. Browsers fail these silently.

> **Fixed 2026-07-30:** explicit filenames weren't joined to the root dir, so `validate.py tutorials/python index.html` silently checked `./index.html` (the site homepage) and reported bogus missing-asset errors. A checker that inspects the wrong file while reporting confidently is worse than none — re-verify this behaviour if the script is ever refactored.

Quizzes: existing 200-Q banks stay; extend/retune only after a track's lessons are done, if question topics drifted.

**Build notes for resuming/replicating on remaining tracks:**
- Curriculum expansion pattern: split each v3 combined-topic lesson into 2-4 focused lessons at 3-5x depth (HTML: 14→32; CSS: 14→28). Group into thematic sections (e.g. CSS: Foundations/Layout/Motion/Modern/Architecture/Production) reflected in nav.js.
- Later lessons in a track deliberately cross-reference earlier ones by name — a capstone/consolidation lesson near the end of each major section that assembles several prior lessons' techniques into one real component (HTML's Production Patterns, CSS's Component Patterns) is a deliberate, recurring pedagogical device worth replicating.
- Old superseded combined-topic HTML files become tiny redirect stubs (meta http-equiv=refresh + links to the split successors) rather than being deleted, in case anything external links to the old URL.
- Commit in checkpoints of 1-4 lessons each, pushing after every checkpoint. Run a link-audit one-liner (grep every internal href, confirm the target file exists) before declaring a track done.

---

## How to build a new track (the repeatable recipe)

Directory: `tutorials/<track>/`

1. **`nav.js`** — `renderSidebar([{title, items:[[label, "file.html"], ...]}, ...])`; last group = `Practice` with `["📝 Quizzes (10 sets × 20 Qs)","quiz.html"]`.
2. **~12 lesson `.html` files** in the v3 format (below). Push every ~4 lessons.
3. **`quiz-bank-1.js`** (sets 1–5) + **`quiz-bank-2.js`** (sets 6–10). Each set: `{title:"Quiz N · Topic", desc, questions:[{q, options:[3 strings], answer:<idx>, explain}×20]}`. Wrapped in `window.QUIZ_SETS=window.QUIZ_SETS||[]; window.QUIZ_SETS.push(...)`. Set 10 = mixed mock exam.
4. **`quiz.html`** — copy from `tutorials/css/quiz.html`, then replace `CSS Quizzes`→`X Quizzes`, `← CSS Track`→`← X Track`, `All CSS quizzes`→`All X quizzes`.
5. **Validate** the bank: `node -e "global.window={};require('./tutorials/<track>/quiz-bank-1.js');require('./tutorials/<track>/quiz-bank-2.js');const s=global.window.QUIZ_SETS;let t=0,b=0;s.forEach(x=>{t+=x.questions.length;b+=x.questions.filter(q=>!(q.answer>=0&&q.answer<q.options.length&&q.explain&&q.q)).length});console.log(s.length,t,b)"` → must print `10 200 0`.
6. Add the track's card link on the homepage `index.html` if not already present, and `git add -A && git commit && git push`.

### v3 lesson HTML skeleton
```
<header> logo + nav(← Track / Quizzes)  →  <div class="tutorial-layout"><aside class="sidebar" id="sidebar">
<main class="content">
  <h1>Title <span class="level-badge level-basic|level-adv|level-ultra">Basics</span></h1>
  <p>intro</p>
  <h2>…</h2>  <pre>code</pre>  <table class="tbl">…</table>  <div class="note">key insight</div>
  <h2>Common Mistakes</h2> <table class="tbl">…</table>
  <h2>Interview Questions</h2> 3× <details class="solution"><summary>Q</summary><p>A</p></details>
  <div class="exercise"><strong>🏋️ Practice:</strong> …</div>
  <div class="takeaways"><h3>🎯 Key Takeaways</h3><ul>…</ul></div>
  <div class="pager"> ← prev / next → </div>
</main>
<script src="../../js/sidebar.js"></script><script src="nav.js"></script>
```
**Content bar:** model-first (explain WHY, not just API), name the traps, cross-link to related lessons/tracks, cover the non-negotiable mid/senior concepts.

---

## Ops notes
- Shared assets: `css/style.css`, `js/sidebar.js` (renderSidebar), `js/quiz.js` (v2 engine: explanations after submit + retake), `playground/` (sandboxed iframe editor — used by frontend tracks).
- GitHub Pages occasionally fails deploy with a transient "try again later". Fix: `gh api repos/Dhruv36/learnhub/pages/builds -X POST`.
- Windows line-ending warnings on commit (LF→CRLF) are harmless.
