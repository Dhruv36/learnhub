# LearnHub lesson rebuild — v4 spec

*Track-agnostic. Written during the React pass; the React-specific notes are marked as such
at the end. Substitute the track directory and its own freshly-rebuilt reference lessons.*

Repo root: the repository containing this file.
Track: `tutorials/<track>/`

**Reference lessons** (read two before writing anything, and match their per-Part size):
`tutorials/react/data-fetching.html` (43KB), `tutorials/java/synchronization.html` (45KB).

You are rewriting existing lesson pages to the site's "v4 mature" depth. Plain HTML,
no build step. **Read `tutorials/react/forms.html` and `tutorials/react/props.html` first** —
those are the rebuilt reference lessons for this track. Match their voice, structure and
density. If you want a second opinion on depth, `tutorials/java/synchronization.html` is the
house standard.

## Absolute rules

1. **Rewrite the whole file** with the Write tool. Keep the existing `<h1>` topic and the
   existing **pager links** — read the current file's `<div class="pager">` before overwriting
   and reproduce it exactly. Keep the header/sidebar/script boilerplate byte-identical.
2. **Do NOT edit `validate.py`. Do NOT run any git command** — not `add`, not `commit`, not
   `push`. The parent session handles all commits. Touch only the lesson HTML files assigned
   to you.
3. **File size is NOT a target.** There is a 45KB warning in validate.py — it is a review flag,
   never a goal. Never pad with filler, restated points, or jargon to reach it. A 40KB lesson
   that teaches well is finished.
4. **Do not overshoot either.** The reference lessons are ~45KB with 9–12 tables. If a draft
   lands past ~55KB or past 14 tables, you have over-written it — tighten before moving on.
5. After each file run `python validate.py tutorials/react <file>.html` from the repo root and
   fix any ERROR lines. Size warnings are fine — ignore them.

## The single most common validate.py error

Unescaped `<` inside a `<pre>` block. **Inside `<pre>` use no HTML tags at all** — no `<code>`,
no `<strong>`. Write plain text, and escape angle brackets and ampersands: `&lt;div&gt;`,
`&amp;&amp;`, `() =&gt; {}`. This matters more in React than in Java because JSX is full of
angle brackets — `<Button />` inside a `<pre>` MUST be written `&lt;Button /&gt;`. Use CAPITALS
for emphasis inside `<pre>`. HTML tags are fine everywhere outside `<pre>`.

## Required structure (in this order)

```
<h1>Topic <span class="level-badge level-adv">Section</span></h1>

<p><strong>What you'll master:</strong> ... 60–110 words naming the SPECIFIC mechanisms and
   traps the lesson covers, with <strong>bold</strong> on the 3–4 non-obvious ones. End with
   "Prerequisites: <a href="...">X</a>."</p>

<h2>Part 1 — ...</h2>   through   <h2>Part 6 — ...</h2>    (6 parts; 7 only if truly needed)
<h2>Common Mistakes</h2>
<h2>Interview Questions</h2>
<h2>🏋️ Graded Exercises</h2>
<div class="takeaways"><h3>🎯 Key Takeaways</h3><ul>...</ul></div>
<div class="pager">...</div>
```

### Parts 1–6
Each part is a `<h2>` followed by a large `<pre>` block of mechanism-first teaching (annotated
code, ASCII diagrams, measured numbers, failure cases) and/or a `<table class="tbl">`.
Explain **why the technology behaves as it does** — for React: reconciliation, the fiber work loop, effect timing,
closure capture — not just which API to call. Where a number exists (a render count, a bundle
size, a 16ms frame budget) give it and say what makes it vary.

### Common Mistakes
`<table class="tbl">` with header row `Mistake | What actually happens | Do this instead`.
**12–16 data rows.** Each must be a real trap, not a restatement of the API.

### Interview Questions
Exactly **6** `<details class="solution">` blocks:
`<summary><strong>Beginner:</strong> ...</summary>` ×2, then `<strong>Mid:</strong>` ×2, then
`<strong>Senior:</strong>` ×2. Answers are 3–6 paragraphs; senior answers argue trade-offs and
end with a recommendation.

### Graded Exercises
Exactly **6** `<div class="exercise">` blocks, labelled
`<strong>1 (easy):</strong>` `2 (easy)` `3 (medium)` `4 (medium)` `5 (hard)` `6 (hard)`.
Each poses concrete broken or suboptimal code, then a
`<details class="solution"><summary>Solution</summary>` with corrected code, a
`<table class="tbl">` where it clarifies, and **reasoned prose explaining what the wrong
version actually does at runtime**. Not an answer key.

### Key Takeaways
**14–16** `<li>` items, each leading with a `<strong>` claim. Specific and testable, e.g.
"**`useEffect` cleanup runs before every re-run, not only on unmount**", never "understand
effects".

## Target totals per lesson
9–12 `class="tbl"` tables, 12–16 mistake rows, 6 interview questions, 6 exercises,
14–16 takeaways. ~40–48KB naturally results — do not chase the number.

## React-specific accuracy notes
- Target **React 18/19**. Say which version a feature needs when it matters.
- StrictMode double-invokes effects and renders **in development only** — be precise about this
  wherever it comes up; it is the single most misunderstood thing in modern React.
- Do not present class components as current practice; mention them only for contrast.
- Be honest where the ecosystem disagrees (RSC adoption, when a state library is warranted,
  whether `useMemo` is worth it) rather than presenting one side as settled.

## Tone
Direct, technical, senior-engineer voice. Second person. No marketing language, no "let's dive
in", no emoji outside the two headings shown above. Prefer concrete failure stories to
abstractions. Say plainly when common advice is wrong and why.
