"""Validate LearnHub lesson HTML: structure, tag balance, escaping, links.

Usage:  python validate.py <dir> [file ...]
Exits non-zero if any ERROR is found.
"""
import sys, os, re, html
from html.parser import HTMLParser

# Size below which a lesson is FLAGGED FOR REVIEW -- not a target to pad to.
#
# Tracks built to the mature recipe land at 50-65KB because of what they
# contain: the mechanism rather than the API, measured failure modes, trade-off
# tables, and tiered interview answers. A lesson well under that was usually
# written to the earlier, thinner recipe and is worth re-reading.
#
# It is NOT a quota. The question for a flagged lesson is "does this teach the
# mechanism, the failure modes, and what a senior answer sounds like?" Some
# genuinely narrow topics answer yes at 35KB and should be left alone -- record
# those in REVIEWED_THIN below so they stop being flagged.
V4_MIN_KB = 45

# Lessons judged complete despite being under V4_MIN_KB, as "track/file.html".
# Add an entry only after reading the lesson and concluding the topic has no
# further interview-relevant depth to give -- never to silence the warning.
REVIEWED_THIN = {
    # "css/specificity.html",   # example: focused topic, fully covered at 33KB

    # Reviewed 2026-08-31. Each read in full: mechanism-first, failure modes
    # named, senior framing present, det=12 ex=6. Conceptual/foundational
    # topics that have no further interview-relevant depth to give.
    "linux/index.html",              # 44KB, kernel/userspace + the 3-part process
    "python/index.html",             # 35KB, name/object model, mutable default, copying
    "python/control-flow.html",      # 38KB, LEGB, late binding, match, exceptions
    "python/data-structures.html",   # 42KB, per-operation complexity, hashability
    "python/strings-io.html",        # 42KB, str/bytes boundary, encodings, pathlib

    # system-design, reviewed 2026-08-31. All at the mature SD/case-study
    # format with 7-9 sections, deep dives and quantified takeaways; 10 of 11
    # sit within 4KB of the floor. Three are technique lessons where extra
    # length would be padding rather than depth.
    "system-design/index.html",                  # 44KB, the 7 scaling stages
    "system-design/estimation.html",             # 30KB, narrow topic, fully worked
    "system-design/interview-framework.html",    # 42KB, technique, not a subject
    "system-design/tradeoff-driven-design.html", # 44KB, technique, not a subject
    "system-design/cap-theorem.html",            # 41KB, PACELC, tunable consistency
    "system-design/consistent-hashing.html",     # 42KB, vnodes, keys-not-load
    "system-design/distributed-consensus.html",  # 42KB, Raft, why reads are harder
    "system-design/cost-capacity-slo.html",      # 41KB, W=1/(1-p), unit economics
    "system-design/migration-strategies.html",   # 44KB, shadow reads, dual-write
    "system-design/design-instagram-feed.html",  # 41KB, case study, fan-out hybrid
    "system-design/design-search-engine.html",   # 44KB, case study, doc-partitioning

    # react, reviewed 2026-09-01 during the rebuild. Rebuilt to the mature
    # standard and judged complete below the baseline - the topic is narrower
    # than its neighbours, and everything it owes is present: the fiber-identity
    # mechanism, the index-key corruption proof, reconciliation rules including
    # the wrapper-type trap, measured costs, and 7 reasoned exercises.
    "react/rendering.html",          # 40KB, lists, keys & conditional rendering
    "react/events.html",             # 44KB, synthetic events & the two dispatch systems
    "react/render-cycle.html",       # 40KB, the five phases, purity, commit timing

    # java, reviewed 2026-09-03 during the rebuild.
    "java/types.html",               # 44KB, primitives vs references, promotion, pass-by-value
    "java/operators.html",           # 43KB, integer division, short-circuit, bitwise, precedence
    "java/control-flow.html",        # 43KB, branching, the four loops, termination reasoning
    "java/methods.html",             # 43KB, signatures, overload resolution, recursion limits
    "java/strings.html",             # 41KB, immutability, the pool, encoding and locale
    "java/arrays.html",              # 42KB, contiguity, shallow copy, covariance
    "java/oop.html",                 # 42KB, invariants, constructors, access, static
    "java/inheritance.html",         # 44KB, dispatch, fragile base class, composition
    "java/interfaces.html",          # 41KB, contracts, defaults, diamond, lambdas
    "java/equality.html",            # 42KB, the contract, vanishing objects, ordering
    "java/enums-nested.html",        # 43KB, enums as classes, ordinal, this$0 leak
}

VOID = {"area","base","br","col","embed","hr","img","input","link","meta",
        "param","source","track","wbr"}
# Tags we require to nest correctly. <p> is omitted: HTML allows implicit
# closing, and the lessons rely on that in places.
CHECK = {"div","details","summary","pre","table","tr","td","th","ul","ol",
         "li","main","aside","header","nav","body","html","h1","h2","h3",
         "strong","em","code","a"}

