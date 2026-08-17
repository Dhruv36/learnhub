#!/usr/bin/env python3
"""Validate a track's quiz bank: set count, question count, malformed entries,
duplicate stems, and answer-position skew.

    python tools/quizcheck.py tutorials/redis

A healthy bank prints "10 200 0" plus a roughly even answer distribution.
A skewed distribution (e.g. all answers at index 1) makes the quiz guessable
without reading the questions -- fix it with tools/quizshuffle.py.

Exit code 1 if the bank is malformed or the answer distribution is badly skewed.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

NODE_SNIPPET = r"""
global.window = {};
require(process.argv[1]);
require(process.argv[2]);
const sets = global.window.QUIZ_SETS || [];
console.log(JSON.stringify(sets));
"""


def load_bank(track_dir: Path):
    """Load the two quiz-bank files via node and return the parsed sets."""
    b1 = track_dir / "quiz-bank-1.js"
    b2 = track_dir / "quiz-bank-2.js"
    for f in (b1, b2):
        if not f.exists():
            sys.exit(f"missing {f}")
    # encoding is explicit: the banks are UTF-8 and Windows would otherwise
    # decode the node output as cp1252 and fail on the first non-ASCII character
    out = subprocess.run(
        ["node", "-e", NODE_SNIPPET, str(b1.resolve()), str(b2.resolve())],
        capture_output=True, text=True, encoding="utf-8",
    )
    if out.returncode != 0:
        sys.exit(f"failed to load bank:\n{out.stderr}")
    return json.loads(out.stdout)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    track = Path(sys.argv[1])
    sets = load_bank(track)

    total = sum(len(s["questions"]) for s in sets)
    bad = 0
    stems = []
    dist = {}

    for s in sets:
        for q in s["questions"]:
            stems.append(q.get("q", ""))
            ok = (
                q.get("q")
                and q.get("explain")
                and isinstance(q.get("answer"), int)
                and 0 <= q["answer"] < len(q.get("options", []))
            )
            if not ok:
                bad += 1
            dist[q.get("answer")] = dist.get(q.get("answer"), 0) + 1

    dupes = len(stems) - len(set(stems))

    print(f"{len(sets)} {total} {bad}")
    print(f"duplicate stems: {dupes}")
    print(f"answer distribution: {json.dumps(dist, sort_keys=True)}")

    errors = []
    if len(sets) != 10:
        errors.append(f"expected 10 sets, found {len(sets)}")
    if total != 200:
        errors.append(f"expected 200 questions, found {total}")
    if bad:
        errors.append(f"{bad} malformed questions")
    if dupes:
        errors.append(f"{dupes} duplicate stems")

    # skew check: no single answer index should hold more than 60% of answers
    if total:
        worst = max(dist.values())
        if worst / total > 0.6:
            idx = max(dist, key=dist.get)
            errors.append(
                f"answer skew: {worst}/{total} ({100*worst/total:.0f}%) at index {idx}"
                " -- run tools/quizshuffle.py"
            )

    for e in errors:
        print(f"  ! {e}")
    print("OK" if not errors else f"{len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
