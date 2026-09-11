#!/usr/bin/env bash
# Pre-commit gate for depth-pass edits. Run from the repo root:
#   tools/gate.sh <track> <lesson> [<lesson> ...]
# Passes only if validate.py reports 0 errors, quizcheck.py prints OK, and each
# named lesson's pager links are unchanged versus HEAD.
set -u
track=${1:?usage: tools/gate.sh <track> <lesson>...}; shift

v=$(python validate.py "tutorials/$track" 2>&1 | tail -1); echo "  validate: $v"
echo "$v" | grep -q ', 0 errors$' || {
  echo "  GATE FAILED: validation"
  python validate.py "tutorials/$track" 2>&1 | grep -A3 ERROR | head -20
  exit 1
}

pager() { grep -A3 'class="pager"' | grep -o 'href="[^"]*"'; }
for f in "$@"; do
  diff <(git show "HEAD:tutorials/$track/$f.html" | pager) <(pager < "tutorials/$track/$f.html") >/dev/null \
    || { echo "  GATE FAILED: pager changed in $f"; exit 1; }
done

q=$(python tools/quizcheck.py "tutorials/$track" 2>&1 | tail -1); echo "  quizcheck: $q"
[ "$q" = "OK" ] || { echo "  GATE FAILED: quizcheck"; exit 1; }
echo "  gate passed"
