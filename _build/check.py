"""Everything CI checks, runnable locally too:  python3 _build/check.py

1. build_all.py rebuilds every template and runs the audit (fails on audit errors)
2. the rebuilt .etch.txt files must match the committed ones — the build "timestamp" is ignored, and files that
   differ only by it are restored so they do not show up as changes
3. preview/ and builder/kit-data.js must match a fresh build_preview.py (commit them after editing templates)
4. build_site.py must be able to put the website together
5. every colour preset in builder/presets.js passes every contrast pair the builder checks
6. every page type in builder/pages.js names section templates that exist
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable


def run(*args, **kw):
    return subprocess.run(args, cwd=ROOT, check=True, text=True, capture_output=kw.get("capture", False))


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, capture_output=True).stdout


def strip_ts(text):
    return re.sub(r'"timestamp":"[^"]*"', "", text)


def luminance(hex_colour):
    rgb = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    rgb = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


def contrast(a, b):
    x, y = luminance(a), luminance(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


# same pairs as PAIRS in builder/builder.js — preset colours: primary, accent, light, text, on-primary,
# button primary bg, its text, button secondary bg, its text
PRESET_PAIRS = [("text on light", 3, 2, 4.5), ("text on primary", 4, 0, 4.5), ("primary on light", 0, 2, 4.5),
                ("icon on accent", 4, 1, 3), ("primary button text", 6, 5, 4.5),
                ("secondary button text", 8, 7, 4.5), ("outline primary button on light", 5, 2, 4.5),
                ("secondary button on the header", 7, 0, 4.5)]


def check_presets():
    text = open(os.path.join(ROOT, "builder", "presets.js"), encoding="utf-8").read()
    presets = json.loads(text[text.index("=") + 1:].strip().rstrip(";"))
    problems = []
    for pr in presets:
        c = pr["colors"]
        if len(c) != 9 or not all(re.fullmatch(r"#[0-9a-f]{6}", x, re.I) for x in c):
            problems.append(f"{pr['name']}: needs 9 colours as #rrggbb")
            continue
        for label, fg, bg, need in PRESET_PAIRS:
            got = contrast(c[fg], c[bg])
            if got < need:
                problems.append(f"{pr['name']}: {label} {got:.2f}:1 (needs {need}:1)")
    return len(presets), problems


def check_page_types():
    """builder/pages.js may only name section templates the builder knows (build_preview.CATALOG)."""
    sys.path.insert(0, HERE)
    from build_preview import CATALOG
    sections = {tid for tid, group, *_ in CATALOG if group == "section"}
    text = open(os.path.join(ROOT, "builder", "pages.js"), encoding="utf-8").read()
    types = json.loads(text[text.index("=") + 1:].strip().rstrip(";"))
    problems = []
    for t in types:
        for item in t.get("sections", []):
            if item.get("id") not in sections:
                problems.append(f"{t.get('id')}: unknown section '{item.get('id')}'")
            if item.get("need") not in ("required", "recommended"):
                problems.append(f"{t.get('id')}/{item.get('id')}: need must be required or recommended")
    return len(types), problems


def main():
    errors = []
    count, problems = check_page_types()
    if problems:
        errors.append("page types:\n  " + "\n  ".join(problems))
    else:
        print(f"page types: {count} use known sections")
    count, problems = check_presets()
    if problems:
        errors.append("colour presets fail contrast:\n  " + "\n  ".join(problems))
    else:
        print(f"presets: {count} pass every contrast pair")
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
