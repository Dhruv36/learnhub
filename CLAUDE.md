# LearnHub

A GeeksforGeeks/W3Schools-style learning site. **Plain HTML/CSS/JS, no build step.**
Deployed to GitHub Pages from `main` — every push goes live at
https://dhruv36.github.io/learnhub/

23 tracks under `tutorials/<track>/`. Each track = ~20–46 lessons + a 10×20 quiz bank.

---

## ▶️ Resume here

**Current work: the v4 depth pass.** Bringing older lessons up to the mature recipe, track by
track. For the three tracks left this is *deepening existing lessons*, not rewriting them.

| | |
|---|---|
| **In progress** | **None — the v4 depth pass is complete (2026-09-11).** Every track measures at recipe with `tools/depth.py`. aspnet finished 2026-09-11 (24/24); on the way, a claim repeated in seven aspnet lessons (that `UseAuthorization` before `UseRouting` "fails open") was found false and corrected — see rule 4. dotnet (23/23), angular and nodejs finished the same day. |
| **Measured depth** | `python tools/depth.py react javascript html css` — medians below, react is the finished reference |
| **Next tracks** | **mistakes/takeaways top-up (started 2026-09-11).** A full-site `depth.py` run shows several "complete" tracks below 12–16 mistakes / 14–16 takeaways, IQ depth already fine: database-concepts (10/10), linux (10/13), python and sql (takeaways 10), vector-databases (mistakes 9), docker (mistakes 10), system-design (10/12). Append rows only (rule 1e minus the IQ step). **database-concepts DONE 2026-09-11** (15/15, medians 16/16); rule 4 caught six dated or false claims on the way — pg_upgrade keeps stats from PG18, PgBouncer 1.21+ carries prepared statements, plain `REFRESH MATERIALIZED VIEW` is ACCESS EXCLUSIVE, InnoDB does not escalate locks, the PG14 vacuum failsafe, and checksums can be enabled offline (default on in PG18). **linux DONE 2026-09-11** (20/20, medians 15/16); rule 4 fixed a wrong SigIgn mask, a self-contradicting PID-1 Docker example, a misattributed dmesg line and an inode hunt using `-type d`. Its last 8 lessons (text-processing → shell-scripting) were extended from their existing rows without a full re-read, so they are the least audited. **python and sql DONE 2026-09-11** (medians 14/16 and 15/16); their new takeaways mostly promote topics already in each lesson's mistakes table. **vector-databases DONE 2026-09-11** (median 14/16). **docker DONE 2026-09-11** (21/21, median 14 mistakes; takeaways were already 18–20); rule 4 caught runtime-stack claiming containers survive a dockerd restart by default — the default is `live-restore: false`, the shim only makes live-restore possible (lesson, exercise 2, IQs and quiz-bank-1 Q45 corrected) — and process-model saying `on-failure` restarts after a daemon restart (it does not). **system-design DONE 2026-09-11** (36/36, median 13/14; every lesson 12–13 / 14–15). kubernetes, leetcode, mongodb, redis and springboot were already at target (medians 12–13 / 17–20), and a site-wide per-lesson scan left only java pattern-matching and redis index under 12 mistakes, both topped up. **The top-up is COMPLETE** — every lesson on the site now meets 12+ mistakes / 14+ takeaways. `tools/pending/lib.py` now accepts numbered `<h2>8. Common Mistakes</h2>` headings and whitespace inside the takeaways div. Next: re-run `validate.py` and `depth.py` site-wide to pick the next gap. system-design's "parts 0" is its `<h2>1. …</h2>` numbering, not a gap. |
| **Complete** | aspnet, dotnet, angular, nodejs, css, html, javascript, react, java, springboot, python, linux, sql, aws, cicd, docker, kubernetes, mongodb, redis, leetcode, system-design, database-concepts, vector-databases |

**To pick up the next lesson:** run `python tools/depth.py <track> --per-lesson`, pick the weakest
row, read that lesson in full, then deepen it in place. `docs/LESSON_REBUILD_SPEC.md` is the recipe;
full history is in `PROJECT_STATUS.md`.

```
                   parts  iq_count  iq_words exercises  mistakes takeaways    tables
TARGET                 6         6 3-6 paras         6     12-16     14-16         6
react (n=28)           6         6       194         6        16        16        10
javascript (n=38)      8         6       202         6        16        21         2   DONE
html (n=32)            6         6       212         6        18        22         2   DONE
css (n=28)             5         6       242         6        16        22         1   DONE
nodejs (n=24)          6         6       232         6        17        20         1   DONE
angular (n=23)         6         6       234         6        16        18         1   DONE
dotnet (n=23)          6         6       275         6        16        18         1   DONE
aspnet (n=24)          6         6       271         6        16        16         1   DONE
```
Every section exists in each track above, nodejs included; only the depth per section is short. See rule 1c — **deepen in
place, never rewrite.** `docs/TASKS/` is empty and these tracks do not need briefs: the lesson
already tells you its own topics. Read the lesson, then expand it.

---

## Rules that are easy to get wrong

**1. The 45KB flag is a review prompt, never a target.**
`validate.py` warns below `V4_MIN_KB = 45`. That means *re-read this lesson*, not *pad it to 45KB*.
**Never add filler, restated points, or jargon to cross the line.** A 40KB lesson that teaches well is
finished — record it in `REVIEWED_THIN` with a one-line note and move on. Quality is judged on
teaching, not bytes.

