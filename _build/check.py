"""Everything CI checks, runnable locally too:  python3 _build/check.py

1. build_all.py rebuilds every template and runs the audit (fails on audit errors)
2. the rebuilt .etch.txt files must match the committed ones — the build "timestamp" is ignored, and files that
   differ only by it are restored so they do not show up as changes
3. preview/ and builder/kit-data.js must match a fresh build_preview.py (commit them after editing templates)
4. build_site.py must be able to put the website together
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable


def run(*args, **kw):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=kw.get("capture", False))


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, capture_output=True).stdout


def strip_ts(text):
    return re.sub(r'"timestamp":"[^"]*"', "", text)


def main():
    errors = []
    run(PY, "_build/build_all.py")  # check=True: audit errors stop here

    changed = []
    for f in git("ls-files", "*.etch.txt").split():
        committed = git("show", f"HEAD:{f}")
        current = open(os.path.join(ROOT, f), encoding="utf-8").read()
        if strip_ts(committed) != strip_ts(current):
            changed.append(f)
        elif committed != current:
            git("checkout", "--", f)  # only the timestamp moved
    if changed:
        errors.append("templates differ from the committed files (commit the rebuilt .etch.txt): " + ", ".join(changed))

    run(PY, "_build/build_preview.py")
    stale = git("status", "--porcelain", "--", "preview", "builder").strip()
    if stale:
        errors.append("preview / builder data is out of date — run python3 _build/build_preview.py and commit:\n"
                      + stale)

    run(PY, "_build/build_site.py")

    for e in errors:
        print("CHECK FAILED:", e)
    print("check:", "failed" if errors else "ok")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
