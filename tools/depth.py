#!/usr/bin/env python3
"""Measure a track's TEACHING depth, not its file size.

    python tools/depth.py javascript css        # per-track medians
    python tools/depth.py css --per-lesson      # every lesson
    python tools/depth.py --selftest

validate.py's 45KB warning says "re-read this lesson". It cannot say whether
the lesson TEACHES well. This does the next best thing: it counts the things
the v4 recipe actually asks for, so a track can be compared against a finished
one (react) on substance rather than bytes.

Read the numbers as a prompt to go and look, never as a target to hit. A lesson
with 6 short takeaways may be finished if its topic is genuinely narrow.
"""
import re
import sys
import glob
import os
import statistics

# docs/LESSON_REBUILD_SPEC.md targets, for reference in the output.
TARGET = {"iq_words": "3-6 paras", "mistakes": "12-16", "takeaways": "14-16",
          "iq_count": "6", "exercises": "6"}


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def section(html, heading):
    """Body of the <h2> whose text contains `heading`, up to the next h2 or the
    takeaways div (which is not itself an h2)."""
    m = re.search(r"<h2>[^<]*" + heading + r"[^<]*</h2>(.*?)"
                  r'(?=<h2>|<div class="takeaways")', html, re.S)
    return m.group(1) if m else ""


def measure(html):
    """None for a stub/redirect page, else the lesson's teaching markers."""
    if len(html) < 2000:
        return None
    iq = section(html, "Interview Questions")
    answers = []
    for d in re.findall(r"<details.*?</details>", iq, re.S):
        # the question lives in <summary>; measure only the ANSWER
        body = re.sub(r"<summary.*?</summary>", "", d, flags=re.S)
        answers.append(len(strip_tags(body).split()))
    mistakes = section(html, "Common Mistakes")
    tk = re.search(r'class="takeaways".*?</ul>', html, re.S)
    return {
        "parts": len(re.findall(r"<h2>Part \d", html)),
        "iq_count": len(answers),
        # median, so one long answer cannot carry a lesson of short ones
        "iq_words": int(statistics.median(answers)) if answers else 0,
        "exercises": len(re.findall(r'class="exercise"', html)),
        # -1 for the header row
        "mistakes": max(0, len(re.findall(r"<tr>", mistakes)) - 1),
        "takeaways": len(re.findall(r"<li>", tk.group(0))) if tk else 0,
        "tables": len(re.findall(r'class="tbl"', html)),
    }


def lessons(track):
    for f in sorted(glob.glob(f"tutorials/{track}/*.html")):
        if os.path.basename(f) == "quiz.html":
            continue
        with open(f, encoding="utf-8", errors="replace") as fh:
            m = measure(fh.read())
        if m:                      # skip redirect stubs
            yield os.path.basename(f), m


COLS = ["parts", "iq_count", "iq_words", "exercises", "mistakes", "takeaways", "tables"]


def report(tracks, per_lesson=False):
    print(f"{'':14s}" + "".join(f"{c:>10s}" for c in COLS))
    print(f"{'TARGET':14s}" + "".join(
        f"{TARGET.get(c, '6'):>10s}" for c in COLS))
    print("-" * (14 + 10 * len(COLS)))
    for track in tracks:
        rows = list(lessons(track))
        if not rows:
            print(f"{track:14s}  no lessons found")
            continue
        if per_lesson:
            print(f"\n=== {track} ===")
            for name, m in rows:
                print(f"{name[:14]:14s}" + "".join(f"{m[c]:>10d}" for c in COLS))
        med = {c: statistics.median([m[c] for _, m in rows]) for c in COLS}
        label = f"{track} (n={len(rows)})"
        print(f"{label[:14]:14s}" + "".join(f"{med[c]:>10.0f}" for c in COLS))


FIXTURE = """<html><body>
<h2>Part 1 — A</h2><h2>Part 2 — B</h2>
<h2>Common Mistakes</h2><table class="tbl">
<tr><th>M</th><th>W</th></tr><tr><td>a</td><td>b</td></tr><tr><td>c</td><td>d</td></tr></table>
<h2>Interview Questions</h2>
<details><summary>ignore these words entirely please</summary><p>one two three four five</p></details>
<details><summary>q2</summary><p>one two three</p></details>
<h2>Exercises</h2><div class="exercise">x</div>
<div class="takeaways"><ul><li>a</li><li>b</li><li>c</li></ul></div>
</body></html>""" + "x" * 2000


def selftest():
    m = measure(FIXTURE)
    assert m["parts"] == 2, m
    assert m["iq_count"] == 2, m
    # answers are 5 and 3 words; the summary text must NOT be counted
    assert m["iq_words"] == 4, m
    assert m["exercises"] == 1, m
    assert m["mistakes"] == 2, m          # 3 <tr> minus the header
    assert m["takeaways"] == 3, m
    assert measure("<html>tiny</html>") is None
    print("selftest OK")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        selftest()
    elif args:
        report(args, per_lesson="--per-lesson" in sys.argv)
    else:
        print(__doc__)