**1b. To judge a track, run `python tools/depth.py <track>` — never eyeball KB.**
It counts what the recipe actually asks for (interview-answer length, mistake rows, takeaways,
exercises, parts) and prints `react` alongside as the finished reference. **A KB-based read of a
track is wrong and has been made before:** in Sept 2026 a session called html/css "half-depth, not
one lesson has been through the v4 recipe" purely from a 24KB median. That was false — every lesson
already had all six sections. Measure, then go read two lessons before concluding anything.

**1c. javascript, html, css, nodejs and angular were ELABORATION jobs** and are done — the method in 1e is
proven across 145 lessons. Measure dotnet and aspnet before assuming the same shape.
All three already have the full v4 shape: 5-8 Parts, Common Mistakes, 6 levelled interview
questions, 6 exercises, takeaways. They were written to a lighter earlier version of the recipe.
What they are missing is depth *per section* — see the table in "Resume here". **Do not rewrite
these files from scratch.** Deepen in place: expand interview answers to 3-6 paragraphs that argue
trade-offs, take mistake rows from ~7 to 12-16, takeaways from ~6 to 14-16. Rewriting loses good
material and costs many times more.

**1e. The elaboration recipe that finished js/html/css (use it for nodejs).**
Per lesson: expand interview answers Q1-Q4 to 3-4 paragraphs each (Q5/Q6 are usually already
long — expanding only two of six does NOT move the median), append mistake rows to ~16, and
append takeaways to ~16-22. Leave Parts and exercises untouched. Work in batches of four
lessons, and gate every commit with **`tools/gate.sh <track> <lesson>...`** (from the repo root):
`validate.py` 0 errors, `quizcheck.py` OK, and the pager links unchanged versus HEAD. Pushes
through OneDrive can exceed 120s — use a long timeout.
The splicer is **`tools/pending/lib.py`**: `apply(path, iq={1: html, ...}, mistakes=rows,
takeaways=lis)` replaces the Nth interview answer by position inside the Interview Questions
section only (some tracks label answers `<strong>Beginner:</strong>` with no Q-number) and appends
mistake rows and takeaways. A batch script is one `apply()` per lesson; any
`tools/pending/batch*.py` is a working template. **Apply a batch once, then delete it** — re-running duplicates its rows.
Also check Parts with `depth.py --per-lesson`: dotnet had five lessons with only 5 Parts, which
needed a new Part 6 inserted before Common Mistakes, not just elaboration.

**1d. SETTLED 2026-09-10: html/css keep their build-and-observe lab exercises.**
Their exercises are labs ("build a flex toolbar, watch the icons shrink, add `flex-shrink: 0`") where
the spec describes debug exercises. **Leave them as labs.** For a visual, hands-on medium the lab
shape teaches better, they already number 6 per lesson with reasoned solutions, and the measured gap
in these tracks is interview-answer depth, mistake rows and takeaways — not exercises. Rewriting
working exercises would be the destruction rule 1c exists to prevent. Do not mix the two shapes
within a track.

**2. Never put HTML tags inside a `<pre>` block.**
This is the single most common `validate.py` error. Inside `<pre>` use plain text and escape
angle brackets: `&lt;div&gt;`, `&amp;&amp;`, `() =&gt; {}`. Use CAPITALS for emphasis. Tags are
fine everywhere outside `<pre>`.

**3. Verify before every commit.**
```bash
python validate.py tutorials/<track>          # 0 errors required
python tools/quizcheck.py tutorials/<track>   # last line must be "OK"
tools/gate.sh <track> <lesson>...             # both of the above + pager check
```

**4. Verify framework-behaviour claims before repeating them.**
In Sept 2026 seven aspnet lessons said `UseAuthorization` before `UseRouting` "fails open silently".
Since ASP.NET Core 3.0 it throws for endpoints with authorization metadata, and a fallback policy
applies to every request — it fails closed. A subagent reading the lessons caught it; the same pass
found a wrong minimal-API binding claim and a wrong exception-filter claim. When a lesson asserts
what a framework does in an edge case, check the docs before echoing it into new answers.

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

**What worked 2026-09-11:** agents wrote *batch scripts* (not lesson files) and were told to
save after every lesson. Both still died on a 429 session limit, but left 12 finished lessons on
disk. Have them write into `tools/pending/` (not a session temp dir) so the work survives the
session too.

---

## Layout

```
tutorials/<track>/       lessons + nav.js (the sidebar's single source of truth)
                         quiz.html + quiz-bank-1.js (sets 1–5) + quiz-bank-2.js (sets 6–10)
validate.py              tag nesting, unescaped < in <pre>, asset refs, links, depth flag
tools/                   quizcheck.py, quizshuffle.js, depth.py, gate.sh — committed, no session deps
tools/pending/           lib.py (the splicer) + drafted batch scripts not yet applied
                         depth.py measures TEACHING markers; use it instead of judging by KB
docs/LESSON_REBUILD_SPEC.md   the v4 recipe
docs/TASKS/              per-lesson briefs, ready to hand to an agent
PROJECT_STATUS.md        full per-track history
```

A lesson's pager links and its `nav.js` entry must agree. When rebuilding, **read the existing
pager and reproduce it exactly** — do not invent new links.
