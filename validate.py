"""Validate LearnHub lesson HTML: structure, tag balance, escaping, links.

Usage:  python validate.py <dir> [file ...]
Exits non-zero if any ERROR is found.
"""
import sys, os, re, html
from html.parser import HTMLParser

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
        if stats["kb"] < 20:
            warnings.append(f"only {stats['kb']}KB (v4 target 20KB+)")
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
