# -*- coding: utf-8 -*-
"""Shared splice helpers for the LearnHub elaboration pass."""
import io
import re

D = '<details class="solution"><summary>'


def _replace_iq_by_position(s, path, iq):
    """Replace the Nth <details> block (1-based) inside the Interview Questions
    section only, so exercise solutions further down can never be touched.
    Used for tracks whose summaries carry no Q-number (e.g. nodejs)."""
    m = re.search(r"(<h2>Interview Questions</h2>)(.*?)(?=<h2>)", s, re.S)
    assert m, "%s: no Interview Questions section" % path
    body = m.group(2)
    blocks = list(re.finditer(r"<details\b[^>]*>.*?</details>", body, re.S))
    for idx in iq:
        assert 1 <= idx <= len(blocks), "%s: no interview answer #%d" % (path, idx)
    for idx in sorted(iq, reverse=True):  # back to front keeps offsets valid
        b = blocks[idx - 1]
        body = body[:b.start()] + iq[idx] + body[b.end():]
    return s[:m.start(2)] + body + s[m.end(2):]


def apply(path, answers=None, mistakes=None, takeaways=None, iq=None):
    """Replace interview answers (by Q-number via `answers`, or by position via
    `iq`); append mistake rows and takeaway items."""
    with io.open(path, encoding="utf-8") as fh:
        before = fh.read()
    s = before
    for q, new in (answers or {}).items():
        pat = re.compile(re.escape(D) + r"(?:<strong>)?" + q + r"\b.*?</details>", re.S)
        s, n = pat.subn(lambda _: new, s, count=1)
        assert n == 1, "%s: %s not matched" % (path, q)
    if iq:
        s = _replace_iq_by_position(s, path, iq)
    if mistakes:
        m = re.search(r"(<h2>Common Mistakes</h2>.*?)(\n\s*</table>)", s, re.S)
        assert m, "%s: no mistakes table" % path
        s = s[:m.end(1)] + "\n" + mistakes + s[m.end(1):]
    if takeaways:
        m2 = re.search(r'(<div class="takeaways"><h3>[^<]*</h3><ul>)(.*?)(\s*</ul></div>)', s, re.S)
        assert m2, "%s: no takeaways" % path
        s = s[:m2.end(2)] + "\n" + takeaways + s[m2.end(2):]

    # Guard against the unclosed-<strong> slip validate.py caught once.
    # Count over the WHOLE file, not per line: existing markup legitimately
    # opens <strong> on one line and closes it on the next.
    for tag in ("strong", "code", "li", "details"):
        opened = len(re.findall(r"<%s[ >]" % tag, s))
        closed = len(re.findall(r"</%s>" % tag, s))
        was = len(re.findall(r"<%s[ >]" % tag, before)) - len(re.findall(r"</%s>" % tag, before))
        if opened - closed != was:
            raise AssertionError(
                "%s: <%s> balance changed by %d (was %d, now %d) — check the block you added"
                % (path, tag, (opened - closed) - was, was, opened - closed))

    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(s)
    print("ok", path)


if __name__ == "__main__":
    # self-check for the positional path: exercise solutions must be untouched
    fixture = ("<h2>Interview Questions</h2>"
               '<details class="solution"><summary>A</summary><p>a</p></details>'
               '<details class="solution"><summary>B</summary><p>b</p></details>'
               "<h2>Exercises</h2>"
               '<details class="solution"><summary>E</summary><p>e</p></details>')
    out = _replace_iq_by_position(fixture, "fixture", {2: '<details class="solution"><summary>B2</summary><p>new</p></details>'})
    assert "B2" in out and ">b<" not in out, out
    assert "<summary>A</summary>" in out and "<summary>E</summary>" in out, out
    print("lib selftest OK")
