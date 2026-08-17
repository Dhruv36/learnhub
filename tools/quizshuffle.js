#!/usr/bin/env node
/**
 * De-skew a track's quiz bank by shuffling each question's options.
 *
 *     node tools/quizshuffle.js tutorials/redis
 *
 * Banks are frequently authored with the correct answer always at index 1,
 * which makes the quiz guessable without reading the questions. This rewrites
 * quiz-bank-1.js and quiz-bank-2.js in place with the options shuffled and the
 * `answer` index updated to follow the correct option.
 *
 * The shuffle uses a fixed seed, so re-running produces the same result and the
 * diff is stable. Verify afterwards with:  python tools/quizcheck.py <track>
 */
const fs = require("fs");
const path = require("path");

const dir = process.argv[2];
if (!dir) {
  console.error("usage: node tools/quizshuffle.js <track-dir>");
  process.exit(1);
}

const b1 = path.resolve(dir, "quiz-bank-1.js");
const b2 = path.resolve(dir, "quiz-bank-2.js");
for (const f of [b1, b2]) {
  if (!fs.existsSync(f)) {
    console.error(`missing ${f}`);
    process.exit(1);
  }
}

global.window = {};
require(b1);
require(b2);
const SETS = global.window.QUIZ_SETS;

if (!SETS || SETS.length !== 10) {
  console.error(`expected 10 sets, found ${SETS ? SETS.length : 0}`);
  process.exit(1);
}

// Each question is shuffled using a PRNG seeded from its own stem, so the
// output depends only on the question text -- NOT on the current option order.
// That makes the script idempotent: running it twice leaves the file unchanged,
// so re-runs never produce spurious diffs.
const seedFrom = (str) => {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return Math.abs(h) || 1;
};

let moved = 0;
for (const set of SETS) {
  for (const q of set.questions) {
    let seed = seedFrom(q.q);
    const rnd = () => {
      seed = (seed * 1103515245 + 12345) & 0x7fffffff;
      return seed / 0x7fffffff;
    };
    const correct = q.options[q.answer];
    // sort to a canonical order first, so the result is independent of input order
    const opts = [...q.options].sort();
    for (let i = opts.length - 1; i > 0; i--) {
      const j = Math.floor(rnd() * (i + 1));
      [opts[i], opts[j]] = [opts[j], opts[i]];
    }
    const idx = opts.indexOf(correct);
    if (idx !== q.answer) moved++;
    q.options = opts;
    q.answer = idx;
  }
}

const esc = (s) => JSON.stringify(s);

const emitSet = (s) =>
  "{ title: " + esc(s.title) + ",\n  desc: " + esc(s.desc) + ",\n  questions: [\n" +
  s.questions
    .map(
      (q) =>
        "  { q: " + esc(q.q) + ", options: [" + q.options.map(esc).join(", ") +
        "], answer: " + q.answer + ",\n    explain: " + esc(q.explain) + " },"
    )
    .join("\n") +
  "\n]},";

const emitFile = (sets, header) =>
  header + "\nwindow.QUIZ_SETS = window.QUIZ_SETS || [];\nwindow.QUIZ_SETS.push(\n" +
  sets.map(emitSet).join("\n") + "\n);\n";

const name = path.basename(path.resolve(dir));
fs.writeFileSync(b1, emitFile(SETS.slice(0, 5),
  `// ${name} quiz bank — sets 1–5 (20 questions each, with explanations)`));
fs.writeFileSync(b2, emitFile(SETS.slice(5, 10),
  `// ${name} quiz bank — sets 6–10 (20 questions each, with explanations)`));

const dist = {};
SETS.forEach((s) => s.questions.forEach((q) => (dist[q.answer] = (dist[q.answer] || 0) + 1)));
console.log(`answers moved: ${moved}`);
console.log(`new distribution: ${JSON.stringify(dist)}`);
console.log(`verify: python tools/quizcheck.py ${dir}`);
