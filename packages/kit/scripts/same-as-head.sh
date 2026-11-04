#!/usr/bin/env bash
# After `pnpm build:kit`: every .etch.txt must equal the committed file apart from the build "timestamp".
# Prints SAME / DIFF per file, restores the files that only differ by their timestamp, exits 1 on any DIFF.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
diffs=0
for f in $(git ls-files 'etch-*/*.etch.txt'); do
  a=$(git show "HEAD:$f" | sed -E 's/"timestamp":"[^"]*"//')
  b=$(sed -E 's/"timestamp":"[^"]*"//' "$f")
  if [ "$a" = "$b" ]; then
    echo "SAME $f"
    git checkout -- "$f"
  else
    echo "DIFF $f"
    diffs=$((diffs + 1))
  fi
done
echo "$(git ls-files 'etch-*/*.etch.txt' | wc -l | tr -d ' ') files, $diffs differ"
[ "$diffs" -eq 0 ]
