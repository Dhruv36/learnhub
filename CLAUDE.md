# LearnHub

A GeeksforGeeks/W3Schools-style learning site. **Plain HTML/CSS/JS, no build step.**
Deployed to GitHub Pages from `main` — every push goes live at
https://dhruv36.github.io/learnhub/

23 tracks under `tutorials/<track>/`. Each track = ~20–46 lessons + a 10×20 quiz bank.

---

## ▶️ Resume here

**Current work: the v4 depth pass.** Rewriting older lessons to the mature recipe, track by track.

| | |
|---|---|
| **In progress** | **React — 30 of 32 done.** 2 remain: `concurrent`, `production` |
| **Next tracks** | javascript 38 · html 32 · css 28 · nodejs 24 · angular 23 · dotnet 23 · aspnet 17 (by flagged count) |
| **Complete** | java, springboot, python, linux, sql, aws, cicd, docker, kubernetes, mongodb, redis, leetcode, system-design, database-concepts, vector-databases |

**To pick up the next lesson:** read `docs/LESSON_REBUILD_SPEC.md`, then the brief in
`docs/TASKS/<track>-<lesson>.md`, then write the file. Full history is in `PROJECT_STATUS.md`.

---

## Rules that are easy to get wrong

**1. The 45KB flag is a review prompt, never a target.**
`validate.py` warns below `V4_MIN_KB = 45`. That means *re-read this lesson*, not *pad it to 45KB*.
**Never add filler, restated points, or jargon to cross the line.** A 40KB lesson that teaches well is
finished — record it in `REVIEWED_THIN` with a one-line note and move on. Quality is judged on
teaching, not bytes.

**2. Never put HTML tags inside a `<pre>` block.**
This is the single most common `validate.py` error. Inside `<pre>` use plain text and escape
angle brackets: `&lt;div&gt;`, `&amp;&amp;`, `() =&gt; {}`. Use CAPITALS for emphasis. Tags are
fine everywhere outside `<pre>`.

**3. Verify before every commit.**
```bash
python validate.py tutorials/<track>          # 0 errors required
python tools/quizcheck.py tutorials/<track>   # expects "10 200 0"
```

---

## Delegating to subagents — read before spawning

Across three rounds (2026-09-08/09) agents completed **9 lessons and failed 12 times**, always the
same way: write lesson 1 at ~2× the target size, notice, announce "rewriting tighter", die
mid-rewrite. Naming an explicit KB target and a reference file **did not fix it** — their finished
lessons still came in at 61–69KB.

Lessons written directly landed at 42–44KB first time with no rewrite cycle.

**So: prefer writing directly.** If you do delegate, expect roughly one completed lesson per agent
and plan to finish the rest yourself. Their finished files are still good — commit them rather than
re-trimming working content.

**Always tell an agent: do NOT run git, do NOT edit `validate.py`.** Agents have committed
unreviewed work when not told otherwise. The parent session owns all commits.

---

## Layout

```
tutorials/<track>/       lessons + nav.js (the sidebar's single source of truth)
                         quiz.html + quiz-bank-1.js (sets 1–5) + quiz-bank-2.js (sets 6–10)
validate.py              tag nesting, unescaped < in <pre>, asset refs, links, depth flag
tools/                   quizcheck.py, quizshuffle.js — committed, no session deps
docs/LESSON_REBUILD_SPEC.md   the v4 recipe
docs/TASKS/              per-lesson briefs, ready to hand to an agent
PROJECT_STATUS.md        full per-track history
```

A lesson's pager links and its `nav.js` entry must agree. When rebuilding, **read the existing
pager and reproduce it exactly** — do not invent new links.
