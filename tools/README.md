# tools/

Repo-committed tooling. Nothing here depends on a session, a scratchpad, or
anything outside this repo — clone it and everything works.

## validate.py (repo root)

Checks lesson HTML: tag nesting, unescaped `<` inside `<pre>` (which silently
swallows content in browsers), asset references, internal links, and v4
structure counts.

```
PYTHONIOENCODING=utf-8 python validate.py tutorials/<track>              # whole track
PYTHONIOENCODING=utf-8 python validate.py tutorials/<track> <file>.html  # one lesson
```

A v4 lesson must report `det=12 ex=6` with 0 errors. While a track is mid-build,
forward links to unwritten lessons appear as "broken link" — that is expected and
clears as each file lands. Re-run the whole-track validate at the end.

## tools/quizcheck.py

Validates a track's quiz bank and **detects answer-position skew**.

```
python tools/quizcheck.py tutorials/<track>
```

Healthy output:

```
10 200 0
duplicate stems: 0
answer distribution: {"0": 66, "1": 71, "2": 63}
OK
```

The first line is `sets questions malformed` — it must read `10 200 0`.
Exits 1 on any problem, so it works in a check script.

**Why the skew check exists:** banks are frequently authored with the correct
answer always at index 1, which makes the quiz answerable without reading the
questions. Both the LeetCode bank (191/200 at index 1) and the Redis bank
(200/200) had this before it was caught.

## tools/quizshuffle.js

Fixes skew by shuffling each question's options and updating `answer` to follow
the correct option.

```
node tools/quizshuffle.js tutorials/<track>
python tools/quizcheck.py tutorials/<track>      # verify
```

**Idempotent.** Each question is shuffled with a PRNG seeded from its own stem
and a canonicalised option order, so the result depends only on the question
text. Running it twice leaves the files byte-identical — no spurious diffs.

It never changes stems, option sets, or which option is correct; only positions
move. Verify that after running:

```bash
mkdir -p .tmpcheck
git show HEAD:tutorials/<track>/quiz-bank-1.js > .tmpcheck/o1.js
git show HEAD:tutorials/<track>/quiz-bank-2.js > .tmpcheck/o2.js
node -e "
const p=require('path');
global.window={};require(p.resolve('.tmpcheck/o1.js'));require(p.resolve('.tmpcheck/o2.js'));
const a=global.window.QUIZ_SETS.flatMap(s=>s.questions);
global.window={};require(p.resolve('tutorials/<track>/quiz-bank-1.js'));require(p.resolve('tutorials/<track>/quiz-bank-2.js'));
const b=global.window.QUIZ_SETS.flatMap(s=>s.questions);
let bad=0;
for(let i=0;i<a.length;i++){
  if(a[i].q!==b[i].q){bad++;continue;}
  if(a[i].options[a[i].answer]!==b[i].options[b[i].answer])bad++;
}
console.log(bad===0?'PASS':bad+' MISMATCHES');
"
rm -rf .tmpcheck
```

Note: use repo-relative paths in `node -e` on Windows — node resolves `/tmp` as
`C:\tmp` and fails.

## Quiz-bank format

Two files per track, five sets each:

```js
window.QUIZ_SETS = window.QUIZ_SETS || [];
window.QUIZ_SETS.push(
{ title: "Quiz 1 · Topic",
  desc: "…",
  questions: [
  { q: "…", options: ["a", "b", "c"], answer: 1,
    explain: "…" },
  // × 20
]},
// × 5 per file
);
```

Set 10 is the mixed mock exam. Every question needs a non-empty `explain`.

## Definition of done, per track

1. Every lesson: `det=12 ex=6`, 0 errors from `validate.py`
2. Whole track: `validate.py tutorials/<track>` reports 0 errors **and 0 warnings**
3. Quiz bank: `quizcheck.py` reports `10 200 0`, no duplicates, `OK` (no skew)
4. `quiz.html` checked for the stale `← CSS Track` link and for mojibake
   (`·`, `→` — double-encoded UTF-8) before committing
5. PROJECT_STATUS.md updated and pushed
