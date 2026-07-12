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
| 6 | Python | 12 | 200 | ✅ DONE |
| 7 | Java | 12 | 200 | ✅ DONE |
| 8 | SQL | 12 | 200 | ✅ DONE |
| 9 | MongoDB | 12 | 200 | ✅ DONE |
| 10 | Redis | 11 | 200 | ✅ DONE |
| 11 | Docker | 12 | 200 | ✅ DONE |
| 12 | Kubernetes | 12 | 200 | ✅ DONE |
| 13 | AWS | 12 | 200 | ✅ DONE |
| 14 | CI/CD | 12 | 200 | ✅ DONE |
| 15 | Angular | 12 | 200 | ✅ DONE |
| 16 | .NET (C#) | 12 | 200 | ✅ DONE |
| 17 | ASP.NET Core | 12 | 200 | ✅ DONE |
| 18 | LeetCode Patterns | 21 lessons (Foundations ×3 + Core ×8 + Trees&Graphs ×4 + Advanced ×6) | 200 | ✅ DONE |
| 19 | System Design | 44 lessons (Fundamentals ×11 + Deep Dives ×6 + Case Studies ×12 + Senior/Staff ×7) | 200 | ✅ DONE |

**v3 build-out done: 19 full tracks (3,800 quiz questions), all committed & pushed.**

---

## 🚧 CURRENT PHASE: Mastery v4 rebuild (started 2026-07-12)

**User feedback:** v3 lessons (~9–13KB each) are too shallow — "can't even master a single topic" at beginner, mid, OR senior level. Directive: make learners masters of each topic.

**Decisions (user-confirmed via AskUserQuestion):**
1. **Expand curriculum** — split combined topics into focused lessons at 3–5× depth (not deepen-in-place). E.g., JS "Closures & this" → 4 separate lessons. Tracks grow from ~12–16 to ~30+ lessons.
2. **Work in site order, tracks 1→19**: HTML → CSS → JavaScript → React → Node.js → Python → Java → SQL → MongoDB → Redis → Docker → Kubernetes → AWS → CI/CD → Angular → .NET → ASP.NET Core → LeetCode → System Design. Complete each track fully before moving on.

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
| 1 | HTML | 🚧 IN PROGRESS — curriculum expanded 14→~31 lessons (new nav.js); writing lessons in batches, commit every ~4 |
| 2–19 | all others | ⏳ pending (still at v3 depth) |

Quizzes: existing 200-Q banks stay; extend/retune only after a track's lessons are done, if question topics drifted.

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