class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.errors = []
        self.counts = {}
        self.opened = set()

    def handle_starttag(self, tag, attrs):
        self.counts[tag] = self.counts.get(tag, 0) + 1
        self.opened.add(tag)
        if tag in VOID or tag not in CHECK:
            return
        self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag not in CHECK:
            # A closing tag for something we never open is almost always a
            # typo (</note> for </div>); browsers drop it silently.
            if tag not in self.opened:
                self.errors.append(
                    f"line {self.getpos()[0]}: unknown closing tag </{tag}>")
            return
        if not self.stack:
            self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")
            return
        if self.stack[-1][0] != tag:
            open_tag, open_line = self.stack[-1]
            self.errors.append(
                f"line {self.getpos()[0]}: </{tag}> closes <{open_tag}> "
                f"opened at line {open_line}")
            # Try to recover: pop until we find a match.
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            return
        self.stack.pop()


def check_file(path):
    errors, warnings = [], []
    src = open(path, encoding="utf-8").read()
    name = os.path.basename(path)

    c = Checker()
    try:
        c.feed(src)
    except Exception as e:                      # pragma: no cover
        errors.append(f"parse failure: {e}")
    errors.extend(c.errors)
    for tag, line in c.stack:
        errors.append(f"unclosed <{tag}> opened at line {line}")

    # Raw < or > inside <pre> that isn't a real tag would have been eaten by
    # the parser above; instead verify pre blocks decode to something sane.
    for m in re.finditer(r"<pre>(.*?)</pre>", src, re.S):
        body = m.group(1)
        line = src[:m.start()].count("\n") + 1
        # A bare "<" followed by a letter inside <pre> is almost certainly an
        # unescaped tag-like sequence that the browser will swallow.
        for bad in re.finditer(r"<(?=[a-zA-Z/])", body):
            frag = body[bad.start():bad.start() + 40].replace("\n", " ")
            errors.append(f"line ~{line}: unescaped '<' in <pre>: {frag!r}")

    # Redirect stubs (old combined lessons kept so external links survive) are
    # not lessons: they carry no sidebar/nav and are meant to be tiny.
    is_stub = 'http-equiv="refresh"' in src

    # Structural expectations for a v4 lesson.
    stats = {
        "kb":        len(src) // 1024,
        "solution":  src.count('class="solution"'),
        "exercise":  src.count('class="exercise"'),
        "tbl":       src.count('class="tbl"'),
        "takeaways": src.count('class="takeaways"'),
        "pager":     src.count('class="pager"'),
    }
    if name != "quiz.html" and not is_stub:
        track_file = f"{os.path.basename(os.path.dirname(os.path.abspath(path)))}/{name}"
        if stats["kb"] < V4_MIN_KB and track_file not in REVIEWED_THIN:
            warnings.append("below the v4 depth baseline, review "
                            "(a flag, not a size target)")
        if stats["solution"] < 12:
            warnings.append(f"{stats['solution']} details blocks (expect 12)")
        if stats["exercise"] < 6:
            warnings.append(f"{stats['exercise']} exercises (expect 6)")
        if stats["takeaways"] != 1:
            warnings.append(f"{stats['takeaways']} takeaways blocks (expect 1)")
        if stats["pager"] != 1:
            warnings.append(f"{stats['pager']} pagers (expect 1)")
        for required in ("../../css/style.css", "../../js/sidebar.js", "nav.js"):
            if required not in src:
                errors.append(f"missing asset reference: {required}")

    # Internal links must resolve. Code samples inside <pre> are illustrative
    # (lessons teach relative paths with hrefs like "/menu.html" that are not
    # real site links), so strip pre blocks before scanning.
    d = os.path.dirname(path)
    # Blank out pre bodies rather than deleting them, so line numbers still match.
    linkable = re.sub(r"<pre>.*?</pre>",
                      lambda m: "\n" * m.group(0).count("\n"), src, flags=re.S)
    for m in re.finditer(r'href="([^"#?:]+\.html)([^"]*)"', linkable):
        target = m.group(1)
        if target.startswith("http"):
            continue
        resolved = os.path.normpath(os.path.join(d, target))
        if not os.path.exists(resolved):
            line = src[:m.start()].count("\n") + 1
            errors.append(f"line {line}: broken link -> {target}")

    return stats, errors, warnings


def main():
    root = sys.argv[1]
    # explicit names are relative to root, same as the directory listing below —
    # otherwise `validate.py tutorials/python index.html` silently checks ./index.html
    files = [os.path.join(root, f) for f in sys.argv[2:]] or sorted(
        os.path.join(root, f) for f in os.listdir(root) if f.endswith(".html"))
    total_err = 0
    for path in files:
        stats, errors, warnings = check_file(path)
        name = os.path.basename(path)
        if errors:
            total_err += len(errors)
            print(f"\n[ERROR] {name}  ({stats['kb']}KB)")
            for e in errors:
                print(f"   ! {e}")
        elif warnings:
            print(f"[warn ] {name:32s} {stats['kb']:>3}KB  " + "; ".join(warnings))
        else:
            print(f"[ ok  ] {name:32s} {stats['kb']:>3}KB  "
                  f"det={stats['solution']} ex={stats['exercise']} "
                  f"tbl={stats['tbl']}")
    print(f"\n{len(files)} files checked, {total_err} errors")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
